from pathlib import Path
from app.constants.architecture_constants import (
    ENTRY_POINTS,
    CONFIG_FILES,
    LAYERED_FOLDERS,
    MVC_FOLDERS,
    CLEAN_ARCHITECTURE_FOLDERS,
    MICROSERVICE_HINTS,
)

from app.constants.framework_constants import (
    BACKEND_FRAMEWORKS,
    FRONTEND_FRAMEWORKS
)

from app.constants.devops_constants import DEVOPS_FILES
from app.constants.testing_constants import TESTING_FRAMEWORKS
from app.constants.architecture_constants import IGNORE_FOLDERS


class ArchitectureAnalyzer:

    @staticmethod
    def analyze_repository(
        repository_path: Path
    ) -> dict:

        root_folders = []
        entry_points = []
        config_files = []

        for item in repository_path.iterdir():

            if (
                item.is_dir()
                and item.name not in IGNORE_FOLDERS
            ):
                root_folders.append(item.name)

            elif (
                item.is_file()
                and item.name in ENTRY_POINTS
            ):
                entry_points.append(item.name)

            if (
                item.is_file()
                and item.name in CONFIG_FILES
            ):
                config_files.append(item.name)

        project_type = ArchitectureAnalyzer.detect_project_type(
            repository_path,
            config_files
        )

        architecture_pattern = (
            ArchitectureAnalyzer.detect_architecture_pattern(
                root_folders
            )
        )

        return {
            "project_type": project_type,
            "architecture_pattern": architecture_pattern,
            "entry_points": sorted(entry_points),
            "root_folders": sorted(root_folders),
            "config_files": sorted(config_files)
        }

    @staticmethod
    def detect_project_type(
        repository_path: Path,
        config_files: list[str]
    ) -> str:

        requirements = (
            repository_path / "requirements.txt"
        )

        if requirements.exists():

            content = requirements.read_text(
                encoding="utf-8",
                errors="ignore"
            ).lower()

            if "fastapi" in content:
                return "FastAPI Backend"

            if "django" in content:
                return "Django Backend"

            if "flask" in content:
                return "Flask Backend"

        package_json = (
            repository_path / "package.json"
        )

        if package_json.exists():

            content = package_json.read_text(
                encoding="utf-8",
                errors="ignore"
            ).lower()

            if '"next"' in content:
                return "Next.js Frontend"

            if '"react"' in content:
                return "React Frontend"

            if '"express"' in content:
                return "Express Backend"

            if '"@nestjs"' in content:
                return "NestJS Backend"

        composer = (
            repository_path / "composer.json"
        )

        if composer.exists():
            return "Laravel"

        pom = (
            repository_path / "pom.xml"
        )

        if pom.exists():
            return "Spring Boot"

        return "Unknown"

    @staticmethod
    def detect_architecture_pattern(
        root_folders: list[str]
    ) -> str:

        folders = {
            folder.lower()
            for folder in root_folders
        }

        if {
            "controllers",
            "services",
            "repositories",
            "models"
        }.issubset(folders):
            return "Layered Architecture"

        if {
            "domain",
            "application",
            "infrastructure"
        }.issubset(folders):
            return "Clean Architecture"

        if {
            "adapters",
            "ports"
        }.issubset(folders):
            return "Hexagonal Architecture"

        if {
            "api",
            "services",
            "models"
        }.issubset(folders):
            return "MVC"

        return "Unknown"