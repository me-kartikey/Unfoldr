from pydantic import BaseModel, Field
from pydantic import ConfigDict
from typing import Optional

# Created on 13-08-2026: Validation schemas for User registration, login responses, and session tokens

class UserCreate(BaseModel):
    email: str = Field(..., min_length=3, max_length=255)
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=128)

class UserLogin(BaseModel):
    username_or_email: str
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    role: str
    is_active: bool
    
    model_config = ConfigDict(
        from_attributes=True
    )

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[str] = None
    role: Optional[str] = None
