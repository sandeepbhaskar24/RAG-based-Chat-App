from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]  # backend/
ROOT_DIR = BASE_DIR.parent                      # repo root


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(ROOT_DIR / ".env", BASE_DIR / ".env"),
        extra="ignore",
    )

    # App
    APP_NAME: str = "RAG Chat API"
    DEBUG: bool = False
    CORS_ORIGINS: list[str] = ["*"]

    # Auth
    JWT_SECRET: str = "change-me"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    # Database
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/rag_chat?charset=utf8mb4"

    # OpenAI / LLM
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str | None = None
    LLM_MODEL: str = "gpt-4o-mini"
    LLM_TEMPERATURE: float = 0.2
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    EMBEDDING_DIM: int = 1536

    # Qdrant
    QDRANT_URL: str = "http://localhost:6333"   # use ":memory:" for an in-process store
    QDRANT_API_KEY: str | None = None
    QDRANT_COLLECTION: str = "documents"

    # RAG tuning
    CHUNK_SIZE: int = 900
    CHUNK_OVERLAP: int = 120
    RETRIEVAL_K: int = 5
    HISTORY_TOKEN_BUDGET: int = 2000

    # Uploads
    UPLOAD_DIR: Path = BASE_DIR / "storage" / "uploads"
    MAX_UPLOAD_MB: int = 20
    ALLOWED_EXTENSIONS: set[str] = {".pdf", ".docx", ".txt", ".md"}


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
