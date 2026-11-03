"""Agent 2 - RAG, as graph nodes.

    rewrite -> search -> assess --answer--------------> generate -> verify -> END
                  ^         |
                  |         +--retrieve_again (once)--> retry --+
                  +-------------------------------------------- +
                            +--clarify / abstain / nothing----> no_answer -> END

Whole-document questions (the router's OVERVIEW route: summary, contents, "what is in it") skip search:
    summarize  -> reads the document in order, samples across it, writes ONE summary (1 LLM call)

LLM calls (max 6, enforced by ctx.budget):
  rewrite (only if needed) -> evaluate (only if reranker is unsure) -> retry rewrite (retry only)
  -> evaluate again (only if unsure) -> FINAL ANSWER (always reserved) -> verify (only if risky)
"""
import logging
import re
from collections import defaultdict
from typing import Literal

from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel, Field

from app.agents.context import RequestContext, emit, get_ctx
from app.agents.llm import call_structured, stream_answer
from app.agents.prompts import (ANSWER_PROMPT, EVALUATE_PROMPT, RETRY_PROMPT, REWRITE_PROMPT,
                                SUMMARY_PROMPT, VERIFY_PROMPT)
from app.agents.state import AgentState
from app.core.config import settings
from app.rag.chain import _filename_map, _names, extract_sources
from app.rag.hybrid import load_corpus, merge_unique
from app.rag.memory import count_tokens
from app.rag.reranker import rerank

logger = logging.getLogger(__name__)

NOT_FOUND = "I could not find it in the uploaded documents."
MAX_SUMMARY_DOCS = 5          # when no file is attached, summarise at most this many (newest first)


# ── Structured outputs ──────────────────────────────────────────────────────────

class RewriteResult(BaseModel):
    queries: list[str] = Field(description="1-3 search queries")


class Evaluation(BaseModel):
    is_relevant: bool = False
    is_sufficient: bool = False
    has_conflicts: bool = False
    missing_information: list[str] = Field(default_factory=list)
    recommended_action: Literal["answer", "retrieve_again", "clarify", "abstain"] = "answer"
    clarification_question: str = ""


class Verdict(BaseModel):
    supported: bool
    unsupported_claims: list[str] = Field(default_factory=list)


# ── Helpers (plain functions, easy to test) ─────────────────────────────────────

_FOLLOWUP = re.compile(r"\b(it|its|they|them|their|that|this|those|these|he|she|his|her|there)\b", re.I)
_MULTIPART = re.compile(r"\b(and|vs|versus|compare|difference|both)\b", re.I)


def needs_rewrite(question: str, history: list) -> bool:
    """Cheap rules so simple questions skip the rewrite call."""
    words = len(question.split())
    follow_up = bool(history) and (words <= 8 or bool(_FOLLOWUP.search(question)))
    return follow_up or words < 3 or words > 25 or question.count("?") > 1 or bool(_MULTIPART.search(question))


