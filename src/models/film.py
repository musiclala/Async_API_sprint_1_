from uuid import UUID
from typing import List, Optional
from pydantic import BaseModel, Field

from src.models.genre import Genre
from src.models.person import Person


class FilmShort(BaseModel):
    uuid: UUID = Field(alias="id")
    title: str
    imdb_rating: Optional[float] = None

    model_config = {"populate_by_name": True}


class Film(BaseModel):
    uuid: UUID = Field(alias="id")
    title: str
    imdb_rating: Optional[float] = None
    description: Optional[str] = None

    genre: List[Genre] = []
    actors: List[Person] = []
    writers: List[Person] = []
    directors: List[Person] = []

    model_config = {"populate_by_name": True}