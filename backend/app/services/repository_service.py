from sqlalchemy.orm import Session

from app.models.repository import Repository
from app.repositories.repository_repository import RepositoryRepository
from app.schemas.repository import RepositoryCreate


class RepositoryService:

    @staticmethod
    def create_repository(
        db: Session,
        repository_data: RepositoryCreate
    ) -> Repository:

        return RepositoryRepository.create(
            db=db,
            repository_data=repository_data
        )
    
    @staticmethod
    def get_repositories(db: Session):
       
        return RepositoryRepository.get_all(db) 
    
    @staticmethod
    def get_repository(
        db: Session,
        repository_id: str
    ):

        return RepositoryRepository.get_by_id(
            db=db,
            repository_id=repository_id
        )
    @staticmethod
    def create_uploaded_repository(
        db: Session,
        repository_id: str,
        file_name: str,
        repository_path: str
    ):
        repository_name= file_name.removesuffix(".zip")
        repository_data=RepositoryCreate(
            name=repository_name,
            original_name=file_name,
            storage_path=repository_path
        )
        return RepositoryRepository.create(db=db, repository_data=repository_data)
