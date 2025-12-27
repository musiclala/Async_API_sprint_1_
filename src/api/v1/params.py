from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from fastapi import Query

@dataclass(frozen=True)
class Pagination:
    page_number: int
    page_size: int


def pagination_params(
    page_number: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=100),
) -> Pagination:
    return Pagination(page_number=page_number, page_size=page_size)


@dataclass(frozen=True)
class FilmListParams:
    sort: str | None
    genre: UUID | None


def films_list_params(
    sort: str | None = Query(default="-imdb_rating"),
    genre: UUID | None = Query(default=None),
) -> FilmListParams:
    return FilmListParams(sort=sort, genre=genre)