"""Knowledge-base agent with a deterministic fast path and an evidence-checked advanced path."""
import logging
import re

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from sqlalchemy import select

from app.agents.evidence import Evidence
from app.agents.llm import get_llm
from app.agents.prompts import (
    CHECK_PROMPT,
    KB_AGENT_PROMPT,
    KB_ANSWER_PROMPT,
    KB_NUDGE,
    KB_SIMPLE_ANSWER_PROMPT,
    REWRITE_PROMPT,
    SUMMARY_MAP_PROMPT,
    SUMMARY_REDUCE_PROMPT,
)
from app.agents.state import AgentState
from app.core.config import settings
from app.rag.chain import _filename_map, _names, format_context
from app.rag.retriever import retrieve
from app.db.models import Document as DocumentModel
from app.db.session import SessionLocal
from app.rag.loaders import load_file
from app.rag.splitter import split_documents

logger = logging.getLogger(__name__)


def _ev(config: RunnableConfig) -> Evidence:
    return config["configurable"]["evidence"]


# Query planning is deliberately deterministic: obvious requests should not pay for
# another LLM call just to decide whether they are simple or complex.
SUMMARY_RE = re.compile(
    r"\b(summarize|summarise|summary|give me an overview|overview of)\b.*"
    r"\b(document|file|pdf|report|book|notes?)\b|"
    r"\b(summarize|summarise)\s+(this|the|my|attached|uploaded)\b|"
    r"\b(summarize|summarise|summary)\s+(chapter|section|part)\b",
    re.I,
)
COMPLEX_RE = re.compile(
    r"\b(compare|comparison|contrast|differentiate|pros and cons|advantages and disadvantages|"
    r"across chapters|across sections|all aspects|comprehensive|in depth|in detail|"
    r"step by step|multiple perspectives)\b",
    re.I,
)
MULTI_PART_RE = re.compile(r"\b(and|versus|vs\.?|while|whereas|respectively)\b", re.I)


def classify_kb_task(question: str) -> dict:
    """Return task type and execution policy without an extra model call."""
    q = (question or "").strip()
    if SUMMARY_RE.search(q):
        return {
            "task_type": "document_summary",
            "retrieval_strategy": "full_document",
            "needs_verification": False,
        }

    # Avoid treating ordinary conjunctions in a sentence as complex unless the request
    # explicitly asks for comparison, multiple dimensions, or multiple questions.
    question_marks = q.count("?")
    is_complex = bool(COMPLEX_RE.search(q)) or question_marks > 1
    if not is_complex and re.search(r"\b(compare|contrast|differentiate)\b", q, re.I):
        is_complex = True
    if not is_complex and MULTI_PART_RE.search(q) and re.search(
        r"\b(algorithm|model|method|approach|architecture|advantages|limitations|performance)\b",
        q, re.I
    ):
        is_complex = True

    return {
        "task_type": "complex" if is_complex else "simple",
        "retrieval_strategy": "multi_search" if is_complex else "single_search",
        "needs_verification": is_complex,
    }


def kb_plan_node(state: AgentState):
    plan = classify_kb_task(state.get("question", ""))
    logger.info(
        "KB plan: task_type=%s retrieval_strategy=%s needs_verification=%s",
        plan["task_type"], plan["retrieval_strategy"], plan["needs_verification"],
    )
    return plan


def route_after_kb_plan(state: AgentState) -> str:
    if state.get("task_type") == "document_summary":
        return "kb_full_summary"
    return "kb_agent" if state.get("needs_verification", False) else "kb_simple_retrieve"




# ── Full-document Map-Reduce summary path ─────────────────────────────────────

SUMMARY_GROUP_CHAR_BUDGET = 16000
SUMMARY_REDUCE_BATCH_SIZE = 8


