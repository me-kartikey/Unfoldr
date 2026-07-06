from sqlalchemy.orm import Session

from app.models.repository_dependency import RepositoryDependency
from app.schemas.repository_dependency import (
    RepositoryDependencyCreate
)


class RepositoryDependencyRepository:

    @staticmethod
    def create(
        db: Session,
        dependency_data_create: RepositoryDependencyCreate
    ) -> RepositoryDependency:

        dependency = RepositoryDependency(
            repository_id=dependency_data_create.repository_id,
            name=dependency_data_create.name,
            version=dependency_data_create.version,
            language=dependency_data_create.language,
            package_manager=dependency_data_create.package_manager,
            dependency_type=dependency_data_create.dependency_type
        )

        db.add(dependency)
        db.commit()
        db.refresh(dependency)

        return dependency

    @staticmethod
    def get_by_repository(
        db: Session,
        repository_id: str
    ) -> list[RepositoryDependency]:

        return (
            db.query(RepositoryDependency)
            .filter(
                RepositoryDependency.repository_id == repository_id
            )
            .all()
        )