from app.db.base import Base
from app.db.session import engine
from app.models.repository import Repository
def init_db(): 
    Base.metadata.create_all(bind=engine)