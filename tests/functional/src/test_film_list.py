import pytest

from settings import settings

import pytest

pytestmark = pytest.mark.asyncio


async def test_films_list_validation_page_size_too_big(aiohttp_session):
    async with aiohttp_session.get(
        f"{settings.api_url}{settings.films_list_path}",
        params={"page_number": 1, "page_size": 1000},
    ) as resp:
        assert resp.status == 422


async def test_films_list_returns_all(aiohttp_session):
    async with aiohttp_session.get(
        f"{settings.api_url}{settings.films_list_path}",
        params={"page_number": 1, "page_size": 10, "sort": "-imdb_rating"},
    ) as resp:
        assert resp.status == 200
        data = await resp.json()
        assert isinstance(data, list)
        assert len(data) >= 2
        assert {"uuid", "title", "imdb_rating"} <= set(data[0].keys())


async def test_films_list_returns_only_n(aiohttp_session):
    async with aiohttp_session.get(
        f"{settings.api_url}{settings.films_list_path}",
        params={"page_number": 1, "page_size": 1, "sort": "-imdb_rating"},
    ) as resp:
        assert resp.status == 200
        data = await resp.json()
        assert len(data) == 1