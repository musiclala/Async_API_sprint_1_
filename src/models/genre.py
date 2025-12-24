from uuid import UUID
from pydantic import BaseModel, Field


class Genre(BaseModel):
    uuid: UUID = Field(alias="id")
    name: str

    model_config = {"populate_by_name": True}