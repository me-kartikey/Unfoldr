from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str
    environment: str
    debug: bool

    database_url: str

    upload_dir: str

    google_api_key: str

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )

    chroma_db_path: str = "storage/chroma"
    chroma_collection_name: str = "repositories"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()