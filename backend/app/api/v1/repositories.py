from fastapi import APIRouter, Depends, File, UploadFile
import time
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

@router.post(
        "/upload",
        response_model=RepositoryResponse
        )

def upload_repository(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)):
    # Total Scan Time start
    total_start = time.perf_counter()  # added to check timing

    repository_id, repository_path = (
    StorageService.create_repository_directory()
)
    # Saving ZIP timing
    start_save = time.perf_counter()  # added to check timing
    zip_path = StorageService.save_zip(
    repository_path=repository_path,
    uploaded_file=file
)
    save_time = time.perf_counter() - start_save  # added to check timing
    print(f"Saving uploaded ZIP: {save_time:.3f}s")

    # Extracting ZIP timing
    start_extract = time.perf_counter()  # added to check timing
    extract_path = StorageService.extract_zip(
    zip_path=zip_path,
    repository_path=repository_path
)
    extract_time = time.perf_counter() - start_extract  # added to check timing
    print(f"ZIP Extraction: {extract_time:.3f}s")

    repository = RepositoryService.create_uploaded_repository(
        db=db,
        file_name=file.filename,
        repository_path=repository_path
    )

    # Total Scan Time end
    total_time = time.perf_counter() - total_start  # added to check timing
    print(f"Total Scan Time: {total_time:.3f}s")

    return repository

