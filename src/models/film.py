from uuid import UUID
from pydantic import BaseModel, Field

from src.models.genre import Genre
from src.models.person import Person


class FilmShort(BaseModel):
    uuid: UUID = Field(alias="id")
    title: str
    imdb_rating: float | None = None

    model_config = {"populate_by_name": True}


class Film(BaseModel):
    uuid: UUID = Field(alias="id")
    title: str
    imdb_rating: float | None = None
    description: str = None

    genre: list[Genre] = Field(default_factory=list)
    actors: list[Person] = Field(default_factory=list)
    writers: list[Person] = Field(default_factory=list)
    directors: list[Person] = Field(default_factory=list)

    model_config = {"populate_by_name": True}