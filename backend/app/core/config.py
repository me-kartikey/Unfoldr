from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str
    environment: str
    debug: bool

    database_url: str
    db_pool_size: int = 10
    db_max_overflow: int = 20

    upload_dir: str
    
    # Upload limits (configurable)
    max_upload_size: int = 104857600  # 100MB
    max_extracted_size: int = 314572800  # 300MB
    max_file_count: int = 20000
    max_individual_file_size: int = 52428800  # 50MB

    google_api_key: str

    # Security
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    csrf_secret_key: str
    allowed_origins: List[str] = [
        "http://localhost",
        "http://localhost:80",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1",
        "http://127.0.0.1:80",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )

    chroma_db_path: str
    chroma_collection_name: str = "repositories"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()