from langchain_openai import ChatOpenAI

from app.core.config import settings


def get_llm(temperature: float | None = None) -> ChatOpenAI:
    """Chat model for every agent. streaming=True so LangGraph can emit token chunks."""
    return ChatOpenAI(
        model=settings.LLM_MODEL,
        temperature=settings.LLM_TEMPERATURE if temperature is None else temperature,
        api_key=settings.OPENROUTER_API_KEY or None,
        base_url=settings.OPENAI_BASE_URL,
        max_retries=2,
        streaming=True,
    )