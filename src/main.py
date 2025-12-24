from fastapi import FastAPI

from src.api.v1 import films
from src.core import config
from src.db import elastic, redis

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
)

@app.on_event("startup")
async def startup():
    await elastic.init_elastic()
    await redis.init_redis()

@app.on_event("shutdown")
async def shutdown():
    await redis.close_redis()
    await elastic.close_elastic()


app.include_router(films.router, prefix="/api/v1/films", tags=["films"])
