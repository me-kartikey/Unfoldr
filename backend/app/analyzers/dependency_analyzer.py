from pathlib import Path
import json
import tomllib
import re
import xml.etree.ElementTree as ET


class DependencyAnalyzer:

    @staticmethod
    def create_dependency(
        name: str,
        version: str | None,
        language: str,
        package_manager: str,
        dependency_type: str = "production"
    ) -> dict:

        return {
            "name": name.strip(),
            "version": version,
            "language": language,
            "package_manager": package_manager,
            "dependency_type": dependency_type
        }

    @staticmethod
    def parse_dependency_string(
        dependency: str,
        language: str,
        package_manager: str,
        dependency_type: str = "production"
    ) -> dict:

        dependency = dependency.strip()

        operators = [
            "==",
            ">=",
            "<=",
            "~=",
            "!=",
            ">",
            "<"
        ]

        for operator in operators:

            if operator in dependency:

                name, version = dependency.split(
                    operator,
                    1
                )

                return DependencyAnalyzer.create_dependency(
                    name=name,
                    version=operator + version.strip(),
                    language=language,
                    package_manager=package_manager,
                    dependency_type=dependency_type
                )

        return DependencyAnalyzer.create_dependency(
            name=dependency,
            version=None,
            language=language,
            package_manager=package_manager,
            dependency_type=dependency_type
        )

    @staticmethod
    def parse_requirements_txt(
        tracked_files: list[Path]
    ) -> list[dict]:
        # Edited on 2026-08-13: Refactored to scan requirements from pre-scanned in-memory list instead of disk rglob.
        dependencies = []

        requirements_files = [f for f in tracked_files if f.name == "requirements.txt"]

        for requirements_file in requirements_files:
            with requirements_file.open(
                encoding="utf-8"
            ) as file:

                for line in file:
                    line = line.strip()

                    if (
                        not line
                        or line.startswith("#")
                    ):
                        continue

                    dependencies.append(
                        DependencyAnalyzer.parse_dependency_string(
                            dependency=line,
                            language="Python",
                            package_manager="pip"
                        )
                    )

        return dependencies

    @staticmethod
    def parse_package_json(
        tracked_files: list[Path]
    ) -> list[dict]:
        # Edited on 2026-08-13: Refactored to scan package.json from pre-scanned in-memory list.
        dependencies = []

        package_files = [f for f in tracked_files if f.name == "package.json"]

        for package_file in package_files:
            with package_file.open(
                encoding="utf-8"
            ) as file:
                package_data = json.load(file)

            for name, version in package_data.get(
                "dependencies",
                {}
            ).items():

                dependencies.append(
                    DependencyAnalyzer.create_dependency(
                        name=name,
                        version=version,
                        language="JavaScript",
                        package_manager="npm",
                        dependency_type="production"
                    )
                )

            for name, version in package_data.get(
                "devDependencies",
                {}
            ).items():

                dependencies.append(
                    DependencyAnalyzer.create_dependency(
                        name=name,
                        version=version,
                        language="JavaScript",
                        package_manager="npm",
                        dependency_type="development"
                    )
                )

        return dependencies

    @staticmethod
    def parse_pyproject_toml(
        tracked_files: list[Path]
    ) -> list[dict]:
        # Edited on 2026-08-13: Refactored to scan pyproject.toml from pre-scanned in-memory list.
        dependencies = []

        pyproject_files = [f for f in tracked_files if f.name == "pyproject.toml"]

        for pyproject_file in pyproject_files:
            with pyproject_file.open(
                "rb"
            ) as file:
                data = tomllib.load(file)

            project = data.get(
                "project",
                {}
            )

            for dependency in project.get(
                "dependencies",
                []
            ):

                dependencies.append(
                    DependencyAnalyzer.parse_dependency_string(
                        dependency=dependency,
                        language="Python",
                        package_manager="pip"
                    )
                )

            poetry_dependencies = (
                data.get("tool", {})
                .get("poetry", {})
                .get("dependencies", {})
            )

            for name, version in poetry_dependencies.items():
                if name == "python":
                    continue

                dependencies.append(
                    DependencyAnalyzer.create_dependency(
                        name=name,
                        version=str(version),
                        language="Python",
                        package_manager="poetry"
                    )
                )

        return dependencies

    @staticmethod
    def parse_pipfile(
        tracked_files: list[Path]
    ) -> list[dict]:
        # Edited on 2026-08-13: Refactored to scan Pipfile from pre-scanned in-memory list.
        dependencies = []

        pipfiles = [f for f in tracked_files if f.name == "Pipfile"]

        for pipfile in pipfiles:
            with pipfile.open(
                "rb"
            ) as file:
                data = tomllib.load(file)

            for name, version in data.get(
                "packages",
                {}
            ).items():

                dependencies.append(
                    DependencyAnalyzer.create_dependency(
                        name=name,
                        version=str(version),
                        language="Python",
                        package_manager="pipenv",
                        dependency_type="production"
                    )
                )

            for name, version in data.get(
                "dev-packages",
                {}
            ).items():

                dependencies.append(
                    DependencyAnalyzer.create_dependency(
                        name=name,
                        version=str(version),
                        language="Python",
                        package_manager="pipenv",
                        dependency_type="development"
                    )
                )

        return dependencies
    
    @staticmethod
    def parse_go_mod(
        tracked_files: list[Path]
    ) -> list[dict]:
        # Edited on 2026-08-13: Refactored to scan go.mod from pre-scanned in-memory list.
        dependencies = []

        go_mods = [f for f in tracked_files if f.name == "go.mod"]

        for go_mod in go_mods:
            with go_mod.open(
                encoding="utf-8"
            ) as file:
                lines = file.readlines()

            inside_require = False

            for line in lines:
                line = line.strip()

                if (
                    not line
                    or line.startswith("//")
                ):
                    continue

                if line.startswith("require ("):
                    inside_require = True
                    continue

                if inside_require and line == ")":
                    inside_require = False
                    continue

                if inside_require:
                    parts = line.split()

                    if len(parts) >= 2:
                        dependencies.append(
                            DependencyAnalyzer.create_dependency(
                                name=parts[0],
                                version=parts[1],
                                language="Go",
                                package_manager="go",
                                dependency_type="production"
                            )
                        )

                elif line.startswith("require"):
                    parts = line.replace(
                        "require",
                        ""
                    ).strip().split()

                    if len(parts) >= 2:
                        dependencies.append(
                            DependencyAnalyzer.create_dependency(
                                name=parts[0],
                                version=parts[1],
                                language="Go",
                                package_manager="go",
                                dependency_type="production"
                            )
                        )

        return dependencies

    @staticmethod
    def parse_cargo_toml(
        tracked_files: list[Path]
    ) -> list[dict]:
        # Edited on 2026-08-13: Refactored to scan Cargo.toml from pre-scanned in-memory list.
        dependencies = []

        cargo_files = [f for f in tracked_files if f.name == "Cargo.toml"]

        for cargo_file in cargo_files:
            with cargo_file.open(
                "rb"
            ) as file:
                data = tomllib.load(file)

            for name, version in data.get(
                "dependencies",
                {}
            ).items():

                if isinstance(
                    version,
                    dict
                ):
                    version = version.get(
                        "version"
                    )

                dependencies.append(
                    DependencyAnalyzer.create_dependency(
                        name=name,
                        version=str(version)
                        if version
                        else None,
                        language="Rust",
                        package_manager="cargo",
                        dependency_type="production"
                    )
                )

            for name, version in data.get(
                "dev-dependencies",
                {}
            ).items():

                if isinstance(
                    version,
                    dict
                ):
                    version = version.get(
                        "version"
                    )

                dependencies.append(
                    DependencyAnalyzer.create_dependency(
                        name=name,
                        version=str(version)
                        if version
                        else None,
                        language="Rust",
                        package_manager="cargo",
                        dependency_type="development"
                    )
                )

        return dependencies

    @staticmethod
    def parse_composer_json(
        tracked_files: list[Path]
    ) -> list[dict]:
        # Edited on 2026-08-13: Refactored to scan composer.json from pre-scanned in-memory list.
        dependencies = []

        composer_files = [f for f in tracked_files if f.name == "composer.json"]

        for composer_file in composer_files:
            with composer_file.open(
                encoding="utf-8"
            ) as file:
                data = json.load(file)

            for name, version in data.get(
                "require",
                {}
            ).items():

                if name == "php":
                    continue

                dependencies.append(
                    DependencyAnalyzer.create_dependency(
                        name=name,
                        version=version,
                        language="PHP",
                        package_manager="composer",
                        dependency_type="production"
                    )
                )

            for name, version in data.get(
                "require-dev",
                {}
            ).items():

                dependencies.append(
                    DependencyAnalyzer.create_dependency(
                        name=name,
                        version=version,
                        language="PHP",
                        package_manager="composer",
                        dependency_type="development"
                    )
                )

        return dependencies
    
    @staticmethod
    def parse_pom_xml(
        tracked_files: list[Path]
    ) -> list[dict]:
        # Edited on 2026-08-13: Refactored to scan pom.xml from pre-scanned in-memory list.
        dependencies = []

        pom_files = [f for f in tracked_files if f.name == "pom.xml"]

        for pom_file in pom_files:
            try:
                tree = ET.parse(pom_file)
                root = tree.getroot()
            except Exception:
                continue

            namespace = ""

            if root.tag.startswith("{"):
                namespace = root.tag.split("}")[0] + "}"

            for dependency in root.findall(
                f".//{namespace}dependency"
            ):

                group_id = dependency.find(
                    f"{namespace}groupId"
                )

                artifact_id = dependency.find(
                    f"{namespace}artifactId"
                )

                version = dependency.find(
                    f"{namespace}version"
                )

                if artifact_id is None:
                    continue

                name = artifact_id.text

                if (
                    group_id is not None
                    and group_id.text
                ):

                    name = (
                        f"{group_id.text}:{artifact_id.text}"
                    )

                dependencies.append(
                    DependencyAnalyzer.create_dependency(
                        name=name,
                        version=(
                            version.text
                            if version is not None
                            else None
                        ),
                        language="Java",
                        package_manager="maven",
                        dependency_type="production"
                    )
                )

        return dependencies

    @staticmethod
    def parse_build_gradle(
        tracked_files: list[Path]
    ) -> list[dict]:
        # Edited on 2026-08-13: Refactored to scan build gradle from pre-scanned in-memory list.
        dependencies = []

        gradle_files = [f for f in tracked_files if f.name in ("build.gradle", "build.gradle.kts")]

        pattern = re.compile(
            r'["\']([^:"\']+):([^:"\']+):([^"\']+)["\']'
        )

        for gradle_file in gradle_files:
            with gradle_file.open(
                encoding="utf-8",
                errors="ignore"
            ) as file:

                for line in file:
                    match = pattern.search(
                        line
                    )

                    if not match:
                        continue

                    group = match.group(1)
                    artifact = match.group(2)
                    version = match.group(3)

                    dependency_type = (
                        "development"
                        if "testImplementation" in line
                        else "production"
                    )

                    dependencies.append(
                        DependencyAnalyzer.create_dependency(
                            name=f"{group}:{artifact}",
                            version=version,
                            language="Java",
                            package_manager="gradle",
                            dependency_type=dependency_type
                        )
                    )

        return dependencies

    @staticmethod
    def detect_dependencies(
        repository_path: Path
    ) -> list[dict]:
        # Edited on 2026-08-13: Refactored to scan repository once and reuse the file list in-memory.
        from app.core.file_scanner import FileScanner

        tracked_files = FileScanner.scan_repository(repository_path)

        dependencies = []

        dependencies.extend(
            DependencyAnalyzer.parse_requirements_txt(
                tracked_files
            )
        )

        dependencies.extend(
            DependencyAnalyzer.parse_package_json(
                tracked_files
            )
        )

        dependencies.extend(
            DependencyAnalyzer.parse_pyproject_toml(
                tracked_files
            )
        )

        dependencies.extend(
            DependencyAnalyzer.parse_pipfile(
                tracked_files
            )
        )

        dependencies.extend(
            DependencyAnalyzer.parse_go_mod(
                tracked_files
            )
        )

        dependencies.extend(
            DependencyAnalyzer.parse_cargo_toml(
                tracked_files
            )
        )

        dependencies.extend(
            DependencyAnalyzer.parse_composer_json(
                tracked_files
            )
        )

        dependencies.extend(
            DependencyAnalyzer.parse_pom_xml(
                tracked_files
            )
        )

        dependencies.extend(
            DependencyAnalyzer.parse_build_gradle(
                tracked_files
            )
        )

        return dependencies