from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.v1 import films
from src.db import elastic, redis
from src.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await elastic.init_elastic()
    await redis.init_redis()
    yield
    await redis.close_redis()
    await elastic.close_elastic()


app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

app.include_router(films.router, prefix="/api/v1/films", tags=["films"])