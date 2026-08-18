from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate

# Created on 13-08-2026: Repository class handling database operations for User queries

class UserRepository:
    @staticmethod
    def create(db: Session, user_create: UserCreate, hashed_password: str) -> User:
        user = User(
            email=user_create.email.lower().strip(),
            username=user_create.username.strip(),
            hashed_password=hashed_password,
            role="user",
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_by_id(db: Session, user_id: str) -> User | None:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_by_email(db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email.lower().strip()).first()

    @staticmethod
    def get_by_username(db: Session, username: str) -> User | None:
        return db.query(User).filter(User.username == username.strip()).first()
