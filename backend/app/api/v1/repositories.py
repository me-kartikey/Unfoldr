from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.repository import (
    RepositoryCreate,
    RepositoryResponse
)
from app.services.repository_service import RepositoryService

router = APIRouter(
    prefix="/repositories",
    tags=["Repositories"]
)


@router.post(
    "",
    response_model=RepositoryResponse
)
def create_repository(
    repository_data: RepositoryCreate,
    db: Session = Depends(get_db)
):

    repository = RepositoryService.create_repository(
        db=db,
        repository_data=repository_data
    )

    return repository
@router.get(
    "",
    response_model=list[RepositoryResponse])
def get_repositories(
    db: Session=Depends(get_db)):
    return RepositoryService.get_repositories(db)