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

        backend_framework = (
            ArchitectureAnalyzer.detect_backend_framework(
                repository_path
            )
        )

        frontend_framework = (
            ArchitectureAnalyzer.detect_frontend_framework(
                repository_path
            )
        )

        project_type = ArchitectureAnalyzer.detect_project_type(
            backend_framework,
            frontend_framework
        )

        architecture_pattern = (
            ArchitectureAnalyzer.detect_architecture_pattern(
                root_folders
            )
        )

        databases = (
            ArchitectureAnalyzer.detect_databases(
                repository_path
            )
        )

        orms = (
            ArchitectureAnalyzer.detect_orms(
                repository_path
            )
        )

        authentication_methods = (
            ArchitectureAnalyzer.detect_authentication(
                repository_path
            )
        )

        api_styles = (
            ArchitectureAnalyzer.detect_api_styles(
                repository_path
            )
        )

        devops = (
            ArchitectureAnalyzer.detect_devops(
                repository_path
            )
        )

        cicd = (
            ArchitectureAnalyzer.detect_cicd(
                repository_path
            )
        )

        testing = (
            ArchitectureAnalyzer.detect_testing(
                repository_path
            )
        )

        code_quality = (
            ArchitectureAnalyzer.detect_code_quality(
                repository_path
            )
        )

        environment = (
            ArchitectureAnalyzer.detect_environment(
                repository_path
            )
        )

        deployment = (
            ArchitectureAnalyzer.detect_deployment(
                repository_path
            )
        )

        repository_characteristics = (
            ArchitectureAnalyzer.detect_repository_characteristics(
                repository_path
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
        repository_path: Path,
        file_names: list[str]
    ) -> dict[str, list[str]]:

        contents = {}

        for file_name in file_names:

            file_contents = []

            files = list(
                repository_path.rglob(file_name)
            )

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
        repository_path: Path
    ) -> str:

        contents = (
            ArchitectureAnalyzer.read_repository_file(
                repository_path,
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
        repository_path: Path
    ) -> str:

        contents = (
            ArchitectureAnalyzer.read_repository_file(
                repository_path,
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
        root_folders: list[str]
    ) -> str:

        folders = {
            folder.lower()
            for folder in root_folders
        }

        if LAYERED_FOLDERS.issubset(folders):
            return "Layered Architecture"

        if CLEAN_ARCHITECTURE_FOLDERS.issubset(folders):
            return "Clean Architecture"

        if HEXAGONAL_FOLDERS.issubset(folders):
            return "Hexagonal Architecture"

        if MVC_FOLDERS.issubset(folders):
            return "MVC"

        return "Unknown"

    @staticmethod
    def detect_databases(
        repository_path: Path
    ) -> list[str]:

        databases = set()

        contents = (
            ArchitectureAnalyzer.read_repository_file(
                repository_path,
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
        repository_path: Path
    ) -> list[str]:

        orms = set()

        contents = (
            ArchitectureAnalyzer.read_repository_file(
                repository_path,
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
        repository_path: Path
    ) -> list[str]:

        authentication_methods = set()

        contents = (
            ArchitectureAnalyzer.read_repository_file(
                repository_path,
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
        repository_path: Path
    ) -> list[str]:

        api_styles = set()

        contents = (
            ArchitectureAnalyzer.read_repository_file(
                repository_path,
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
        repository_path: Path
    ) -> list[str]:

        devops = set()

        contents = (
            ArchitectureAnalyzer.read_repository_file(
                repository_path,
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
        repository_path: Path
    ) -> list[str]:

        cicd = set()

        contents = (
            ArchitectureAnalyzer.read_repository_file(
                repository_path,
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
        repository_path: Path
    ) -> list[str]:

        testing = set()

        contents = (
            ArchitectureAnalyzer.read_repository_file(
                repository_path,
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
        repository_path: Path
    ) -> list[str]:

        code_quality = set()

        contents = (
            ArchitectureAnalyzer.read_repository_file(
                repository_path,
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
        repository_path: Path
    ) -> list[str]:

        environment = set()

        contents = (
            ArchitectureAnalyzer.read_repository_file(
                repository_path,
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
        repository_path: Path
    ) -> list[str]:

        deployment = set()

        contents = (
            ArchitectureAnalyzer.read_repository_file(
                repository_path,
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
        repository_path: Path
    ) -> list[str]:

        repository_characteristics = set()

        contents = (
            ArchitectureAnalyzer.read_repository_file(
                repository_path,
                REPOSITORY_FILES
            )
        )

        for file_contents in contents.values():

            for content in file_contents:

                for keyword, characteristic in REPOSITORY_CHARACTERISTICS.items():

                    if keyword.lower() in content:

                        repository_characteristics.add(characteristic)

        return sorted(repository_characteristics)