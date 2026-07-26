from pathlib import Path

from app.models.repository import Repository
from app.models.repository_analysis import RepositoryAnalysis
from app.models.repository_architecture import RepositoryArchitecture
from app.models.repository_dependency import RepositoryDependency


class DocumentsGenerator:

    @classmethod
    def generate(
        cls,
        repository: Repository,
        analysis: RepositoryAnalysis,
        architecture: RepositoryArchitecture,
        dependencies: list[RepositoryDependency],
    ) -> str:

        sections = [
            cls._title(repository),
            cls._overview(repository, analysis),
            cls._languages(analysis),
            cls._frameworks(analysis),
            cls._libraries(analysis),
            cls._architecture(architecture),
            cls._folder_structure(architecture),
            cls._entry_points(architecture),
            cls._configuration_files(architecture),
            cls._databases(architecture),
            cls._orms(architecture),
            cls._authentication(architecture),
            cls._api_styles(architecture),
            cls._devops(architecture),
            cls._cicd(architecture),
            cls._testing(architecture),
            cls._code_quality(architecture),
            cls._environment_files(architecture),
            cls._deployment(architecture),
            cls._characteristics(architecture),
            cls._dependencies(dependencies),
        ]

        return "\n\n".join(
            section
            for section in sections
            if section.strip()
        )

    @classmethod
    def save_documentation(
        cls,
        output_path: str,
        content: str,
    ) -> None:

        output = Path(output_path)

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output.write_text(
            content,
            encoding="utf-8",
        )

    @staticmethod
    def _split_csv(value):

        if not value:
            return []

        if isinstance(value, list):
            return value

        if isinstance(value, str):
            return [
                item.strip()
                for item in value.split(",")
                if item.strip()
            ]

        return []
    
    @staticmethod
    def _list_section(title: str, values: list[str]) -> str:

        if not values:
            return ""

        lines = [
            f"## {title}",
            "",
        ]

        for value in values:
            lines.append(f"- {value}")

        return "\n".join(lines)

    @staticmethod
    def _title(
        repository: Repository,
    ) -> str:

        return (
            f"# {repository.name}\n\n"
            "Automatically generated project documentation."
        )

    @classmethod
    def _overview(
        cls,
        repository: Repository,
        analysis: RepositoryAnalysis,
    ) -> str:

        return "\n".join(
            [
                "## Project Overview",
                "",
                f"- Repository : {repository.name}",
                f"- Status : {repository.status}",
                f"- Total Files : {analysis.total_files}",
            ]
        )

    @classmethod
    def _languages(
        cls,
        analysis: RepositoryAnalysis,
    ) -> str:

        return cls._list_section(
            "Languages",
            cls._split_csv(
                analysis.languages,
            ),
        )

    @classmethod
    def _frameworks(
        cls,
        analysis: RepositoryAnalysis,
    ) -> str:

        return cls._list_section(
            "Frameworks",
            cls._split_csv(
                analysis.frameworks,
            ),
        )

    @classmethod
    def _libraries(
        cls,
        analysis: RepositoryAnalysis,
    ) -> str:

        return cls._list_section(
            "Libraries",
            cls._split_csv(
                analysis.libraries,
            ),
        )

    @staticmethod
    def _architecture(
        architecture: RepositoryArchitecture,
    ) -> str:

        return "\n".join(
            [
                "## Architecture",
                "",
                f"- Project Type : {architecture.project_type}",
                f"- Backend Framework : {architecture.backend_framework}",
                f"- Frontend Framework : {architecture.frontend_framework}",
                f"- Architecture Pattern : {architecture.architecture_pattern}",
            ]
        )

    @classmethod
    def _folder_structure(
        cls,
        architecture: RepositoryArchitecture,
    ) -> str:

        return cls._list_section(
            "Root Folders",
            architecture.root_folders,
        )

    @classmethod
    def _entry_points(
        cls,
        architecture: RepositoryArchitecture,
    ) -> str:

        return cls._list_section(
            "Entry Points",
            architecture.entry_points,
        )

    @classmethod
    def _configuration_files(
        cls,
        architecture: RepositoryArchitecture,
    ) -> str:

        return cls._list_section(
            "Configuration Files",
            architecture.config_files,
        )

    @classmethod
    def _databases(
        cls,
        architecture: RepositoryArchitecture,
    ) -> str:

        return cls._list_section(
            "Databases",
            architecture.databases,
        )

    @classmethod
    def _orms(
        cls,
        architecture: RepositoryArchitecture,
    ) -> str:

        return cls._list_section(
            "ORMs",
            architecture.orms,
        )
    @classmethod
    def _authentication(
        cls,
        architecture: RepositoryArchitecture,
    ) -> str:

        return cls._list_section(
            "Authentication",
            architecture.authentication_methods,
        )

    @classmethod
    def _api_styles(
        cls,
        architecture: RepositoryArchitecture,
    ) -> str:

        return cls._list_section(
            "API Styles",
            architecture.api_styles,
        )

    @classmethod
    def _devops(
        cls,
        architecture: RepositoryArchitecture,
    ) -> str:

        return cls._list_section(
            "DevOps Tools",
            architecture.devops_tools,
        )

    @classmethod
    def _cicd(
        cls,
        architecture: RepositoryArchitecture,
    ) -> str:

        return cls._list_section(
            "CI/CD Tools",
            architecture.cicd_tools,
        )

    @classmethod
    def _testing(
        cls,
        architecture: RepositoryArchitecture,
    ) -> str:

        return cls._list_section(
            "Testing Frameworks",
            architecture.testing_frameworks,
        )

    @classmethod
    def _code_quality(
        cls,
        architecture: RepositoryArchitecture,
    ) -> str:

        return cls._list_section(
            "Code Quality Tools",
            architecture.code_quality_tools,
        )

    @classmethod
    def _environment_files(
        cls,
        architecture: RepositoryArchitecture,
    ) -> str:

        return cls._list_section(
            "Environment Files",
            architecture.environment_files,
        )

    @classmethod
    def _deployment(
        cls,
        architecture: RepositoryArchitecture,
    ) -> str:

        return cls._list_section(
            "Deployment Platforms",
            architecture.deployment_platforms,
        )

    @classmethod
    def _characteristics(
        cls,
        architecture: RepositoryArchitecture,
    ) -> str:

        return cls._list_section(
            "Repository Characteristics",
            architecture.repository_characteristics,
        )

    @staticmethod
    def _dependencies(
        dependencies: list[RepositoryDependency],
    ) -> str:

        if not dependencies:
            return ""

        lines = [
            "## Dependencies",
            "",
            "| Package | Version | Language | Package Manager | Type |",
            "|---------|---------|----------|-----------------|------|",
        ]

        dependencies = sorted(
            dependencies,
            key=lambda dependency: (
                dependency.language or "",
                dependency.name.lower(),
            ),
        )

        for dependency in dependencies:

            lines.append(
                "| "
                f"{dependency.name} | "
                f"{dependency.version or '-'} | "
                f"{dependency.language or '-'} | "
                f"{dependency.package_manager or '-'} | "
                f"{dependency.dependency_type or '-'} |"
            )

        return "\n".join(lines)