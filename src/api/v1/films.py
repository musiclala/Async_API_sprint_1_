from __future__ import annotations

from uuid import UUID

from elasticsearch import NotFoundError
from fastapi import APIRouter, Depends, HTTPException, Query

from src.api.deps import get_film_service
from src.api.v1.params import FilmListParams, Pagination, films_list_params, pagination_params
from src.models.film import Film, FilmShort
from src.services.films import FilmService

router = APIRouter()


@router.get(
    "",
    response_model=list[FilmShort],
    summary="Список фильмов",
    description="Возвращает список фильмов с пагинацией, сортировкой и фильтрацией по жанру.",
)
async def films_list(
    pag: Pagination = Depends(pagination_params),
    params: FilmListParams = Depends(films_list_params),
    service: FilmService = Depends(get_film_service),
) -> list[FilmShort]:
    try:
        return await service.list(
            page_number=pag.page_number,
            page_size=pag.page_size,
            sort=params.sort,
            genre=params.genre,
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except NotFoundError:
        raise HTTPException(status_code=503, detail="Search index is not ready")


@router.get(
    "/search",
    response_model=list[FilmShort],
    summary="Поиск фильмов",
    description="Поиск по названию/описанию. Поддерживает пагинацию.",
)
async def films_search(
    query: str = Query(..., min_length=1),
    pag: Pagination = Depends(pagination_params),
    service: FilmService = Depends(get_film_service),
) -> list[FilmShort]:
    try:
        return await service.search(query=query, page_number=pag.page_number, page_size=pag.page_size)
    except NotFoundError:
        raise HTTPException(status_code=503, detail="Search index is not ready")


@router.get(
    "/{film_id}",
    response_model=Film,
    summary="Детали фильма",
    description="Возвращает полную информацию о фильме по UUID.",
)
async def film_details(
    film_id: UUID,
    service: FilmService = Depends(get_film_service),
) -> Film:
    try:
        return await service.get_by_id(film_id)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="film not found")