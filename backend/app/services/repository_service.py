from sqlalchemy.orm import Session

from app.models.repository import Repository
from app.repositories.repository_repository import RepositoryRepository
from app.schemas.repository import RepositoryCreate
from app.analyzers.repository_analyzer import RepositoryAnalyzer
from app.schemas.repository_analysis import RepositoryAnalysisCreate
from app.services.repository_analysis_service import (
    RepositoryAnalysisService
)
from pathlib import Path


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
        repository_name= file_name.removesuffix(".zip")
        repository_data=RepositoryCreate(
            name=repository_name,
            original_name=file_name,
            storage_path=str(repository_path)
        )
        repository=RepositoryRepository.create(
            db=db,
            repository_data=repository_data
        )

        extracted_path = repository_path / "extracted"
        analysis = RepositoryAnalyzer.analyze_repository(extracted_path)
        repository_analysis = RepositoryAnalysisCreate(
        repository_id=repository.id,
        total_files=analysis["total_files"],
        extensions=analysis["extensions"],
        languages=analysis["languages"],
        frameworks=analysis["frameworks"],
        libraries=analysis["libraries"]
        )

        RepositoryAnalysisService.create_analysis(
            db=db,
            repository_analysis=repository_analysis
        )
        return repository
        
     
