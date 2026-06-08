from tokenize import String

from pydantic import BaseModel
class RepositoryCreate(BaseModel):
    name: str
    original_name: str
    storage_path: str 
class RepositoryResponse(BaseModel):
    id: str
    name: str
    original_name: str
    storage_path: str
    status: str