def _resolve_summary_documents(ev: Evidence) -> tuple[list[dict], str | None]:
    """Resolve only ready documents owned by this user.

    Explicit attachment IDs must all belong to this user and be ready. Without IDs,
    select a uniquely named document or the only ready document; otherwise clarify.
    """
    from pathlib import Path

    with SessionLocal() as db:
        stmt = select(DocumentModel).where(
            DocumentModel.user_id == ev.user_id,
            DocumentModel.status == "ready",
        )
        rows = list(db.scalars(stmt).all())

        if ev.doc_ids:
            wanted_order = list(dict.fromkeys(int(x) for x in ev.doc_ids))
            wanted = set(wanted_order)
            by_id = {d.id: d for d in rows}
            selected = [by_id[doc_id] for doc_id in wanted_order if doc_id in by_id]
            if len(selected) != len(wanted):
                return [], (
                    "I couldn't access one or more selected documents. "
                    "Please reattach a document that is ready in your library."
                )
        else:
            q = (ev.question or "").casefold()
            named = [
                d for d in rows
                if d.filename and (
                    d.filename.casefold() in q
                    or Path(d.filename).stem.casefold() in q
                )
            ]
            if len(named) == 1:
                selected = named
            elif len(rows) == 1:
                selected = rows
            elif not rows:
                return [], "There are no ready documents available to summarize."
            else:
                names = "\n".join(f"- {d.filename}" for d in rows[:20])
                return [], (
                    "I found multiple documents in your library. Which one should I summarize?\n\n"
                    f"{names}"
                )

        return [
            {
                "id": d.id,
                "filename": d.filename,
                "stored_path": d.stored_path,
                "chunk_count": d.chunk_count,
            }
            for d in selected
        ], None


def _ordered_summary_chunks(ev: Evidence, documents: list[dict]) -> list[tuple[int, object]]:
    """Recreate ingestion's exact splitter boundaries from persisted source files.

    The current splitter discards start_index and ChunkRef has no chunk ordinal.
    Reloading and splitting with the same pipeline preserves source order and pages,
    without embeddings or semantic top-k retrieval.
    """
    all_chunks = []
    for doc_info in documents:
        raw_docs = load_file(doc_info["stored_path"])
        chunks = split_documents(raw_docs)
        for index, chunk in enumerate(chunks):
            chunk.metadata = {
                **(chunk.metadata or {}),
                "user_id": ev.user_id,
                "doc_id": doc_info["id"],
                "doc_ids": [doc_info["id"]],
                "filename": doc_info["filename"],
                "source": doc_info["filename"],
                "page": chunk.metadata.get("page"),
                "chunk_index": index,
            }
        all_chunks.extend(chunks)

    return ev.add(all_chunks) if all_chunks else []


def _group_chunks(
    numbered_chunks: list[tuple[int, object]],
    char_budget: int = SUMMARY_GROUP_CHAR_BUDGET,
) -> list[list[tuple[int, object]]]:
    groups, current, current_chars = [], [], 0
    for item in numbered_chunks:
        _, doc = item
        cost = len(doc.page_content) + 100
        if current and current_chars + cost > char_budget:
            groups.append(current)
            current, current_chars = [], 0
        current.append(item)
        current_chars += cost
    if current:
        groups.append(current)
    return groups


def _render_summary_group(group: list[tuple[int, object]]) -> str:
    blocks = []
    for ref, doc in group:
        filename = doc.metadata.get("filename", "document")
        page = doc.metadata.get("page")
        location = f"{filename}, page {page}" if page is not None else filename
        blocks.append(f"[{ref}] ({location})\n{doc.page_content}")
    return "\n\n".join(blocks)


def _map_summary(group: list[tuple[int, object]], group_number: int) -> str:
    reply = get_llm(temperature=0, max_tokens=1100).invoke([
        SystemMessage(SUMMARY_MAP_PROMPT),
        HumanMessage(
            f"Summarize section group {group_number}. Preserve citations exactly.\n\n"
            f"{_render_summary_group(group)}"
        ),
    ])
    return str(reply.content).strip()


