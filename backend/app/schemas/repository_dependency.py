from pydantic import BaseModel, ConfigDict


class RepositoryDependencyCreate(BaseModel):

    repository_id: str

    name: str

    version: str | None = None

    language: str

    package_manager: str

    dependency_type: str = "production"


class RepositoryDependencyResponse(BaseModel):

    id: str

    repository_id: str

    name: str

    version: str | None

    language: str

    package_manager: str

    dependency_type: str

    model_config = ConfigDict(
        from_attributes=True
    )