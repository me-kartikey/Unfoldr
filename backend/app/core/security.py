import bcrypt
import jwt
from datetime import datetime, timedelta, UTC
from typing import Optional

from app.core.config import settings

# Created on 13-08-2026: Security service for password hashing and stateless session validation using cryptographically signed JSON Web Tokens (JWT)

def get_password_hash(password: str) -> str:
    """
    Hash password using bcrypt and return string representation.
    """
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify plain password against hashed password using bcrypt.
    """
    plain_bytes = plain_password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")
    try:
        return bcrypt.checkpw(plain_bytes, hashed_bytes)
    except Exception:
        return False

def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """
    Generate cryptographically signed JWT token.
    """
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode = {
        "exp": expire,
        "sub": str(subject)
    }
    
    return jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )

def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode and validate a JWT access token.
    """
    try:
        return jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
