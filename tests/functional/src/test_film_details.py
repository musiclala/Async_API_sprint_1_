import pytest

from settings import settings
from utils.redis_keys import keys_count

import pytest

pytestmark = pytest.mark.asyncio

async def test_film_details_validation_bad_uuid(aiohttp_session):
    url = f"{settings.api_url}{settings.film_details_path.format(film_id='not-a-uuid')}"
    async with aiohttp_session.get(url) as resp:
        assert resp.status == 422


async def test_film_details_found(aiohttp_session):
    film_id = "11111111-1111-1111-1111-111111111111"
    url = f"{settings.api_url}{settings.film_details_path.format(film_id=film_id)}"
    async with aiohttp_session.get(url) as resp:
        assert resp.status == 200
        data = await resp.json()
        assert data["uuid"] == film_id
        assert data["title"] == "Zeta Movie"


async def test_film_details_not_found(aiohttp_session):
    film_id = "00000000-0000-0000-0000-000000000000"
    url = f"{settings.api_url}{settings.film_details_path.format(film_id=film_id)}"
    async with aiohttp_session.get(url) as resp:
        assert resp.status == 404


async def test_film_details_cache_redis(aiohttp_session, redis_client):
    await redis_client.flushdb()

    film_id = "11111111-1111-1111-1111-111111111111"
    url = f"{settings.api_url}{settings.film_details_path.format(film_id=film_id)}"

    before = await keys_count(redis_client, "films:detail*")

    async with aiohttp_session.get(url) as resp1:
        assert resp1.status == 200
        _ = await resp1.json()

    after_first = await keys_count(redis_client, "films:detail*")
    assert after_first > before

    async with aiohttp_session.get(url) as resp2:
        assert resp2.status == 200
        _ = await resp2.json()

    after_second = await keys_count(redis_client, "films:detail*")
    assert after_second == after_first