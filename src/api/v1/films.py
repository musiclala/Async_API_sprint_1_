from uuid import UUID
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from elasticsearch import NotFoundError

from src.api.deps import get_film_service
from src.models.film import Film, FilmShort
from src.services.films import FilmService

router = APIRouter()


@router.get("", response_model=list[FilmShort])
async def films_list(
    sort: Optional[str] = Query(default="-imdb_rating"),
    genre: Optional[UUID] = Query(default=None),
    page_size: int = Query(default=50, ge=1, le=100),
    page_number: int = Query(default=1, ge=1),
    service: FilmService = Depends(get_film_service),
):
    try:
        return await service.list(
            page_number=page_number,
            page_size=page_size,
            sort=sort,
            genre=genre,
        )
    except NotFoundError:
        return []  # индекс ещё не создан
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.get("/search", response_model=list[FilmShort])
async def films_search(
    query: str = Query(..., min_length=1),
    page_size: int = Query(default=50, ge=1, le=100),
    page_number: int = Query(default=1, ge=1),
    service: FilmService = Depends(get_film_service),
):
    return await service.search(query=query, page_number=page_number, page_size=page_size)


@router.get("/{film_id}", response_model=Film)
async def film_details(
    film_id: UUID,
    service: FilmService = Depends(get_film_service),
):
    try:
        return await service.get_by_id(film_id)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="film not found")