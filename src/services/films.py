from __future__ import annotations

from uuid import UUID
from elasticsearch import NotFoundError

from src.models.film import Film, FilmShort
from src.storage.base import AbstractFilmStorage
from src.storage.cache_base import AbstractCache


class FilmService:
    def __init__(
            self,
            storage: AbstractFilmStorage,
            cache: AbstractCache,
    ):
        self.storage = storage
        self.cache = cache

    async def get_by_id(self, film_id: UUID) -> Film:
        key = self.cache.make_key("films:detail", film_id)

        cached = await self.cache.get(key)
        if cached:
            return Film.model_validate(cached)

        try:
            src = await self.storage.get_by_id(film_id)
        except NotFoundError:
            raise

        film = Film.model_validate(src)
        await self.cache.set(key, film.model_dump(by_alias=True))
        return film

    async def search(
        self,
        query: str,
        page_number: int,
        page_size: int,
    ) -> list[FilmShort]:
        key = self.cache.make_key(
            "films:search", query, f"p{page_number}", f"s{page_size}"
        )

        cached = await self.cache.get(key)
        if cached:
            return [FilmShort.model_validate(x) for x in cached]

        items_src = await self.storage.search(
            query=query,
            page_number=page_number,
            page_size=page_size,
        )
        items = [FilmShort.model_validate(x) for x in items_src]

        await self.cache.set(
            key,
            [x.model_dump(by_alias=True) for x in items],
        )
        return items

    async def list(
        self,
        page_number: int,
        page_size: int,
        sort: str | None = None,
        genre: UUID | None = None,
    ) -> list[FilmShort]:
        key = self.cache.make_key(
            "films:list",
            f"genre{genre or '_'}",
            f"sort{sort or '_'}",
            f"p{page_number}",
            f"s{page_size}",
        )

        cached = await self.cache.get(key)
        if cached:
            return [FilmShort.model_validate(x) for x in cached]

        items_src = await self.storage.list(
            page_number=page_number,
            page_size=page_size,
            sort=sort,
            genre=genre,
        )
        items = [FilmShort.model_validate(x) for x in items_src]

        await self.cache.set(
            key,
            [x.model_dump(by_alias=True) for x in items],
        )
        return items