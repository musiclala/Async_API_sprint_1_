from functools import lru_cache

from elasticsearch import AsyncElasticsearch
from redis.asyncio import Redis

from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.services.films import FilmService
from fastapi import Depends

from src.storage.elastic import ElasticFilmRepository
from src.storage.redis_cache import RedisCacheRepository


def get_film_service(
    es: AsyncElasticsearch = Depends(get_elastic),
    redis: Redis = Depends(get_redis),
) -> FilmService:
    storage = ElasticFilmRepository(es)
    cache = RedisCacheRepository(redis)
    return FilmService(storage=storage, cache=cache)