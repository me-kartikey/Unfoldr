from sqlalchemy import create_engine
from sqlalchemy.orm import Session,sessionmaker
from app.core.config import settings
db_url = settings.database_url
if db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+psycopg://", 1)

engine = create_engine(
    db_url,
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