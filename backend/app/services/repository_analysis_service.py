from sqlalchemy.orm import Session

from app.models.repository_analysis import RepositoryAnalysis
from app.repositories.repository_analysis_repository import (
    RepositoryAnalysisRepository
)
from app.schemas.repository_analysis import RepositoryAnalysisCreate

class RepositoryAnalysisService:
    @staticmethod
    def create_analysis(
        db: Session,
        repository_analysis_create: RepositoryAnalysisCreate
    ) -> RepositoryAnalysis:
        return RepositoryAnalysisRepository.create(
            db=db,
            repository_analysis=repository_analysis_create
    )