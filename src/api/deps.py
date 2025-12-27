from functools import lru_cache

from elasticsearch import AsyncElasticsearch
from redis.asyncio import Redis

from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.services.films import FilmService
from fastapi import Depends

from src.storage.elastic import ElasticFilmRepository
from src.storage.redis_cache import RedisCacheRepository


async def get_film_service(
    es=Depends(get_elastic),
    redis=Depends(get_redis),
) -> FilmService:
    repo = ElasticFilmRepository(es)
    cache = RedisCacheRepository(redis)
    return FilmService(repo=repo, cache=cache)