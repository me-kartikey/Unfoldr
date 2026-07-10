from pydantic import BaseModel, ConfigDict


class RepositoryArchitectureCreate(BaseModel):

    repository_id: str

    project_type: str

    architecture_pattern: str

    entry_points: list[str]

    root_folders: list[str]

    config_files: list[str]


class RepositoryArchitectureResponse(BaseModel):

    id: str

    repository_id: str

    project_type: str

    architecture_pattern: str

    entry_points: list[str]

    root_folders: list[str]

    config_files: list[str]

    model_config = ConfigDict(
        from_attributes=True
    )