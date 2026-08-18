from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str
    environment: str
    debug: bool

    database_url: str

    upload_dir: str

    google_api_key: str

    # Added on 13-08-2026: JWT secret key, signature algorithm, and default expiration duration for cookie sessions
    jwt_secret_key: str = "30825ad7c6f059cbda42df35e69bf8841a153bdcf18db1a3d3c8aef9f3a61f03"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

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