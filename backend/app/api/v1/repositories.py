# Edited on 2026-08-11 to support asynchronous repository analysis and polling.
# Edited on 13-08-2026: Add authentication and authorization dependency imports
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, BackgroundTasks
import time
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)
from app.analyzers.repository_analyzer import RepositoryAnalyzer
from sqlalchemy.orm import Session
from app.services.storage_service import StorageService

from app.db.session import get_db
from app.schemas.repository import (
    RepositoryCreate,
    RepositoryResponse
)
from app.services.repository_service import RepositoryService
from app.services.repository_analysis_service import (
    RepositoryAnalysisService
)
from app.services.repository_architecture_service import (
    RepositoryArchitectureService
)
from app.services.repository_dependency_service import (
    RepositoryDependencyService
)
from app.api.deps import get_current_user, check_repository_owner
from app.models.user import User
from app.models.repository import Repository

from app.schemas.repository_analysis import (
    RepositoryAnalysisCreate,
    RepositoryAnalysisResponse
)
from app.schemas.repository_architecture import (
    RepositoryArchitectureResponse
)
from app.schemas.repository_dependency import (
    RepositoryDependencyResponse
)

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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Edited on 13-08-2026: Set current user as owner on creation
    repository = RepositoryService.create_repository(
        db=db,
        repository_data=repository_data,
        user_id=current_user.id
    )

    return repository

@router.get(
    "",
    response_model=list[RepositoryResponse])
def get_repositories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Edited on 13-08-2026: Fetch only current user's repositories
    return RepositoryService.get_repositories(db, user_id=current_user.id)

@router.get(
    "/{repository_id}",
    response_model=RepositoryResponse)
def get_repository(
    repository_id: str,
    repository: Repository = Depends(check_repository_owner)
):
    # Edited on 13-08-2026: Validated repository ownership via dependency
    return repository

# Edited on 2026-08-11: Background task function to run repository analysis asynchronously.
def analyze_repository_task(repository_id: str, repository_path: str, file_name: str):
    from app.db.session import session_local
    from app.services.repository_service import RepositoryService
    
    db = session_local()
    try:
        RepositoryService.run_analysis_pipeline(
            db=db,
            repository_id=repository_id,
            repository_path=Path(repository_path),
            file_name=file_name
        )
    except Exception as e:
        logger.error(f"Error in background analysis task for repository {repository_id}: {e}", exc_info=True)
        try:
            repository = RepositoryService.get_repository(db, repository_id)
            if repository:
                repository.status = "failed"
                db.commit()
        except Exception as db_err:
            logger.error(f"Error updating fail status for repository {repository_id}: {db_err}")
    finally:
        db.close()


@router.post(
        "/upload",
        response_model=RepositoryResponse
        )
