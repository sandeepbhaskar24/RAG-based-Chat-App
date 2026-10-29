"""Agent 2 - Knowledge Base Research Agent (Qdrant).

Loop:  kb_agent --tool calls--> kb_tools --> kb_agent ...
       kb_agent --done--> (kb_nudge if it skipped verification) --> kb_answer (streams)
"""
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from app.agents.evidence import Evidence
from app.agents.llm import get_llm
from app.agents.prompts import (CHECK_PROMPT, KB_AGENT_PROMPT, KB_ANSWER_PROMPT, KB_NUDGE,
                                REWRITE_PROMPT)
from app.agents.state import AgentState
from app.core.config import settings
from app.rag.chain import _filename_map, _names, format_context
from app.rag.retriever import retrieve


def _ev(config: RunnableConfig) -> Evidence:
    return config["configurable"]["evidence"]


# ── Tools ───────────────────────────────────────────────────────────────────────

@tool
def search_knowledge_base(query: str, config: RunnableConfig) -> str:
    """Vector-search the user's uploaded documents. Returns numbered excerpts [n] with their
    source file, page and relevance score. Use a specific, standalone query; call it once per
    sub-topic when a question has several parts. Low scores or off-topic excerpts mean weak results."""
    ev = _ev(config)
    ev.queries.append(query)
    docs = retrieve(query, ev.user_id, ev.doc_ids)
    if not docs:
        return "No results."
    hits = ev.add(docs)
    names = _filename_map([d for _, d in hits])
    blocks = []
    for ref, d in hits:
        page = f", page {d.metadata['page']}" if d.metadata.get("page") else ""
        score = d.metadata.get("score")
        rel = f"; relevance {score:.2f}" if score is not None else ""
        blocks.append(f"[{ref}] (source: {_names(d.metadata, names)}{page}{rel})\n{d.page_content}")
    return "\n\n".join(blocks)


@tool
def rewrite_query(original_query: str, problem: str, config: RunnableConfig) -> str:
    """Rewrite a search query that returned weak, off-topic or empty results. `problem` says what
    went wrong (e.g. 'results were about travel policy, not leave'). Returns ONE improved query
    to pass to search_knowledge_base."""
    ev = _ev(config)
    tried = "\n".join(f"- {q}" for q in ev.queries) or "(none)"
    reply = get_llm(0).invoke([
        SystemMessage(REWRITE_PROMPT),
        HumanMessage(f"User question: {ev.question}\nFailing query: {original_query}\n"
                     f"Problem: {problem}\nQueries already tried:\n{tried}"),
    ])
    return str(reply.content).strip().strip('"')


class Verdict(BaseModel):
    supported: bool = Field(description="True only if EVERY claim in the draft is backed by the excerpts")
    unsupported_claims: list[str] = Field(default_factory=list)
    missing_information: list[str] = Field(default_factory=list)
    suggestion: str = Field(default="", description="What to search for next, if anything")


@tool
def check_sources(draft_answer: str, config: RunnableConfig) -> str:
    """Verify a draft answer (with [n] citations) against ALL excerpts retrieved so far.
    Returns SUPPORTED, or NOT SUPPORTED with the unsupported claims and what is still missing."""
    ev = _ev(config)
    if not ev.docs:
        verdict = {"supported": False, "unsupported_claims": [],
                   "missing_information": ["Nothing relevant has been retrieved yet."],
                   "suggestion": "Search the knowledge base (use rewrite_query if needed)."}
    else:
        judge = get_llm(0).with_structured_output(Verdict, method="function_calling")
        verdict = judge.invoke([
            SystemMessage(CHECK_PROMPT),
            HumanMessage(f"Question: {ev.question}\n\nExcerpts:\n{format_context(ev.docs)}"
                         f"\n\nDraft answer:\n{draft_answer}"),
        ]).model_dump()
    ev.last_verdict = verdict
    if verdict["supported"]:
        return "SUPPORTED: every claim is backed by the retrieved excerpts."
    lines = ["NOT SUPPORTED"]
    lines += [f"- Unsupported claim: {c}" for c in verdict["unsupported_claims"]]
    lines += [f"- Missing: {m}" for m in verdict["missing_information"]]
    if verdict["suggestion"]:
        lines.append(f"Suggestion: {verdict['suggestion']}")
    return "\n".join(lines)


KB_TOOLS = [search_knowledge_base, rewrite_query, check_sources]


# ── Nodes ───────────────────────────────────────────────────────────────────────

def kb_agent_node(state: AgentState, config: RunnableConfig):
    llm = get_llm(0).bind_tools(KB_TOOLS)
    reply = llm.invoke(
        [SystemMessage(KB_AGENT_PROMPT), *state["history"], *state["messages"]], config)
    return {"messages": [reply], "steps": state.get("steps", 0) + 1}


def _verified_since_last_search(messages) -> bool:
    for m in reversed(messages):
        if isinstance(m, ToolMessage):
            if m.name == "check_sources":
                return True
            if m.name == "search_knowledge_base":
                return False
    return False


def route_after_kb_agent(state: AgentState) -> str:
    """Conditional edge: tools -> loop, unverified -> nudge, otherwise write the answer."""
    if state.get("steps", 0) >= settings.AGENT_MAX_STEPS:
        return "kb_answer"                                  # loop guard
    if getattr(state["messages"][-1], "tool_calls", None):
        return "kb_tools"
    if not _verified_since_last_search(state["messages"]):
        return "kb_nudge"
    return "kb_answer"


def kb_nudge_node(state: AgentState):
    return {"messages": [HumanMessage(KB_NUDGE)]}


_ANSWER = ChatPromptTemplate.from_messages([
    ("system", KB_ANSWER_PROMPT),
    MessagesPlaceholder("history"),
    ("human", "{question}"),
])


def _verification_note(ev: Evidence) -> str:
    v = ev.last_verdict
    if v is None:
        return "The evidence was not verified."
    if v["supported"]:
        return "Verified - the retrieved excerpts support the answer."
    bits = v["unsupported_claims"] + v["missing_information"]
    return "NOT fully verified. Unsupported or missing: " + "; ".join(bits or ["unspecified"])


def kb_answer_node(state: AgentState, config: RunnableConfig):
    """Final, streamed answer written from the collected evidence only."""
    ev = _ev(config)
    reply = (_ANSWER | get_llm()).invoke({
        "context": format_context(ev.docs),
        "verification": _verification_note(ev),
        "history": state["history"],
        "question": state["question"],
    }, config)
    return {"messages": [reply]}