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
            backend_framework=architecture_data.backend_framework,
            frontend_framework=architecture_data.frontend_framework,
            architecture_pattern=architecture_data.architecture_pattern,
            entry_points=architecture_data.entry_points,
            root_folders=architecture_data.root_folders,
            config_files=architecture_data.config_files,
            databases=architecture_data.databases,
            orms=architecture_data.orms,
            authentication_methods=architecture_data.authentication_methods,
            api_styles=architecture_data.api_styles,
            devops_tools=architecture_data.devops_tools,
            cicd_tools=architecture_data.cicd_tools,
            testing_frameworks=architecture_data.testing_frameworks,
            code_quality_tools=architecture_data.code_quality_tools,
            environment_files=architecture_data.environment_files,
            deployment_platforms=architecture_data.deployment_platforms,
            repository_characteristics=architecture_data.repository_characteristics
        )

        db.add(architecture)
        db.commit()
        db.refresh(architecture)

        return architecture