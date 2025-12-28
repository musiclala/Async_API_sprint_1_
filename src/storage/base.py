from __future__ import annotations

import abc
from uuid import UUID


class AbstractFilmStorage(abc.ABC):
    @abc.abstractmethod
    async def get_by_id(self, film_id: UUID) -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    async def search(
        self,
        query: str,
        page_number: int,
        page_size: int,
    ) -> list[dict]:
        raise NotImplementedError

    @abc.abstractmethod
    async def list(
        self,
        page_number: int,
        page_size: int,
        sort: str | None = None,
        genre: UUID | None = None,
    ) -> list[dict]:
        raise NotImplementedError