def _reduce_summaries(summaries: list[str], *, question: str) -> str:
    """Recursively condense intermediate summaries, then write the final answer."""
    current = summaries
    while len(current) > SUMMARY_REDUCE_BATCH_SIZE:
        next_level = []
        for start in range(0, len(current), SUMMARY_REDUCE_BATCH_SIZE):
            batch = current[start:start + SUMMARY_REDUCE_BATCH_SIZE]
            reply = get_llm(temperature=0, max_tokens=1100).invoke([
                SystemMessage(SUMMARY_REDUCE_PROMPT),
                HumanMessage(
                    "Combine these partial summaries into a compact intermediate summary. "
                    "Keep citations unchanged; do not add unsupported details.\n\n"
                    + "\n\n--- PARTIAL SUMMARY ---\n\n".join(batch)
                ),
            ])
            next_level.append(str(reply.content).strip())
        current = next_level

    reply = get_llm(temperature=0, max_tokens=1800).invoke([
        SystemMessage(SUMMARY_REDUCE_PROMPT),
        HumanMessage(
            f"User request: {question}\n\n"
            "Create the final answer with useful headings. Preserve exact citation references "
            "on factual claims. Do not add facts absent from the intermediate summaries.\n\n"
            + "\n\n--- SECTION SUMMARY ---\n\n".join(current)
        ),
    ])
    return str(reply.content).strip()


def kb_full_document_summary_node(state: AgentState, config: RunnableConfig):
    """Summarize every chunk of the selected ready document(s) with Map-Reduce."""
    ev = _ev(config)
    try:
        documents, issue = _resolve_summary_documents(ev)
        if issue:
            return {"messages": [AIMessage(content=issue)]}

        numbered_chunks = _ordered_summary_chunks(ev, documents)
        if not numbered_chunks:
            return {"messages": [AIMessage(
                content="I couldn't extract readable text from the selected document(s). "
                        "Scanned PDFs may require OCR before they can be summarized."
            )]}

        groups = _group_chunks(numbered_chunks)
        logger.info(
            "Full-document summary: user_id=%s doc_ids=%s chunks=%d groups=%d",
            ev.user_id, [d["id"] for d in documents], len(numbered_chunks), len(groups),
        )

        summaries = [
            _map_summary(group, index + 1)
            for index, group in enumerate(groups)
        ]
        final_text = _reduce_summaries(
            summaries, question=state.get("question", ev.question)
        )
        return {"messages": [AIMessage(content=final_text)]}

    except Exception:
        logger.exception(
            "Full-document summarization failed for user_id=%s doc_ids=%s",
            ev.user_id, ev.doc_ids,
        )
        return {"messages": [AIMessage(
            content="I couldn't complete the full-document summary because the source file "
                    "could not be processed. Please check that it is still available and try again."
        )]}


def _standalone_query(state: AgentState) -> str:
    """Add the latest prior user question for short elliptical follow-ups without an LLM call."""
    question = (state.get("question") or "").strip()
    if len(question.split()) > 8:
        return question
    history = state.get("history") or []
    previous_user = None
    for message in reversed(history):
        if getattr(message, "type", "") in ("human", "user"):
            content = getattr(message, "content", "")
            if isinstance(content, str) and content.strip():
                previous_user = content.strip()
                break
    if previous_user and re.search(
        r"\b(it|this|that|these|those|they|them|its|their|what about|how about|and)\b",
        question, re.I
    ):
        return f"{previous_user}\nFollow-up question: {question}"
    return question


def kb_simple_retrieve_node(state: AgentState, config: RunnableConfig):
    """One deterministic retrieval for simple requests; no agent loop or judge call."""
    ev = _ev(config)
    query = _standalone_query(state)
    ev.queries.append(query)
    docs = retrieve(query, ev.user_id, ev.doc_ids)
    if docs:
        ev.add(docs)
    logger.info(
        "KB fast path: task_type=%s query=%r retrieved_chunks=%d",
        state.get("task_type"), query[:200], len(docs or []),
    )
    return {}


