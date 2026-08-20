from pathlib import Path

from app.constants.architecture_constants import (
    ENTRY_POINTS,
    CONFIG_FILES,
    LAYERED_FOLDERS,
    MVC_FOLDERS,
    CLEAN_ARCHITECTURE_FOLDERS,
    HEXAGONAL_FOLDERS,
    IGNORE_FOLDERS
)

from app.constants.framework_constants import (
    BACKEND_FRAMEWORKS,
    FRONTEND_FRAMEWORKS,
    BACKEND_FRAMEWORK_FILES,
    FRONTEND_FRAMEWORK_FILES
)

from app.constants.database_constants import (
    DATABASES,
    DATABASE_FILES
)

from app.constants.orm_constants import (
    ORMS,
    ORM_FILES
)

from app.constants.authentication_constants import (
    AUTHENTICATION_METHODS,
    AUTHENTICATION_FILES
)

from app.constants.api_style_constants import (
    API_STYLES,
    API_STYLE_FILES
)

from app.constants.devops_constants import (
    DEVOPS_TOOLS,
    DEVOPS_FILES
)

from app.constants.cicd_constants import (
    CICD_PLATFORMS,
    CICD_FILES
)

from app.constants.testing_constants import (
    TESTING_TOOLS,
    TESTING_FILES
)

from app.constants.code_quality_constants import (
    CODE_QUALITY_TOOLS,
    CODE_QUALITY_FILES
)

from app.constants.environment_constants import (
    ENVIRONMENT_CONFIGS,
    ENVIRONMENT_FILES
)

from app.constants.deployment_constants import (
    DEPLOYMENT_PLATFORMS,
    DEPLOYMENT_FILES
)

from app.constants.repository_constants import (
    REPOSITORY_CHARACTERISTICS,
    REPOSITORY_FILES
)


