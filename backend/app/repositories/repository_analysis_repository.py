import json

from sqlalchemy.orm import Session

from app.models.repository_analysis import RepositoryAnalysis
from app.schemas.repository_analysis import RepositoryAnalysisCreate

class RepositoryAnalysisRepository:
    @staticmethod
    def create(
        db: Session,
        repository_analysis: RepositoryAnalysisCreate
    ) -> RepositoryAnalysis:

        repository_analysis = RepositoryAnalysis(
            repository_id=repository_analysis.repository_id,
            total_files=repository_analysis.total_files,
            extensions=json.dumps(repository_analysis.extensions),
            languages=json.dumps(repository_analysis.languages),
            frameworks=json.dumps(repository_analysis.frameworks),
            libraries=json.dumps(repository_analysis.libraries)
        )

        db.add(repository_analysis)

        db.commit() 

        db.refresh(repository_analysis)

        return repository_analysis