# ── Advanced-path tools ───────────────────────────────────────────────────────

@tool
def search_knowledge_base(query: str, config: RunnableConfig) -> str:
    """Vector-search the user's uploaded documents. Returns numbered excerpts [n] with their
    source file, page and relevance score. Use a specific, standalone query."""
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
    """Rewrite a search query that returned weak, off-topic or empty results."""
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
    """Verify a draft answer against all excerpts retrieved so far."""
    ev = _ev(config)
    if not ev.docs:
        verdict = {
            "supported": False,
            "unsupported_claims": [],
            "missing_information": ["Nothing relevant has been retrieved yet."],
            "suggestion": "Search the knowledge base (use rewrite_query if needed).",
        }
    else:
        judge = get_llm(0).with_structured_output(Verdict, method="function_calling")
        verdict = judge.invoke([
            SystemMessage(CHECK_PROMPT),
            HumanMessage(
                f"Question: {ev.question}\n\nExcerpts:\n{format_context(ev.docs)}"
                f"\n\nDraft answer:\n{draft_answer}"
            ),
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


# ── Advanced agent path ───────────────────────────────────────────────────────

def kb_agent_node(state: AgentState, config: RunnableConfig):
    # Verification remains available only on this advanced path.
    tools = KB_TOOLS if state.get("needs_verification", True) else [
        search_knowledge_base, rewrite_query
    ]
    llm = get_llm(0).bind_tools(tools)
    reply = llm.invoke(
        [SystemMessage(KB_AGENT_PROMPT), *state.get("history", []), *state["messages"]],
        config,
    )
    return {"messages": [reply], "steps": state.get("steps", 0) + 1}


def _verified_since_last_search(messages) -> bool:
    for message in reversed(messages):
        if isinstance(message, ToolMessage):
            if message.name == "check_sources":
                return True
            if message.name == "search_knowledge_base":
                return False
    return False


def route_after_kb_agent(state: AgentState) -> str:
    if state.get("steps", 0) >= settings.AGENT_MAX_STEPS:
        return "kb_answer"
    last_message = state["messages"][-1]
    if getattr(last_message, "tool_calls", None):
        return "kb_tools"
    if state.get("needs_verification", True) and not _verified_since_last_search(state["messages"]):
        return "kb_nudge"
    return "kb_answer"


def kb_nudge_node(state: AgentState):
    return {"messages": [HumanMessage(KB_NUDGE)]}


_ANSWER = ChatPromptTemplate.from_messages([
    ("system", KB_ANSWER_PROMPT),
    MessagesPlaceholder("history"),
    ("human", "{question}"),
])
_SIMPLE_ANSWER = ChatPromptTemplate.from_messages([
    ("system", KB_SIMPLE_ANSWER_PROMPT),
    MessagesPlaceholder("history"),
    ("human", "{question}"),
])


def _verification_note(ev: Evidence, needs_verification: bool) -> str:
    if not needs_verification:
        return "Separate judge verification was intentionally skipped for this fast-path request."
    verdict = ev.last_verdict
    if verdict is None:
        return "The evidence was not verified."
    if verdict["supported"]:
        return "Verified - the retrieved excerpts support the answer."
    bits = verdict["unsupported_claims"] + verdict["missing_information"]
    return "NOT fully verified. Unsupported or missing: " + "; ".join(bits or ["unspecified"])


def kb_answer_node(state: AgentState, config: RunnableConfig):
    """Generate the user-facing answer once, from collected evidence."""
    ev = _ev(config)
    needs_verification = state.get("needs_verification", True)
    prompt = _ANSWER if needs_verification else _SIMPLE_ANSWER
    reply = (prompt | get_llm()).invoke({
        "context": format_context(ev.docs),
        "verification": _verification_note(ev, needs_verification),
        "history": state.get("history", []),
        "question": state["question"],
    }, config)
    return {"messages": [reply]}
