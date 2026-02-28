from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    project_name: str = Field("movies-api", alias="PROJECT_NAME")

    redis_host: str = Field(..., alias="REDIS_HOST")
    redis_port: int = Field(6379, alias="REDIS_PORT")
    redis_db: int = Field(0, alias="REDIS_DB")

    elastic_host: str = Field(..., alias="ELASTIC_HOST")
    elastic_port: int = Field(9200, alias="ELASTIC_PORT")
    elastic_index: str = Field("movies", alias="ELASTIC_INDEX")

    @property
    def elastic_url(self) -> str:
        if self.elastic_host.startswith(("http://", "https://")):
            return self.elastic_host
        return f"http://{self.elastic_host}:{self.elastic_port}"

    cache_ttl_seconds: int = Field(300, alias="CACHE_TTL_SECONDS")

    jwt_secret_key: str = Field("", alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field("HS256", alias="JWT_ALGORITHM")


settings = Settings()