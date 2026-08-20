from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.services.user_service import UserService
from app.core.security import create_access_token
from app.api.deps import get_current_user
from app.models.user import User

# Created on 13-08-2026: Authentication router for register, login, logout, and self-profile queries

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_create: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user account. Ensures unique email and username constraints.
    """
    return UserService.register_user(db, user_create)

@router.post("/login")
def login(response: Response, login_data: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user credentials, issue a JWT session token, and set it in a secure HTTP-only cookie.
    """
    from app.core.config import settings
    import hmac
    import hashlib

    user = UserService.authenticate_user(
        db, 
        login_data.username_or_email, 
        login_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username/email or password"
        )
    
    token = create_access_token(subject=user.id)
    is_secure = settings.environment != "development"
    
    # Set secure HttpOnly cookie for session tracking
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=is_secure,
        samesite="lax",
        max_age=settings.access_token_expire_minutes * 60
    )
    
    # Generate CSRF token statelessly tied to the session
    csrf_token = hmac.new(
        settings.csrf_secret_key.encode(),
        token.encode(),
        hashlib.sha256
    ).hexdigest()
    
    response.set_cookie(
        key="csrf_token",
        value=csrf_token,
        httponly=False,  # JavaScript needs to read this to send in header
        secure=is_secure,
        samesite="lax",
        max_age=settings.access_token_expire_minutes * 60
    )
    
    return {"status": "success", "message": "Logged in successfully"}

@router.post("/logout")
def logout(response: Response):
    """
    Log out user by deleting the access_token session cookie.
    """
    from app.core.config import settings
    is_secure = settings.environment != "development"
    
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=is_secure,
        samesite="lax"
    )
    response.delete_cookie(
        key="csrf_token",
        httponly=False,
        secure=is_secure,
        samesite="lax"
    )
    return {"status": "success", "message": "Logged out successfully"}

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """
    Get information of the currently authenticated user session.
    """
    return current_user
