from __future__ import annotations

from uuid import UUID
from typing import Optional

from elasticsearch import AsyncElasticsearch

from src.core.config import settings
from src.storage.base import AbstractFilmStorage


def build_sort(sort: Optional[str]) -> list[dict]:
    if not sort:
        return [{"imdb_rating": {"order": "desc"}}]

    order = "asc"
    field = sort
    if sort.startswith("-"):
        order = "desc"
        field = sort[1:]

    if field not in {"imdb_rating", "title"}:
        raise ValueError(f"Unsupported sort field: {field}")

    return [{field: {"order": order}}]


class ElasticFilmRepository(AbstractFilmStorage):
    def __init__(self, es: AsyncElasticsearch):
        self.es = es
        self.index = settings.elastic_index

    async def get_by_id(self, film_id: UUID) -> dict:
        doc = await self.es.get(index=self.index, id=str(film_id))
        src = doc.get("_source") or {}
        src["id"] = doc.get("_id", str(film_id))
        return src

    async def search(self, query: str, page_number: int, page_size: int) -> list[dict]:
        body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["title^3", "description"],
                    "fuzziness": "AUTO",
                }
            },
            "_source": ["title", "imdb_rating"],
            "from": (page_number - 1) * page_size,
            "size": page_size,
        }
        resp = await self.es.search(index=self.index, body=body)
        hits = resp.get("hits", {}).get("hits", [])

        out: list[dict] = []
        for h in hits:
            src = h.get("_source") or {}
            src["id"] = h.get("_id")
            out.append(src)
        return out

    async def list(
        self,
        page_number: int,
        page_size: int,
        sort: Optional[str] = None,
        genre: Optional[UUID] = None,
    ) -> list[dict]:
        query = {"term": {"genre.id": str(genre)}} if genre else {"match_all": {}}

        body = {
            "query": query,
            "sort": build_sort(sort),
            "_source": ["title", "imdb_rating"],
            "from": (page_number - 1) * page_size,
            "size": page_size,
        }

        resp = await self.es.search(index=self.index, body=body)
        hits = resp.get("hits", {}).get("hits", [])

        out: list[dict] = []
        for h in hits:
            src = h.get("_source") or {}
            src["id"] = h.get("_id")
            out.append(src)
        return out