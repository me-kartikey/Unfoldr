from fastapi import Request, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import decode_access_token
from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.models.repository import Repository

# Created on 13-08-2026: Dependency injection utilities for user authentication and repository ownership validation

def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    """
    FastAPI dependency injection to authenticate requests via HTTP-only cookie.
    Falls back to Bearer headers for testing/Swagger utility.
    """
    token = request.cookies.get("access_token")
    if not token:
        # Fallback to Authorization Header for Swagger UI testing convenience
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.replace("Bearer ", "")
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated"
            )

    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired or invalid token"
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    
    user = UserRepository.get_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
        
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is inactive"
        )
        
    return user

def check_repository_owner(
    repository_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Repository:
    """
    Dependency to verify that the authenticated user owns the target repository resource.
    """
    from app.services.repository_service import RepositoryService
    repository = RepositoryService.get_repository(db, repository_id)
    if not repository:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repository not found"
        )
        
    if repository.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: You are not the owner of this repository"
        )
        
    return repository
