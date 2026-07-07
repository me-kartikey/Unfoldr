import json

from sqlalchemy.orm import Session

from app.models.repository_architecture import RepositoryArchitecture
from app.schemas.repository_architecture import (
    RepositoryArchitectureCreate
)


class RepositoryArchitectureRepository:

    @staticmethod
    def create(
        db: Session,
        architecture_data: RepositoryArchitectureCreate
    ) -> RepositoryArchitecture:

        architecture = RepositoryArchitecture(
            repository_id=architecture_data.repository_id,
            project_type=architecture_data.project_type,
            entry_points=json.dumps(
                architecture_data.entry_points
            ),
            root_folders=json.dumps(
                architecture_data.root_folders
            ),
            config_files=json.dumps(
                architecture_data.config_files
            )
        )

        db.add(architecture)
        db.commit()
        db.refresh(architecture)

        return architecture