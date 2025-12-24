from functools import lru_cache

from elasticsearch import AsyncElasticsearch
from redis.asyncio import Redis

from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.services.films import FilmService


@lru_cache()
def get_film_service_cached(es: AsyncElasticsearch, redis: Redis) -> FilmService:
    return FilmService(es=es, redis=redis)


async def get_film_service() -> FilmService:
    es = await get_elastic()
    redis = await get_redis()
    return get_film_service_cached(es, redis)