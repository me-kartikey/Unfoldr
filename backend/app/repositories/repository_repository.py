from sqlalchemy.orm import Session

from app.models.repository import Repository
from app.schemas.repository import RepositoryCreate
from sqlalchemy import select


class RepositoryRepository:
#for posting data insde the database
    @staticmethod
    def create(
        db: Session,
        repository_data: RepositoryCreate,
        user_id: str
    ) -> Repository:
        # Edited on 13-08-2026: Associate repository with the creating user_id
        repository = Repository(
            name=repository_data.name,
            original_name=repository_data.original_name,
            storage_path=repository_data.storage_path,
            user_id=user_id
        )

        db.add(repository)

        db.commit()

        db.refresh(repository)

        return repository
    
    # for getting all the data from the database for a specific user
    @staticmethod
    def get_all_by_user(db: Session, user_id: str):
        # Edited on 13-08-2026: Query repositories filtered by owner user_id
        statement = select(Repository).where(Repository.user_id == user_id)
        result=db.execute(statement)
        return result.scalars().all()
    
    @staticmethod
    def get_by_id(
        db: Session,
        repository_id: str
    ):
    
        return (
            db.query(Repository)
            .filter(
                Repository.id == repository_id
            )
         .first()
    )
    
    