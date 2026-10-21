import logging
from termcolor import colored
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.routing import iter_route_contexts
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, chat, documents, health
from app.core.config import settings
from app.core.logging import setup_logging
from app.db.session import init_db

setup_logging(settings.DEBUG)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.JWT_SECRET == "change-me":
        logger.warning("JWT_SECRET is the default value - set a strong secret in .env")
    settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    init_db()  # creates tables if they don't exist (use Alembic later for migrations)
    yield


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(documents.router)
app.include_router(chat.router)

for route in iter_route_contexts(app.routes):
    print(route.path, route.methods, route.name)
