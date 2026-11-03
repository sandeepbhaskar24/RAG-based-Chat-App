"""LLM factory + the per-request call budget.

Every LLM call in the app goes through `call_structured` or `stream_answer`, and both of them
spend from an LLMBudget. The limit is enforced in code, not in a prompt.
"""
import json
import logging
import re
import threading
import time
from collections.abc import Iterator
from dataclasses import dataclass, field

from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from app.core.config import settings

logger = logging.getLogger(__name__)


def get_llm(temperature: float | None = None, max_tokens: int | None = None) -> ChatOpenAI:
    """Chat model for every agent.

    max_tokens matters on OpenRouter: without it, credit for the model's full output
    limit is reserved per call, which fails with 402 when the balance is low.
    """
    return ChatOpenAI(
        model=settings.LLM_MODEL,
        temperature=settings.LLM_TEMPERATURE if temperature is None else temperature,
        max_tokens=max_tokens or settings.LLM_MAX_TOKENS,
        api_key=settings.OPENROUTER_API_KEY or None,
        base_url=settings.OPENAI_BASE_URL,
        max_retries=2,
        streaming=True,
    )


# ── Call budget ─────────────────────────────────────────────────────────────────

class BudgetExceeded(RuntimeError):
    pass


@dataclass
class LLMBudget:
    """Counts LLM calls for ONE user request (shared by all agents)."""
    limit: int = field(default_factory=lambda: settings.MAX_LLM_CALLS)
    used: int = 0
    labels: list[str] = field(default_factory=list)
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    @property
    def remaining(self) -> int:
        return self.limit - self.used

    def can_spend(self, keep: int = 1) -> bool:
        """True if we can make one more call and still have `keep` calls left.

        Optional steps use keep=1 so the final answer call is always reserved.
        """
        return self.remaining > keep

    def spend(self, label: str) -> None:
        with self._lock:
            if self.used >= self.limit:
                raise BudgetExceeded(f"LLM call budget ({self.limit}) exhausted before '{label}'")
            self.used += 1
            self.labels.append(label)


def message_text(msg) -> str:
    """Plain text of a message/chunk (content may be a string or a list of parts)."""
    c = msg.content
    if isinstance(c, str):
        return c
    return "".join(p.get("text", "") for p in c if isinstance(p, dict) and p.get("type") == "text")


class StructuredOutputError(RuntimeError):
    """The model replied, but not with usable structured data."""


def _parse_json_reply(schema: type[BaseModel], raw) -> BaseModel | None:
    """Fallback: some models answer in plain text/JSON instead of a tool call. Try to recover it."""
    text = re.sub(r"```(?:json)?", "", message_text(raw)).strip()
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end <= start:
        return None
    try:
        return schema.model_validate(json.loads(text[start:end + 1]))
    except Exception:
        return None


STRUCTURED_MAX_TOKENS = 1500     # reasoning models spend part of this on "thinking"


def _with_schema_hint(schema: type[BaseModel], messages: list) -> list:
    """Tell the model what JSON to produce if it doesn't use the tool call (we can parse that)."""
    from langchain_core.messages import SystemMessage

    hint = ("\n\nIf you cannot call the function, reply with ONLY a JSON object matching this schema: "
            + json.dumps(schema.model_json_schema()))
    if messages and isinstance(messages[0], SystemMessage):
        return [SystemMessage(str(messages[0].content) + hint), *messages[1:]]
    return [SystemMessage(hint.strip()), *messages]


def call_structured(budget: LLMBudget, label: str, schema: type[BaseModel], messages: list):
    """One non-streaming call that returns a validated `schema` object (e.g. a routing decision).

    Never returns None: raises StructuredOutputError instead, so callers can fall back.
    """
    budget.spend(label)
    start = time.perf_counter()
    try:
        llm = get_llm(0, max_tokens=STRUCTURED_MAX_TOKENS).with_structured_output(
            schema, method="function_calling", include_raw=True)
        out = llm.invoke(_with_schema_hint(schema, messages))
        result = out.get("parsed")
        if result is None and out.get("raw") is not None:
            result = _parse_json_reply(schema, out["raw"])      # free recovery, no extra LLM call
        if result is None:
            raw = out.get("raw")
            logger.warning("[%s] unusable structured output: parsing_error=%s finish_reason=%s content=%r",
                           label, out.get("parsing_error"),
                           (getattr(raw, "response_metadata", None) or {}).get("finish_reason"),
                           message_text(raw)[:200] if raw is not None else None)
            raise StructuredOutputError(f"Model returned no valid {schema.__name__} for '{label}'")
        return result
    finally:
        logger.info("LLM call %d/%d [%s] %.0f ms", budget.used, budget.limit, label,
                    (time.perf_counter() - start) * 1000)


def stream_answer(budget: LLMBudget, label: str, messages: list,
                  temperature: float | None = None) -> Iterator[str]:
    """One streaming call; yields text pieces."""
    budget.spend(label)
    start = time.perf_counter()
    try:
        for chunk in get_llm(temperature).stream(messages):
            text = message_text(chunk)
            if text:
                yield text
    finally:
        logger.info("LLM call %d/%d [%s] %.0f ms", budget.used, budget.limit, label,
                    (time.perf_counter() - start) * 1000)