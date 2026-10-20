from functools import lru_cache

from langchain_openai import OpenAIEmbeddings

from app.core.config import settings


@lru_cache
def get_embeddings() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(
        model=settings.EMBEDDING_MODEL,
        api_key=settings.OPENAI_API_KEY or None,
        base_url=settings.OPENAI_BASE_URL,
        max_retries=3,
    )
