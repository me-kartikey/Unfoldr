from pathlib import Path
import time

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

from app.generator.documents_generator import DocumentsGenerator

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

        analysis_record = RepositoryAnalysisService.create_analysis(
            db=db,
            repository_analysis=repository_analysis
        )

        # Dependency Analysis
        start_dep_analysis = time.perf_counter()  # added to check timing
        dependencies = DependencyAnalyzer.detect_dependencies(
            repository_root
        )
        dep_analysis_time = time.perf_counter() - start_dep_analysis  # added to check timing
        print(f"Dependency Analysis: {dep_analysis_time:.3f}s")

        print("Dependency found:", dependencies)

        # Saving Dependencies
        start_dep_save = time.perf_counter()  # added to check timing
        for dependency in dependencies:

            # print("Saving dependency:", dependency)

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
        dep_save_time = time.perf_counter() - start_dep_save  # added to check timing
        print(f"Dependency Save: {dep_save_time:.3f}s")
        
        repository_dependencies = (
            RepositoryDependencyService.get_repository_dependencies(
                db=db,
                repository_id=repository.id
                )
        )

        # Architecture Analysis
        start_arch_analysis = time.perf_counter()  # added to check timing
        architecture = ArchitectureAnalyzer.analyze_repository(
            repository_root
        )
        arch_analysis_time = time.perf_counter() - start_arch_analysis  # added to check timing
        print(f"Architecture Analysis: {arch_analysis_time:.3f}s")

        print(f"Architecture: {architecture}")

        # Saving Architecture
        start_arch_save = time.perf_counter()  # added to check timing
        repository_architecture = RepositoryArchitectureCreate(
            repository_id=repository.id,
            project_type=architecture["project_type"],
            backend_framework=architecture["backend_framework"],
            frontend_framework=architecture["frontend_framework"],
            architecture_pattern=architecture["architecture_pattern"],
            entry_points=architecture["entry_points"],
            root_folders=architecture["root_folders"],
            config_files=architecture["config_files"],
            databases=architecture["databases"],
            orms=architecture["orms"],
            authentication_methods=architecture["authentication_methods"],
            api_styles=architecture["api_styles"],
            devops_tools=architecture["devops"],
            cicd_tools=architecture["cicd"],
            testing_frameworks=architecture["testing"],
            code_quality_tools=architecture["code_quality"],
            environment_files=architecture["environment"],
            deployment_platforms=architecture["deployment"],
            repository_characteristics=architecture["repository_characteristics"]
        )

        architecture_record = RepositoryArchitectureService.create_architecture(
            db=db,
            architecture_data=repository_architecture
        )
        arch_save_time = time.perf_counter() - start_arch_save  # added to check timing
        print(f"Architecture Save: {arch_save_time:.3f}s")

        documentation = DocumentsGenerator.generate(
            repository=repository,
            analysis=repository_analysis,
            architecture=repository_architecture,
            dependencies=repository_dependencies,
        )

        DocumentsGenerator.save_documentation(
            output_path=repository_root / "documentation.md",
            content=documentation,
        )

        # Updating Repository Status
        start_status = time.perf_counter()  # added to check timing
        repository.status = "completed"
        db.commit()
        db.refresh(repository)
        status_time = time.perf_counter() - start_status  # added to check timing
        print(f"Updating Repository Status: {status_time:.3f}s")

        return repository