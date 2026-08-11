
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
        repository_analysis: RepositoryAnalysisCreate
    ) -> RepositoryAnalysis:
        return RepositoryAnalysisRepository.create(
            db=db,
            repository_analysis=repository_analysis
        )

    @staticmethod
    def get_analysis(
        db: Session,
        repository_id: str
    ) -> RepositoryAnalysis | None:
        return RepositoryAnalysisRepository.get_by_repository_id(
            db=db,
            repository_id=repository_id
        )