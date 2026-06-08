from sqlalchemy.orm import Session

from app.models.repository import Repository
from app.schemas.repository import RepositoryCreate


class RepositoryRepository:

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