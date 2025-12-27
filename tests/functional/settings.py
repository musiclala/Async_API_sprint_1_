from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=None, env_file_encoding="utf-8", extra="ignore")

    api_url: str = Field("http://localhost:8000", alias="API_URL")
    es_url: str = Field("http://localhost:9200", alias="ES_URL")
    redis_host: str = Field("localhost", alias="REDIS_HOST")
    redis_port: int = Field(6379, alias="REDIS_PORT")

    es_movies_index: str = Field("movies", alias="ES_MOVIES_INDEX")

    films_list_path: str = Field("/api/v1/films", alias="FILMS_LIST_PATH")
    films_search_path: str = Field("/api/v1/films/search", alias="FILMS_SEARCH_PATH")
    film_details_path: str = Field("/api/v1/films/{film_id}", alias="FILM_DETAILS_PATH")


settings = Settings()