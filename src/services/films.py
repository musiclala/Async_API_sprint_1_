from __future__ import annotations

from uuid import UUID

import orjson
from elasticsearch import AsyncElasticsearch
from redis.asyncio import Redis

from src.core.config import settings
from src.models.film import Film, FilmShort


def _cache_key(prefix: str, *parts: str) -> str:
    safe = ":".join(p.replace(":", "_") for p in parts)
    return f"{prefix}:{safe}"


def _build_sort(sort: str | None) -> list[dict]:
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


class FilmService:
    def __init__(self, es: AsyncElasticsearch, redis: Redis):
        self.es = es
        self.redis = redis
        self.index = settings.elastic_index
        self.ttl = settings.cache_ttl_seconds

    async def get_by_id(self, film_id: UUID) -> Film:
        key = _cache_key("films:detail", str(film_id))

        try:
            cached = await self.redis.get(key)
        except Exception:
            cached = None

        if cached:
            return Film.model_validate(orjson.loads(cached))

        doc = await self.es.get(index=self.index, id=str(film_id))
        src = doc.get("_source") or {}
        src["id"] = doc.get("_id", str(film_id))

        film = Film.model_validate(src)

        try:
            await self.redis.setex(key, self.ttl, orjson.dumps(film.model_dump(by_alias=True)))
        except Exception:
            pass

        return film

    async def search(self, query: str, page_number: int, page_size: int) -> list[FilmShort]:
        key = _cache_key("films:search", query.strip(), f"p{page_number}", f"s{page_size}")

        try:
            cached = await self.redis.get(key)
        except Exception:
            cached = None

        if cached:
            data = orjson.loads(cached)
            return [FilmShort.model_validate(x) for x in data]

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

        items: list[FilmShort] = []
        for h in hits:
            src = h.get("_source") or {}
            src["id"] = h.get("_id")
            items.append(FilmShort.model_validate(src))

        try:
            await self.redis.setex(
                key,
                self.ttl,
                orjson.dumps([x.model_dump(by_alias=True) for x in items]),
            )
        except Exception:
            pass

        return items

    async def list(
        self,
        page_number: int,
        page_size: int,
        sort: str | None = None,
        genre: UUID | None = None,
    ) -> list[FilmShort]:
        sort_es = _build_sort(sort)

        key = _cache_key(
            "films:list",
            f"genre{genre or '_'}",
            f"sort{sort or '_'}",
            f"p{page_number}",
            f"s{page_size}",
        )

        try:
            cached = await self.redis.get(key)
        except Exception:
            cached = None

        if cached:
            data = orjson.loads(cached)
            return [FilmShort.model_validate(x) for x in data]

        if genre:
            query = {"term": {"genre.id": str(genre)}}
        else:
            query = {"match_all": {}}

        body = {
            "query": query,
            "sort": sort_es,
            "_source": ["title", "imdb_rating"],
            "from": (page_number - 1) * page_size,
            "size": page_size,
        }

        resp = await self.es.search(index=self.index, body=body)
        hits = resp.get("hits", {}).get("hits", [])

        items: list[FilmShort] = []
        for h in hits:
            src = h.get("_source") or {}
            src["id"] = h.get("_id")
            items.append(FilmShort.model_validate(src))

        try:
            await self.redis.setex(
                key,
                self.ttl,
                orjson.dumps([x.model_dump(by_alias=True) for x in items]),
            )
        except Exception:
            pass

        return items