from uuid import UUID
from pydantic import BaseModel, Field

from src.models.genre import Genre
from src.models.person import Person


class FilmShort(BaseModel):
    uuid: UUID = Field(alias="id")
    title: str
    imdb_rating: float | None = None

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "examples": [
                {"uuid": "b31592e5-673d-46dc-a561-9446438aea0f", "title": "Lunar: The Silver Star", "imdb_rating": 9.2}
            ]
        },
    }


class Film(BaseModel):
    uuid: UUID = Field(alias="id")
    title: str
    imdb_rating: float | None = None
    description: str | None = None

    genre: list[Genre] = []
    actors: list[Person] = []
    writers: list[Person] = []
    directors: list[Person] = []

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "examples": [
                {
                    "uuid": "b31592e5-673d-46dc-a561-9446438aea0f",
                    "title": "Lunar: The Silver Star",
                    "imdb_rating": 9.2,
                    "description": "From the village of Burg...",
                    "genre": [{"uuid": "7ac3cb3b-972d-4004-9e42-ff147ede7463", "name": "Comedy"}],
                    "actors": [{"uuid": "afbdbaca-04e2-44ca-8bef-da1ae4d84cdf", "full_name": "Ashley Parker Angel"}],
                    "writers": [],
                    "directors": [],
                }
            ]
        },
    }