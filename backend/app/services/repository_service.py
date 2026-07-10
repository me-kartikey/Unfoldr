from pathlib import Path

from sqlalchemy.orm import Session

from app.analyzers.architecture_analyzer import ArchitectureAnalyzer
from app.analyzers.dependency_analyzer import DependencyAnalyzer
from app.analyzers.repository_analyzer import RepositoryAnalyzer

from app.models.repository import Repository

from app.repositories.repository_repository import RepositoryRepository

from app.schemas.repository import RepositoryCreate
from app.schemas.repository_analysis import RepositoryAnalysisCreate
from app.schemas.repository_architecture import RepositoryArchitectureCreate
from app.schemas.repository_dependency import RepositoryDependencyCreate

from app.services.repository_analysis_service import (
    RepositoryAnalysisService,
)
from app.services.repository_architecture_service import (
    RepositoryArchitectureService,
)
from app.services.repository_dependency_service import (
    RepositoryDependencyService,
)


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
        file_name: str,
        repository_path: Path
    ):

        repository_name = file_name.removesuffix(".zip")

        repository_data = RepositoryCreate(
            name=repository_name,
            original_name=file_name,
            storage_path=str(repository_path)
        )

        repository = RepositoryRepository.create(
            db=db,
            repository_data=repository_data
        )

        extracted_path = repository_path / "extracted"

        repository_root = next(
            item
            for item in extracted_path.iterdir()
            if item.is_dir()
        )

        # Repository Analysis
        analysis = RepositoryAnalyzer.analyze_repository(
            repository_root
        )

        repository_analysis = RepositoryAnalysisCreate(
            repository_id=repository.id,
            total_files=analysis["total_files"],
            extensions=analysis["extensions"],
            languages=analysis["languages"],
            frameworks=analysis["frameworks"],
            libraries=analysis["libraries"]
        )

        print(f"Repository analysis data: {repository_analysis}")

        RepositoryAnalysisService.create_analysis(
            db=db,
            repository_analysis=repository_analysis
        )

        # Dependency Analysis
        dependencies = DependencyAnalyzer.detect_dependencies(
            repository_root
        )

        print("Dependency found:", dependencies)

        for dependency in dependencies:

            print("Saving dependency:", dependency)

            repository_dependency = RepositoryDependencyCreate(
                repository_id=repository.id,
                name=dependency["name"],
                version=dependency["version"],
                language=dependency["language"],
                package_manager=dependency["package_manager"],
                dependency_type=dependency["dependency_type"]
            )

            RepositoryDependencyService.create_dependency(
                db=db,
                dependency_data=repository_dependency
            )

        # Architecture Analysis
        architecture = ArchitectureAnalyzer.analyze_repository(
            repository_root
        )

        print(f"Architecture: {architecture}")

        repository_architecture = RepositoryArchitectureCreate(
            repository_id=repository.id,
            project_type=architecture["project_type"],
            entry_points=architecture["entry_points"],
            architecture_pattern=architecture["architecture_pattern"],
            root_folders=architecture["root_folders"],
            config_files=architecture["config_files"]
        )

        RepositoryArchitectureService.create_architecture(
            db=db,
            architecture_data=repository_architecture
        )

        return repository