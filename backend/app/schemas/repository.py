from pydantic import BaseModel
from pydantic import ConfigDict

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
    model_config = ConfigDict(
        from_attributes=True
    )