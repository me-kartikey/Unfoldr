from sqlalchemy.orm import Session

from app.models.repository_dependency import RepositoryDependency
from app.repositories.repository_dependency_repository import (
    RepositoryDependencyRepository
)
from app.schemas.repository_dependency import (
    RepositoryDependencyCreate
)


class RepositoryDependencyService:

    @staticmethod
    def create_dependency(
        db: Session,
        dependency_data: RepositoryDependencyCreate
    ) -> RepositoryDependency:

        return RepositoryDependencyRepository.create(
            db=db,
            dependency_data=dependency_data
        )

    @staticmethod
    def get_repository_dependencies(
        db: Session,
        repository_id: str
    ):

        return RepositoryDependencyRepository.get_by_repository(
            db=db,
            repository_id=repository_id
        )