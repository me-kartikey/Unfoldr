from app.db.base import Base
from app.db.session import engine
from app.models.repository import Repository
from app.models.repository_analysis import RepositoryAnalysis
from app.models.repository_dependency import RepositoryDependency
from app.models.repository_architecture import RepositoryArchitecture

def init_db(): 
    Base.metadata.create_all(bind=engine)