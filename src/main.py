from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.v1 import films, auth as auth_api
from src.db import elastic, redis
from src.core.config import settings
from src.middleware import RequestIdMiddleware
from fastapi.responses import ORJSONResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    await elastic.init_elastic()
    await redis.init_redis()
    yield
    await redis.close_redis()
    await elastic.close_elastic()

app = FastAPI(
    title=settings.project_name,
    description=(
        "Асинхронный API онлайн-кинотеатра.\n\n"
        "В текущей итерации реализованы эндпоинты для фильмов: список, поиск, детали."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    default_response_class=ORJSONResponse,
    contact={
        "name": "Support",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT",
    },
    lifespan=lifespan,
)

app.add_middleware(RequestIdMiddleware)
app.include_router(auth_api.router, prefix="/api/v1", tags=["auth"])
app.include_router(films.router, prefix="/api/v1/films", tags=["films"])