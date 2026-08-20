from sqlalchemy import create_engine
from sqlalchemy.orm import Session,sessionmaker
from app.core.config import settings
engine = create_engine(
    settings.database_url,
    echo=False if settings.environment != "development" else settings.debug,
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
    pool_pre_ping=True
)
session_local = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
    )
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()