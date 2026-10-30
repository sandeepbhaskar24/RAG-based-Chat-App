from langchain_openai import ChatOpenAI

from app.core.config import settings


def get_llm(temperature: float | None = None, max_tokens: int | None = None) -> ChatOpenAI:
    """Chat model for every agent. streaming=True so LangGraph can emit token chunks.

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