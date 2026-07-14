from pydantic import BaseModel, ConfigDict


class RepositoryArchitectureCreate(BaseModel):

    repository_id: str

    project_type: str
    backend_framework: str
    frontend_framework: str
    architecture_pattern: str

    entry_points: list[str]
    root_folders: list[str]
    config_files: list[str]
    databases: list[str]
    orms: list[str]
    authentication_methods: list[str]
    api_styles: list[str]
    devops_tools: list[str]
    cicd_tools: list[str]
    testing_frameworks: list[str]
    code_quality_tools: list[str]
    environment_files: list[str]
    deployment_platforms: list[str]
    repository_characteristics: list[str]


class RepositoryArchitectureResponse(BaseModel):

    id: str

    repository_id: str

    project_type: str
    backend_framework: str
    frontend_framework: str
    architecture_pattern: str

    entry_points: list[str]
    root_folders: list[str]
    config_files: list[str]
    databases: list[str]
    orms: list[str]
    authentication_methods: list[str]
    api_styles: list[str]
    devops_tools: list[str]
    cicd_tools: list[str]
    testing_frameworks: list[str]
    code_quality_tools: list[str]
    environment_files: list[str]
    deployment_platforms: list[str]
    repository_characteristics: list[str]

    model_config = ConfigDict(
        from_attributes=True
    )