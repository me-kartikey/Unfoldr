from pathlib import Path
import time

from app.services.chunking_service import ChunkingService
from app.services.embedding_service import EmbeddingService
from app.services.vector_store_service import VectorStoreService

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
        repository_data: RepositoryCreate,
        user_id: str
    ) -> Repository:
        # Edited on 13-08-2026: Set owner user_id when creating new repository
        return RepositoryRepository.create(
            db=db,
            repository_data=repository_data,
            user_id=user_id
        )

    @staticmethod
    def get_repositories(db: Session, user_id: str):
        # Edited on 13-08-2026: Fetch only repositories owned by the logged-in user
        return RepositoryRepository.get_all_by_user(db, user_id)

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
    def initialize_uploaded_repository(
        db: Session,
        file_name: str,
        repository_path: Path,
        user_id: str
    ) -> Repository:
        # Edited on 13-08-2026: Initialize new repository bound to uploading user's ID
        repository_name = file_name.removesuffix(".zip")

        repository_data = RepositoryCreate(
            name=repository_name,
            original_name=file_name,
            storage_path=str(repository_path)
        )

        repository = RepositoryRepository.create(
            db=db,
            repository_data=repository_data,
            user_id=user_id
        )
        
        repository.status = "pending"
        db.commit()
        db.refresh(repository)
        return repository

    @staticmethod
    def run_analysis_pipeline(
        db: Session,
        repository_id: str,
        repository_path: Path,
        file_name: str
    ) -> Repository:
        # Edited on 2026-08-13: Added detailed profiling timers across the entire analysis pipeline to diagnose performance bottlenecks.
        from app.services.storage_service import StorageService

        pipeline_start = time.perf_counter()

        repository = RepositoryRepository.get_by_id(db=db, repository_id=repository_id)
        if not repository:
            raise ValueError(f"Repository {repository_id} not found")

        # Update status to indexing
        repository.status = "indexing"
        db.commit()
        db.refresh(repository)

        extracted_path = repository_path / "extracted"
        zip_path = repository_path / "source.zip"

        # Extract ZIP in background task
        start_extract = time.perf_counter()
        StorageService.extract_zip(
            zip_path=zip_path,
            repository_path=repository_path
        )
        extract_time = time.perf_counter() - start_extract
        print(f"PROFILER: Zip Extraction took {extract_time:.3f}s")

        repository_root = next(
            item
            for item in extracted_path.iterdir()
            if item.is_dir()
        )
        print("\n====== EXTRACTED CONTENT ======")
        for item in extracted_path.rglob("*"):
            pass # Suppressed full contents print to speed up I/O print time
        print("===============================\n")

        # Repository Analysis
        start_rep_analysis = time.perf_counter()
        analysis = RepositoryAnalyzer.analyze_repository(
            repository_root
        )
        rep_analysis_time = time.perf_counter() - start_rep_analysis
        print(f"PROFILER: Repository Analysis took {rep_analysis_time:.3f}s")

        start_rep_save = time.perf_counter()
        repository_analysis = RepositoryAnalysisCreate(
            repository_id=repository.id,
            total_files=analysis["total_files"],
            extensions=analysis["extensions"],
            languages=analysis["languages"],
            frameworks=analysis["frameworks"],
            libraries=analysis["libraries"]
        )

        analysis_record = RepositoryAnalysisService.create_analysis(
            db=db,
            repository_analysis=repository_analysis
        )
        db.commit()
        rep_save_time = time.perf_counter() - start_rep_save
        print(f"PROFILER: Repository Analysis DB Save took {rep_save_time:.3f}s")

        # Dependency Analysis
        start_dep_analysis = time.perf_counter()
        dependencies = DependencyAnalyzer.detect_dependencies(
            repository_root
        )
        dep_analysis_time = time.perf_counter() - start_dep_analysis
        print(f"PROFILER: Dependency Analysis took {dep_analysis_time:.3f}s")

        # Saving Dependencies
        start_dep_save = time.perf_counter()
        for dependency in dependencies:
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
        db.commit()
        dep_save_time = time.perf_counter() - start_dep_save
        print(f"PROFILER: Dependency Save to DB took {dep_save_time:.3f}s")
        
        start_dep_fetch = time.perf_counter()
        repository_dependencies = (
            RepositoryDependencyService.get_repository_dependencies(
                db=db,
                repository_id=repository.id
                )
        )
        dep_fetch_time = time.perf_counter() - start_dep_fetch
        print(f"PROFILER: Dependency Fetch from DB took {dep_fetch_time:.3f}s")

        # Architecture Analysis
        start_arch_analysis = time.perf_counter()
        architecture = ArchitectureAnalyzer.analyze_repository(
            repository_root
        )
        arch_analysis_time = time.perf_counter() - start_arch_analysis
        print(f"PROFILER: Architecture Analysis took {arch_analysis_time:.3f}s")

        # Saving Architecture
        start_arch_save = time.perf_counter()
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
        db.commit()
        arch_save_time = time.perf_counter() - start_arch_save
        print(f"PROFILER: Architecture Save to DB took {arch_save_time:.3f}s")

        # Document Generation
        start_doc_gen = time.perf_counter()
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
        doc_gen_time = time.perf_counter() - start_doc_gen
        print(f"PROFILER: Documentation Generation & File Save took {doc_gen_time:.3f}s")

        # Chunking & Embedding
        start_embedding = time.perf_counter()
        chunking_service = ChunkingService()
        embedding_service = EmbeddingService()
        vector_store = VectorStoreService()

        chunks = chunking_service.chunk_document(documentation)
        print(f"PROFILER: Document split into {len(chunks)} chunks")

        ids = []
        documents = []
        metadatas = []

        for chunk in chunks:
            ids.append(
                f"{repository.id}_{chunk['id']}"
            )

            documents.append(
                chunk["content"]
            )

            metadatas.append(
                {
                    "repository_id": repository.id,
                    "title": chunk["title"]
                }
            )

        # Edited on 2026-08-13: Fetch batch embeddings in a single request instead of iterating sequentially.
        embeddings = embedding_service.generate_embeddings(documents)

        embed_total_time = time.perf_counter() - start_embedding
        print(f"PROFILER: Embeddings loops took {embed_total_time:.3f}s")

        # Vector Database Storage
        start_vector_save = time.perf_counter()
        vector_store.add_documents(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )
        vector_save_time = time.perf_counter() - start_vector_save
        print(f"PROFILER: ChromaDB Vector Storage took {vector_save_time:.3f}s")

        # Updating Repository Status
        start_status = time.perf_counter()
        repository.status = "completed"
        db.commit()
        db.refresh(repository)
        status_time = time.perf_counter() - start_status
        print(f"PROFILER: Updating Status to completed took {status_time:.3f}s")

        total_pipeline_time = time.perf_counter() - pipeline_start
        print(f"PROFILER: TOTAL PIPELINE EXECUTION TIME: {total_pipeline_time:.3f}s")

        return repository