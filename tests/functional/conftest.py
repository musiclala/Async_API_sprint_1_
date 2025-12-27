import aiohttp
import pytest_asyncio
import redis.asyncio as redis
from elasticsearch import AsyncElasticsearch

from settings import settings
from utils.wait_for import wait_all
from utils.ES_seed import recreate_index, seed_docs


@pytest_asyncio.fixture(scope="session")
async def es_client():
    client = AsyncElasticsearch(hosts=[settings.es_url])
    try:
        yield client
    finally:
        await client.close()


@pytest_asyncio.fixture
async def redis_client():
    client = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0)
    try:
        yield client
    finally:
        await client.aclose()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_infra(es_client: AsyncElasticsearch):
    await wait_all(settings.es_url, settings.redis_host, settings.redis_port, settings.api_url)

    r = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0)
    try:
        await r.flushdb()
    finally:
        await r.aclose()

    await recreate_index(es_client, settings.es_movies_index, "testdata/es_movies_index.json")
    await seed_docs(es_client, settings.es_movies_index, "testdata/movies.json")


@pytest_asyncio.fixture
async def aiohttp_session():
    timeout = aiohttp.ClientTimeout(total=5)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        yield session