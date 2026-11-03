from functools import lru_cache
from pathlib import Path
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]  # backend/
ROOT_DIR = BASE_DIR.parent                      # repo root

# Load variables from the .env file into the system environment
load_dotenv()

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
    JWT_SECRET: str = os.getenv("JWT_SECRET")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    # OpenAI / LLM
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY")
    OPENAI_BASE_URL: str = "https://openrouter.ai/api/v1"
    # OPENAI_BASE_URL:str = "https://integrate.api.nvidia.com/v1"

    # LLM_MODEL: str = "nvidia/nemotron-3.5-super-vl:free"
    LLM_MODEL: str = "gpt-4o-mini"
    # LLM_MODEL: str = "nvidia/nemotron-3-embed-1b"

    LLM_TEMPERATURE: float = 0.2
    LLM_MAX_TOKENS: int = 1800
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    # EMBEDDING_MODEL: str = "nvidia/embeddings-nv-embed-qa-4"
    EMBEDDING_DIM: int = 1536

    # Qdrant
    QDRANT_URL: str = "http://localhost:6333"   # use ":memory:" for an in-process store
    QDRANT_API_KEY: str | None = None
    QDRANT_COLLECTION: str = "documents"

    # RAG tuning
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 120
    RETRIEVAL_K: int = 10
    HISTORY_TOKEN_BUDGET: int = 2000

    # Agents
    AGENT_MAX_STEPS: int = 6
    WEATHER_TIMEOUT: float = 10.0

    # Agents / RAG pipeline
    USE_BM25: bool = False
    MAX_LLM_CALLS: int = 6
    DENSE_TOP_K: int = 30
    BM25_TOP_K: int = 30
    RRF_K: int = 60
    MAX_CANDIDATES: int = 60
    FINAL_TOP_K: int = 6
    CONTEXT_TOKEN_BUDGET: int = 3000
    RERANK_MODEL: str = "Xenova/ms-marco-MiniLM-L-6-v2"
    RERANK_HIGH: float = 0.5
    RERANK_LOW: float = 0.05
    ROUTER_MIN_CONFIDENCE: float = 0.5

    SUMMARY_TOKEN_BUDGET: int = 6000   # excerpt tokens sent to the LLM for "summarise the document"

    # Uploads
    UPLOAD_DIR: Path = BASE_DIR / "storage" / "uploads"
    MAX_UPLOAD_MB: int = 20
    ALLOWED_EXTENSIONS: set[str] = {".pdf", ".docx", ".txt", ".md"}

    SUMMARY_CHUNKS: int = 16 


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
