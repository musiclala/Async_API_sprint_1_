from elasticsearch import AsyncElasticsearch

from src.core.config import settings

es: AsyncElasticsearch | None = None


async def get_elastic() -> AsyncElasticsearch:
    return es


async def init_elastic() -> None:
    global es
    es = AsyncElasticsearch(hosts=[settings.elastic_host])


async def close_elastic() -> None:
    global es
    if es is not None:
        await es.close()
        es = None