from elasticsearch import AsyncElasticsearch

from src.core.config import ELASTIC_HOST

es: AsyncElasticsearch | None = None


async def get_elastic() -> AsyncElasticsearch:
    return es


async def init_elastic() -> None:
    global es
    es = AsyncElasticsearch(hosts=[ELASTIC_HOST])


async def close_elastic() -> None:
    global es
    if es is not None:
        await es.close()
        es = None