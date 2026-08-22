from functools import lru_cache
from typing import List, Union
import json
from pydantic import field_validator
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
        "https://unfoldr-ai.vercel.app",
        "https://unfoldr-kappa.vercel.app",
        "https://unfoldr.vercel.app",
    ]

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            v_str = v.strip()
            if v_str.startswith("[") and v_str.endswith("]"):
                try:
                    return json.loads(v_str)
                except Exception:
                    pass
            return [i.strip() for i in v_str.split(",") if i.strip()]
        return v

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