def upload_repository(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Edited on 13-08-2026: Associate upload with uploading user's ID
    repository_id, repository_path = StorageService.create_repository_directory()
    
    # Save the uploaded ZIP
    zip_path = StorageService.save_zip(
        repository_path=repository_path,
        uploaded_file=file
    )
    
    # Initialize repository with "pending" status
    repository = RepositoryService.initialize_uploaded_repository(
        db=db,
        file_name=file.filename,
        repository_path=repository_path,
        user_id=current_user.id
    )
    
    # Add background task to extract ZIP and run analysis pipeline
    background_tasks.add_task(
        analyze_repository_task,
        repository_id=repository.id,
        repository_path=str(repository_path),
        file_name=file.filename
    )
    
    return repository


@router.get(
    "/{repository_id}/analysis",
    response_model=RepositoryAnalysisResponse
)
def get_repository_analysis(
    repository_id: str,
    db: Session = Depends(get_db),
    repository: Repository = Depends(check_repository_owner)
):
    # Edited on 13-08-2026: Validated repository ownership via dependency
    analysis = RepositoryAnalysisService.get_analysis(db=db, repository_id=repository_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found for this repository")
    
    return RepositoryAnalysisResponse(
        id=analysis.id,
        repository_id=analysis.repository_id,
        total_files=analysis.total_files,
        extensions=json.loads(analysis.extensions) if isinstance(analysis.extensions, str) else analysis.extensions,
        languages=json.loads(analysis.languages) if isinstance(analysis.languages, str) else analysis.languages,
        frameworks=json.loads(analysis.frameworks) if isinstance(analysis.frameworks, str) else analysis.frameworks,
        libraries=json.loads(analysis.libraries) if isinstance(analysis.libraries, str) else analysis.libraries
    )


@router.get(
    "/{repository_id}/architecture",
    response_model=RepositoryArchitectureResponse
)
def get_repository_architecture(
    repository_id: str,
    db: Session = Depends(get_db),
    repository: Repository = Depends(check_repository_owner)
):
    # Edited on 13-08-2026: Validated repository ownership via dependency
    architecture = RepositoryArchitectureService.get_architecture(db=db, repository_id=repository_id)
    if not architecture:
        raise HTTPException(status_code=404, detail="Architecture not found for this repository")
    
    return architecture


@router.get(
    "/{repository_id}/dependencies",
    response_model=list[RepositoryDependencyResponse]
)
def get_repository_dependencies(
    repository_id: str,
    db: Session = Depends(get_db),
    repository: Repository = Depends(check_repository_owner)
):
    # Edited on 13-08-2026: Validated repository ownership via dependency
    dependencies = RepositoryDependencyService.get_repository_dependencies(db=db, repository_id=repository_id)
    return dependencies


@router.get(
    "/{repository_id}/documentation"
)
def get_repository_documentation(
    repository_id: str,
    db: Session = Depends(get_db),
    repository: Repository = Depends(check_repository_owner)
):
    # Edited on 13-08-2026: Validated repository ownership via dependency
    extracted_path = Path(repository.storage_path) / "extracted"
    try:
        repository_root = next(
            item for item in extracted_path.iterdir() if item.is_dir()
        )
    except StopIteration:
        repository_root = extracted_path

    doc_file = repository_root / "documentation.md"
    if not doc_file.exists():
        raise HTTPException(status_code=404, detail="Documentation file not found")
    
    try:
        content = doc_file.read_text(encoding="utf-8", errors="ignore")
        return {"documentation": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read documentation: {str(e)}")


@router.get(
    "/{repository_id}/files"
)
def get_repository_files(
    repository_id: str,
    db: Session = Depends(get_db),
    repository: Repository = Depends(check_repository_owner)
):
    # Edited on 13-08-2026: Validated repository ownership via dependency
    extracted_path = Path(repository.storage_path) / "extracted"
    try:
        repository_root = next(
            item for item in extracted_path.iterdir() if item.is_dir()
        )
    except StopIteration:
        repository_root = extracted_path

    def build_tree(path: Path, base_path: Path) -> dict | None:
        name = path.name
        rel_path = str(path.relative_to(base_path)).replace("\\", "/")
        
        ignored = {".git", "__pycache__", "node_modules", ".venv", "venv", ".idea", ".vscode", ".oxlintrc.json", ".gitignore"}
        if name in ignored:
            return None

        if path.is_file():
            return {
                "name": name,
                "path": rel_path,
                "type": "file"
            }
        elif path.is_dir():
            children = []
            try:
                for child in sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name.lower())):
                      child_tree = build_tree(child, base_path)
                      if child_tree:
                          children.append(child_tree)
            except Exception:
                pass
            return {
                "name": name,
                "path": rel_path,
                "type": "dir",
                "children": children
            }
        return None

    tree = build_tree(repository_root, repository_root)
    return tree or {"name": repository.name, "path": "", "type": "dir", "children": []}


@router.get(
    "/{repository_id}/file"
)
def get_file_content(
    repository_id: str,
    path: str,
    db: Session = Depends(get_db),
    repository: Repository = Depends(check_repository_owner)
):
    # Edited on 13-08-2026: Validated repository ownership via dependency
    extracted_path = Path(repository.storage_path) / "extracted"
    try:
        repository_root = next(
            item for item in extracted_path.iterdir() if item.is_dir()
        )
    except StopIteration:
        repository_root = extracted_path

    safe_path = (repository_root / path).resolve()
    if not str(safe_path).startswith(str(repository_root.resolve())):
        raise HTTPException(status_code=403, detail="Access denied")
    
    if not safe_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    SENSITIVE_PATTERNS = [".env", ".key", ".pem", ".p12", ".pfx", "id_rsa", "id_dsa"]
    for pattern in SENSITIVE_PATTERNS:
        if pattern.startswith(".") and safe_path.name.startswith(pattern):
            raise HTTPException(status_code=403, detail="Access denied: Sensitive file")
        if pattern.startswith("*.") and safe_path.name.endswith(pattern[1:]):
            raise HTTPException(status_code=403, detail="Access denied: Sensitive file")
        if pattern == safe_path.name:
            raise HTTPException(status_code=403, detail="Access denied: Sensitive file")
    
    try:
        content = safe_path.read_text(encoding="utf-8", errors="ignore")
        return {"content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read file content: {str(e)}")

