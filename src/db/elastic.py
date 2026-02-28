from elasticsearch import AsyncElasticsearch

from src.core.backoff import expo_backoff
from src.core.config import settings

es: AsyncElasticsearch | None = None


async def get_elastic() -> AsyncElasticsearch:
    return es


@expo_backoff(exceptions=(Exception,), start_sleep_time=0.2, max_retries=7)
async def init_elastic() -> None:
    global es
    es = AsyncElasticsearch(hosts=[settings.elastic_url])
    await es.info()


async def close_elastic() -> None:
    global es
    if es is not None:
        await es.close()
        es = None