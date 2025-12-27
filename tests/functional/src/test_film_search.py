import pytest

from settings import settings
from utils.redis_keys import keys_count


@pytest.mark.asyncio
async def test_search_validation_missing_query(aiohttp_session):
    async with aiohttp_session.get(f"{settings.api_url}{settings.films_search_path}") as resp:
        assert resp.status == 422


@pytest.mark.asyncio
async def test_search_validation_empty_query(aiohttp_session):
    async with aiohttp_session.get(
        f"{settings.api_url}{settings.films_search_path}",
        params={"query": ""},
    ) as resp:
        assert resp.status in (422, 400)


@pytest.mark.asyncio
async def test_search_returns_only_n(aiohttp_session):
    async with aiohttp_session.get(
        f"{settings.api_url}{settings.films_search_path}",
        params={"query": "Movie", "page_number": 1, "page_size": 1},
    ) as resp:
        assert resp.status == 200
        data = await resp.json()
        assert len(data) == 1


@pytest.mark.asyncio
async def test_search_by_phrase(aiohttp_session):
    async with aiohttp_session.get(
        f"{settings.api_url}{settings.films_search_path}",
        params={"query": "Alpha", "page_number": 1, "page_size": 10},
    ) as resp:
        assert resp.status == 200
        data = await resp.json()
        assert any(x["title"] == "Alpha Movie" for x in data)


@pytest.mark.asyncio
async def test_search_cache_redis(aiohttp_session, redis_client):
    await redis_client.flushdb()

    params = {"query": "Alpha", "page_number": 1, "page_size": 10}
    before = await keys_count(redis_client, "films:search*")

    async with aiohttp_session.get(f"{settings.api_url}{settings.films_search_path}", params=params) as resp1:
        assert resp1.status == 200
        _ = await resp1.json()

    after_first = await keys_count(redis_client, "films:search*")
    assert after_first > before

    async with aiohttp_session.get(f"{settings.api_url}{settings.films_search_path}", params=params) as resp2:
        assert resp2.status == 200
        _ = await resp2.json()

    after_second = await keys_count(redis_client, "films:search*")
    assert after_second == after_first