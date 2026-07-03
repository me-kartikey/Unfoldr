from pydantic import BaseModel

class RepositoryAnalysisCreate(BaseModel):

    repository_id: str
    total_files: int

    extensions: list[str]
    languages: list[str]
    frameworks: list[str]
    libraries: list[str]

class RepositoryAnalysisResponse(BaseModel):
    id: str
    repository_id: str
    total_files: int

    extensions: list[str]
    languages: list[str]
    frameworks: list[str]
    libraries: list[str]

    class Config:
        orm_mode = True