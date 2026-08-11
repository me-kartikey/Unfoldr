from sqlalchemy.orm import Session

from app.models.repository_architecture import (
    RepositoryArchitecture
)
from app.repositories.repository_architecture_repository import (
    RepositoryArchitectureRepository
)
from app.schemas.repository_architecture import (
    RepositoryArchitectureCreate
)


class RepositoryArchitectureService:

    @staticmethod
    def create_architecture(
        db: Session,
        architecture_data: RepositoryArchitectureCreate
    ) -> RepositoryArchitecture:

        return RepositoryArchitectureRepository.create(
            db=db,
            architecture_data=architecture_data
        )

    @staticmethod
    def get_architecture(
        db: Session,
        repository_id: str
    ) -> RepositoryArchitecture | None:
        return RepositoryArchitectureRepository.get_by_repository_id(
            db=db,
            repository_id=repository_id
        )