def sample_evenly(chunks: list[Document], max_tokens: int) -> list[Document]:
    """Keep chunks spread across the whole document so the summary covers start, middle and end."""
    costs = [count_tokens(c.page_content) for c in chunks]
    if sum(costs) <= max_tokens:
        return chunks
    n = max(1, max_tokens // max(1, sum(costs) // len(chunks)))
    step = len(chunks) / n
    out, total = [], 0
    for i in range(n):
        c = chunks[int(i * step)]
        cost = count_tokens(c.page_content)
        if out and total + cost > max_tokens:
            break
        out.append(c)
        total += cost
    return out


def build_context(docs: list[Document], budget: int | None = None) -> tuple[list[Document], str]:
    """Number the chunks [1], [2]... within the token budget. The returned list defines the numbers."""
    budget = budget or settings.CONTEXT_TOKEN_BUDGET
    names = _filename_map(docs)
    used, blocks, tokens = [], [], 0
    for d in docs:
        page = f", page {d.metadata['page']}" if d.metadata.get("page") else ""
        block = f"[{len(used) + 1}] (source: {_names(d.metadata, names)}{page})\n{d.page_content}"
        cost = count_tokens(block)
        if used and tokens + cost > budget:
            break
        used.append(d)
        blocks.append(block)
        tokens += cost
    return used, "\n\n".join(blocks)


def validate_citations(answer: str, docs: list[Document]) -> tuple[list[dict], bool]:
    """Keep only [n] that point to a chunk we really gave the model."""
    cited = {int(n) for group in re.findall(r"\[(\d+(?:\s*,\s*\d+)*)\]", answer)
             for n in re.findall(r"\d+", group)}
    valid = sorted(n for n in cited if 1 <= n <= len(docs))
    invalid = cited - set(valid)
    if invalid:
        logger.warning("Answer cited non-existent excerpts: %s", sorted(invalid))
    citations = []
    for n in valid:
        meta = docs[n - 1].metadata
        dids = meta.get("doc_ids") or []
        citations.append({"ref": n, "document_id": dids[0] if dids else None,
                          "chunk_id": meta.get("_id"), "page": meta.get("page")})
    return citations, not invalid


def write_answer(ctx: RequestContext, messages: list, used: list[Document],
                 context_text: str, label: str) -> dict:
    """Stream the final LLM answer, validate its [n] citations, return the state update."""
    emit("status", "Writing the answer\u2026")
    parts: list[str] = []
    for text in stream_answer(ctx.budget, label, messages):
        parts.append(text)
        emit("token", text)
    answer = "".join(parts)
    citations, citations_ok = validate_citations(answer, used)
    return {"answer": answer, "used_docs": used, "context_text": context_text,
            "sources": extract_sources(used), "citations": citations,
            "grounded": bool(citations) and citations_ok}


def evaluate(ctx: RequestContext, question: str, docs: list[Document]) -> Evaluation:
    """Deterministic checks first; the LLM judge is used only when the reranker is unsure."""
    if not docs:
        return Evaluation(missing_information=["No matching passages were found."],
                          recommended_action="retrieve_again")

    scores = [s for d in docs if (s := d.metadata.get("rerank_score")) is not None]
    top = max(scores, default=None)

    if top is not None and top >= settings.RERANK_HIGH:       # clearly good -> no LLM call
        return Evaluation(is_relevant=True, is_sufficient=True, recommended_action="answer")
    if top is not None and top < settings.RERANK_LOW:         # clearly off-topic -> no LLM call
        return Evaluation(missing_information=["Retrieved passages look unrelated to the question."],
                          recommended_action="retrieve_again")

    if not ctx.budget.can_spend():                            # unsure but no spare calls: best effort
        return Evaluation(is_relevant=True, is_sufficient=True, recommended_action="answer")
    try:
        with ctx.stage("evaluate"):
            return call_structured(
                ctx.budget, "evaluate", Evaluation,
                [SystemMessage(EVALUATE_PROMPT),
                 HumanMessage(f"Question: {question}\n\nExcerpts:\n{build_context(docs)[1]}")])
    except Exception:
        logger.exception("Evaluation failed; answering with what we have")
        return Evaluation(is_relevant=True, is_sufficient=True, recommended_action="answer")


# ── Graph nodes ─────────────────────────────────────────────────────────────────

def rewrite_node(state: AgentState, config: RunnableConfig):
    """Stage 1: the original question is always query #1; rewrites are optional extras."""
    ctx, question, history = get_ctx(config), state["question"], state["history"]
    queries = [question]
    if needs_rewrite(question, history) and ctx.budget.can_spend():
        try:
            with ctx.stage("rewrite"):
                result = call_structured(
                    ctx.budget, "rewrite", RewriteResult,
                    [SystemMessage(REWRITE_PROMPT), *history[-6:], HumanMessage(question)])
            queries += [q.strip() for q in result.queries if q.strip()]
        except Exception:
            logger.exception("Query rewrite failed; using the original question")
    return {"queries": list(dict.fromkeys(queries))[:3]}


def search_node(state: AgentState, config: RunnableConfig):
    """Stages 2-3: semantic search (BM25 optional), merge with earlier candidates (matters on retry), rerank."""
    ctx = get_ctx(config)
    emit("status", "Looking again with different keywords\u2026" if state.get("retried")
         else "Searching your documents\u2026")
    with ctx.stage("hybrid_search"):
        fresh = ctx.retriever.search(state["queries"])
    candidates = merge_unique(state.get("candidates", []), fresh)[: settings.MAX_CANDIDATES]
    with ctx.stage("rerank"):
        docs = rerank(state["question"], candidates, settings.FINAL_TOP_K)   # scored vs ORIGINAL question
    log_top_chunks(docs)                      # NEW
    return {"candidates": candidates, "docs": docs}


def assess_node(state: AgentState, config: RunnableConfig):
    """Stage 4."""
    return {"evaluation": evaluate(get_ctx(config), state["question"], state["docs"])}


def route_after_assess(state: AgentState) -> str:
    """Conditional edge. The `retried` flag is what guarantees there is only ONE retry."""
    action = state["evaluation"].recommended_action
    if action == "answer" and state["docs"]:
        return "generate"
    if action == "retrieve_again" and not state.get("retried"):
        return "retry"
    return "no_answer"                                         # clarify, abstain, or retry already used


def retry_node(state: AgentState, config: RunnableConfig):
    """Stage 5: new queries aimed at what was missing (LLM if budget allows, else the gaps themselves)."""
    ctx, ev, tried = get_ctx(config), state["evaluation"], state["queries"]
    new: list[str] = []
    if ctx.budget.can_spend():
        try:
            with ctx.stage("retry_rewrite"):
                result = call_structured(
                    ctx.budget, "retry_rewrite", RewriteResult,
                    [SystemMessage(RETRY_PROMPT),
                     HumanMessage(f"Question: {state['question']}\nQueries already tried: {tried}\n"
                                  f"Missing: {ev.missing_information}")])
            new = [q.strip() for q in result.queries if q.strip()]
        except Exception:
            logger.exception("Retry rewrite failed")
    if not new:
        new = [m.strip() for m in ev.missing_information if m.strip()]
    new = [q for q in dict.fromkeys(new) if q not in tried][:2]
    return {"retried": True, "queries": new}


def route_after_retry(state: AgentState) -> str:
    return "search" if state["queries"] else "no_answer"


def generate_node(state: AgentState, config: RunnableConfig):
    """Stages 6-7: build numbered context, stream the answer, validate its citations."""
    ctx, ev = get_ctx(config), state["evaluation"]
    used, context_text = build_context(state["docs"])

    notes = []
    if ev.has_conflicts:
        notes.append("Excerpts CONFLICT - point out the disagreement.")
    if ev.missing_information:
        notes.append("Not found: " + "; ".join(ev.missing_information) + ".")
    messages = [SystemMessage(ANSWER_PROMPT.format(context=context_text, notes=" ".join(notes) or "None.")),
                *state["history"], HumanMessage(state["question"])]

    return write_answer(ctx, messages, used, context_text, "final_answer")


def summarize_node(state: AgentState, config: RunnableConfig):
    """Whole-document summary: no similarity search, just read the chunks in order and sample across them."""
    ctx = get_ctx(config)
    emit("status", "Reading your document\u2026")
    with ctx.stage("load_document"):
        corpus = load_corpus(ctx.user_id, ctx.doc_ids)
    if not corpus:
        text = "I couldn't find any indexed content to summarise. Check that the document finished processing."
        emit("token", text)
        return {"answer": text}

    by_doc = defaultdict(list)
    for c in corpus:
        dids = c.metadata.get("doc_ids") or [None]
        by_doc[dids[0]].append(c)
    newest = sorted(by_doc, key=lambda d: d or 0, reverse=True)[:MAX_SUMMARY_DOCS]
    per_doc = settings.SUMMARY_TOKEN_BUDGET // len(newest)

    picked: list[Document] = []
    for doc_id in newest:
        chunks = sorted(by_doc[doc_id],
                        key=lambda c: (c.metadata.get("page") or 0, c.metadata.get("chunk_index") or 0))
        picked += sample_evenly(chunks, per_doc)
    used, context_text = build_context(picked, budget=settings.SUMMARY_TOKEN_BUDGET)

    messages = [SystemMessage(SUMMARY_PROMPT.format(context=context_text)),
                *state["history"], HumanMessage(state["question"])]
    return write_answer(ctx, messages, used, context_text, "summary")


def verify_node(state: AgentState, config: RunnableConfig):
    """Optional fact-check AFTER streaming. Runs only for risky answers and only if a call is left."""
    ctx, ev = get_ctx(config), state["evaluation"]
    risky = ev.has_conflicts or bool(ev.missing_information)
    if not risky or not ctx.budget.can_spend(keep=0):
        return {}
    try:
        with ctx.stage("verify"):
            verdict = call_structured(
                ctx.budget, "verify", Verdict,
                [SystemMessage(VERIFY_PROMPT),
                 HumanMessage(f"Excerpts:\n{state['context_text']}\n\nDraft answer:\n{state['answer']}")])
    except Exception:
        logger.exception("Verification failed")
        return {}
    if verdict.supported:
        return {}
    warning = ("\n\n> \u26a0\ufe0f Some statements may not be fully supported by your documents: "
               + "; ".join(verdict.unsupported_claims[:3]))
    emit("token", warning)
    return {"answer": state["answer"] + warning, "grounded": False}


def no_answer_node(state: AgentState):
    """Anything that can't be answered: no documents, clarification needed, or not found. No LLM call."""
    ev = state.get("evaluation")
    if not state.get("has_docs"):
        text = "You haven't uploaded any documents yet. Add a file and ask again."
    elif ev is not None and ev.recommended_action == "clarify":
        text = ev.clarification_question.strip() or "Could you tell me more about what you're looking for?"
    else:
        gaps = ("; ".join(ev.missing_information) if ev is not None else "").rstrip(". ")
        text = (NOT_FOUND + (f" Missing: {gaps}." if gaps else "")
                + " Try rephrasing, or tell me which document to look in.")
    emit("token", text)
    return {"answer": text}

def log_top_chunks(docs: list[Document]) -> None:
    def f(x):
        return f"{x:.4f}" if isinstance(x, (int, float)) else "n/a"
    lines = [f"Top {len(docs)} chunks after rerank:"]
    for i, d in enumerate(docs, 1):
        m = d.metadata
        lines.append(
            f"  #{i} rerank_prob={f(m.get('rerank_score'))}  cosine={f(m.get('score'))}  "
            f"page={m.get('page')}  doc_ids={m.get('doc_ids')}  | "
            f"{' '.join(d.page_content.split())[:70]}…")
    logger.info("\n".join(lines))