from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password

# Created on 13-08-2026: User service wrapping repositories and security logic for authentication validation

class UserService:
    @staticmethod
    def register_user(db: Session, user_create: UserCreate) -> User:
        # Check if email already registered
        existing_email = UserRepository.get_by_email(db, user_create.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Check if username already taken
        existing_username = UserRepository.get_by_username(db, user_create.username)
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )

        # Hash password and create record
        hashed = get_password_hash(user_create.password)
        return UserRepository.create(db, user_create, hashed)

    @staticmethod
    def authenticate_user(db: Session, username_or_email: str, password: str) -> User | None:
        user = None
        if "@" in username_or_email:
            user = UserRepository.get_by_email(db, username_or_email)
        else:
            user = UserRepository.get_by_username(db, username_or_email)

        if not user:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user
