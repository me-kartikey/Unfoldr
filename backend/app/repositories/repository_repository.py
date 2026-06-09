from sqlalchemy.orm import Session

from app.models.repository import Repository
from app.schemas.repository import RepositoryCreate
from sqlalchemy import select


class RepositoryRepository:
#for posting data insde the database
    @staticmethod
    def create(
        db: Session,
        repository_data: RepositoryCreate
    ) -> Repository:

        repository = Repository(
            name=repository_data.name,
            original_name=repository_data.original_name,
            storage_path=repository_data.storage_path
        )

        db.add(repository)

        db.commit()

        db.refresh(repository)

        return repository
    
    # for getting all the data from the database
    @staticmethod
    def get_all(db: Session):
        statement = select(Repository)
        result=db.execute(statement)
        return result.scalars().all()