class ArchitectureAnalyzer:

    @staticmethod
    def analyze_repository(
        repository_path: Path
    ) -> dict:
        # Edited on 2026-08-13: Refactored to index repository files once and perform scans in-memory.
        from app.core.file_scanner import FileScanner

        tracked_files = FileScanner.scan_repository(repository_path)

        root_folders = []
        entry_points = []
        config_files = []

        # Root folders and entry points are determined from direct repository children
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

        backend_framework = (
            ArchitectureAnalyzer.detect_backend_framework(
                tracked_files
            )
        )

        frontend_framework = (
            ArchitectureAnalyzer.detect_frontend_framework(
                tracked_files
            )
        )

        project_type = ArchitectureAnalyzer.detect_project_type(
            backend_framework,
            frontend_framework
        )

        architecture_pattern = (
            ArchitectureAnalyzer.detect_architecture_pattern(
                tracked_files,
                root_folders
            )
        )

        databases = (
            ArchitectureAnalyzer.detect_databases(
                tracked_files
            )
        )

        orms = (
            ArchitectureAnalyzer.detect_orms(
                tracked_files
            )
        )

        authentication_methods = (
            ArchitectureAnalyzer.detect_authentication(
                tracked_files
            )
        )

        api_styles = (
            ArchitectureAnalyzer.detect_api_styles(
                tracked_files
            )
        )

        devops = (
            ArchitectureAnalyzer.detect_devops(
                tracked_files
            )
        )

        cicd = (
            ArchitectureAnalyzer.detect_cicd(
                tracked_files
            )
        )

        testing = (
            ArchitectureAnalyzer.detect_testing(
                tracked_files
            )
        )

        code_quality = (
            ArchitectureAnalyzer.detect_code_quality(
                tracked_files
            )
        )

        environment = (
            ArchitectureAnalyzer.detect_environment(
                tracked_files
            )
        )

        deployment = (
            ArchitectureAnalyzer.detect_deployment(
                tracked_files
            )
        )

        repository_characteristics = (
            ArchitectureAnalyzer.detect_repository_characteristics(
                tracked_files
            )
        )

        return {
            "project_type": project_type,
            "architecture_pattern": architecture_pattern,
            "entry_points": sorted(entry_points),
            "root_folders": sorted(root_folders),
            "config_files": sorted(config_files),
            "backend_framework": backend_framework,
            "frontend_framework": frontend_framework,
            "databases": databases,
            "orms": orms,
            "authentication_methods": authentication_methods,
            "api_styles": api_styles,
            "devops": devops,
            "cicd": cicd,
            "testing": testing,
            "code_quality": code_quality,
            "environment": environment,
            "deployment": deployment,
            "repository_characteristics": repository_characteristics
        }

    @staticmethod
    def read_repository_file(
        tracked_files: list[Path],
        file_names: list[str]
    ) -> dict[str, list[str]]:
        # Edited on 2026-08-13: Refactored to query file contents directly from the pre-scanned in-memory tracked_files list.
        contents = {}

        for file_name in file_names:
            file_contents = []

            # In-memory name filtering (substitutes disk rglob)
            files = [f for f in tracked_files if f.name == file_name]

            for file in files:
                try:
                    file_contents.append(
                        file.read_text(
                            encoding="utf-8",
                            errors="ignore"
                        ).lower()
                    )
                except Exception:
                    continue

            if file_contents:
                contents[file_name] = file_contents

        return contents

    @staticmethod
    def detect_project_type(
        backend_framework: str,
        frontend_framework: str
    ) -> str:
        if (
            backend_framework != "Unknown"
            and frontend_framework != "Unknown"
        ):
            return "Full Stack"

        if backend_framework != "Unknown":
            return "Backend"

        if frontend_framework != "Unknown":
            return "Frontend"

        return "Unknown"

    @staticmethod
    def detect_backend_framework(
        tracked_files: list[Path]
    ) -> str:
        contents = (
            ArchitectureAnalyzer.read_repository_file(
                tracked_files,
                BACKEND_FRAMEWORK_FILES
            )
        )

        for file_contents in contents.values():
            for content in file_contents:
                for package, framework in BACKEND_FRAMEWORKS.items():
                    if package.lower() in content:
                        return framework

        return "Unknown"

    @staticmethod
    def detect_frontend_framework(
        tracked_files: list[Path]
    ) -> str:
        contents = (
            ArchitectureAnalyzer.read_repository_file(
                tracked_files,
                FRONTEND_FRAMEWORK_FILES
            )
        )

        for file_contents in contents.values():
            for content in file_contents:
                for package, framework in FRONTEND_FRAMEWORKS.items():
                    if package.lower() in content:
                        return framework

        return "Unknown"

    @staticmethod
    def detect_architecture_pattern(
        tracked_files: list[Path],
        root_folders: list[str]
    ) -> str:
        # Collect all directory names recursively across the entire repository
        all_folder_names = set()
        for folder in root_folders:
            all_folder_names.add(folder.lower())

        for file_path in tracked_files:
            for parent in file_path.parents:
                if parent.name and parent.name not in IGNORE_FOLDERS:
                    all_folder_names.add(parent.name.lower())

        # Define pattern indicator sets
        layered_indicators = {"controllers", "services", "repositories", "models", "schemas", "routes", "middlewares", "api", "endpoints", "handlers", "dao", "dto"}
        mvc_indicators = {"controllers", "models", "views", "templates"}
        clean_indicators = {"domain", "application", "infrastructure", "presentation", "usecases", "core"}
        hexagonal_indicators = {"adapters", "ports"}
        component_indicators = {"components", "pages", "views", "layouts", "containers", "widgets", "hooks", "store"}

        # Calculate intersection scores
        layered_score = len(layered_indicators.intersection(all_folder_names))
        mvc_score = len(mvc_indicators.intersection(all_folder_names))
        clean_score = len(clean_indicators.intersection(all_folder_names))
        hexagonal_score = len(hexagonal_indicators.intersection(all_folder_names))
        component_score = len(component_indicators.intersection(all_folder_names))

        # Check for Clean Architecture
        if clean_score >= 2 or ("domain" in all_folder_names and "infrastructure" in all_folder_names):
            return "Clean Architecture"

        # Check for Hexagonal Architecture
        if hexagonal_score >= 1 or ("adapters" in all_folder_names and "ports" in all_folder_names):
            return "Hexagonal Architecture"

        # Check for MVC Architecture
        if ("controllers" in all_folder_names and "views" in all_folder_names) or mvc_score >= 2:
            return "MVC Architecture"

        # Check for Layered Architecture (Service / Repository / Route / Controller pattern)
        if layered_score >= 2 or ("services" in all_folder_names or "routes" in all_folder_names or "api" in all_folder_names):
            return "Layered Architecture"

        # Check for Component-Based SPA Architecture
        if component_score >= 2 or "components" in all_folder_names or "pages" in all_folder_names:
            return "Component-Based Architecture"

        # Fallback for standard repository structures
        if len(root_folders) > 0:
            return "Modular Monolith"

        return "Standard Monolithic"

    @staticmethod
    def detect_databases(
        tracked_files: list[Path]
    ) -> list[str]:
        databases = set()
        contents = (
            ArchitectureAnalyzer.read_repository_file(
                tracked_files,
                DATABASE_FILES
            )
        )

        for file_contents in contents.values():
            for content in file_contents:
                for keyword, database in DATABASES.items():
                    if keyword.lower() in content:
                        databases.add(database)

        return sorted(databases)

    @staticmethod
    def detect_orms(
        tracked_files: list[Path]
    ) -> list[str]:
        orms = set()
        contents = (
            ArchitectureAnalyzer.read_repository_file(
                tracked_files,
                ORM_FILES
            )
        )

        for file_contents in contents.values():
            for content in file_contents:
                for keyword, orm in ORMS.items():
                    if keyword.lower() in content:
                        orms.add(orm)

        return sorted(orms)

    @staticmethod
    def detect_authentication(
        tracked_files: list[Path]
    ) -> list[str]:
        authentication_methods = set()
        contents = (
            ArchitectureAnalyzer.read_repository_file(
                tracked_files,
                AUTHENTICATION_FILES
            )
        )

        for file_contents in contents.values():
            for content in file_contents:
                for keyword, auth_method in AUTHENTICATION_METHODS.items():
                    if keyword.lower() in content:
                        authentication_methods.add(auth_method)

        return sorted(authentication_methods)

    @staticmethod
    def detect_api_styles(
        tracked_files: list[Path]
    ) -> list[str]:
        api_styles = set()
        contents = (
            ArchitectureAnalyzer.read_repository_file(
                tracked_files,
                API_STYLE_FILES
            )
        )

        for file_contents in contents.values():
            for content in file_contents:
                for keyword, api_style in API_STYLES.items():
                    if keyword.lower() in content:
                        api_styles.add(api_style)

        return sorted(api_styles)

    @staticmethod
    def detect_devops(
        tracked_files: list[Path]
    ) -> list[str]:
        devops = set()
        contents = (
            ArchitectureAnalyzer.read_repository_file(
                tracked_files,
                DEVOPS_FILES
            )
        )

        for file_contents in contents.values():
            for content in file_contents:
                for keyword, devops_tool in DEVOPS_TOOLS.items():
                    if keyword.lower() in content:
                        devops.add(devops_tool)

        return sorted(devops)

    @staticmethod
    def detect_cicd(
        tracked_files: list[Path]
    ) -> list[str]:
        cicd = set()
        contents = (
            ArchitectureAnalyzer.read_repository_file(
                tracked_files,
                CICD_FILES
            )
        )

        for file_contents in contents.values():
            for content in file_contents:
                for keyword, cicd_platform in CICD_PLATFORMS.items():
                    if keyword.lower() in content:
                        cicd.add(cicd_platform)

        return sorted(cicd)

    @staticmethod
    def detect_testing(
        tracked_files: list[Path]
    ) -> list[str]:
        testing = set()
        contents = (
            ArchitectureAnalyzer.read_repository_file(
                tracked_files,
                TESTING_FILES
            )
        )

        for file_contents in contents.values():
            for content in file_contents:
                for keyword, testing_tool in TESTING_TOOLS.items():
                    if keyword.lower() in content:
                        testing.add(testing_tool)

        return sorted(testing)

    @staticmethod
    def detect_code_quality(
        tracked_files: list[Path]
    ) -> list[str]:
        code_quality = set()
        contents = (
            ArchitectureAnalyzer.read_repository_file(
                tracked_files,
                CODE_QUALITY_FILES
            )
        )

        for file_contents in contents.values():
            for content in file_contents:
                for keyword, code_quality_tool in CODE_QUALITY_TOOLS.items():
                    if keyword.lower() in content:
                        code_quality.add(code_quality_tool)

        return sorted(code_quality)

    @staticmethod
    def detect_environment(
        tracked_files: list[Path]
    ) -> list[str]:
        environment = set()
        contents = (
            ArchitectureAnalyzer.read_repository_file(
                tracked_files,
                ENVIRONMENT_FILES
            )
        )

        for file_contents in contents.values():
            for content in file_contents:
                for keyword, environment_config in ENVIRONMENT_CONFIGS.items():
                    if keyword.lower() in content:
                        environment.add(environment_config)

        return sorted(environment)

    @staticmethod
    def detect_deployment(
        tracked_files: list[Path]
    ) -> list[str]:
        deployment = set()
        contents = (
            ArchitectureAnalyzer.read_repository_file(
                tracked_files,
                DEPLOYMENT_FILES
            )
        )

        for file_contents in contents.values():
            for content in file_contents:
                for keyword, deployment_platform in DEPLOYMENT_PLATFORMS.items():
                    if keyword.lower() in content:
                        deployment.add(deployment_platform)

        return sorted(deployment)

    @staticmethod
    def detect_repository_characteristics(
        tracked_files: list[Path]
    ) -> list[str]:
        repository_characteristics = set()
        contents = (
            ArchitectureAnalyzer.read_repository_file(
                tracked_files,
                REPOSITORY_FILES
            )
        )

        for file_contents in contents.values():
            for content in file_contents:
                for keyword, characteristic in REPOSITORY_CHARACTERISTICS.items():
                    if keyword.lower() in content:
                        repository_characteristics.add(characteristic)

        return sorted(repository_characteristics)