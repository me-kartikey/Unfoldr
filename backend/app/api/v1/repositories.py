from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from app.services.storage_service import StorageService

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

@router.get(
    "/{repository_id}",
    response_model=RepositoryResponse)
def get_repository(
    repository_id: str,
    db: Session=Depends(get_db)):
    return RepositoryService.get_repository(db, repository_id)

@router.post("/upload")
def upload_repository(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)):
    repository_id, repository_path = (
    StorageService.create_repository_directory()
)
    zip_path = StorageService.save_zip(
    repository_path=repository_path,
    uploaded_file=file
)

    return {
    "repository_id": repository_id,
    "repository_path": str(repository_path),
    "filename": file.filename
}
    