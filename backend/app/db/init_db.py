from app.db.base import Base
from app.db.session import engine
from app.models.user import User
from app.models.repository import Repository
from app.models.repository_analysis import RepositoryAnalysis
from app.models.repository_dependency import RepositoryDependency
from app.models.repository_architecture import RepositoryArchitecture

def init_db(): 
    # Added on 13-08-2026: Drop all tables and recreate them to start with a clean test state and initialize auth schemas.
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)