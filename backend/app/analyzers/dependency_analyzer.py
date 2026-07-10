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
        repository_path: Path
    ) -> list[dict]:

        dependencies = []

        for requirements_file in repository_path.rglob(
            "requirements.txt"
        ):

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
        repository_path: Path
    ) -> list[dict]:

        dependencies = []

        for package_file in repository_path.rglob(
            "package.json"
        ):

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
        repository_path: Path
    ) -> list[dict]:

        dependencies = []

        for pyproject_file in repository_path.rglob(
            "pyproject.toml"
        ):

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
        repository_path: Path
    ) -> list[dict]:

        dependencies = []

        for pipfile in repository_path.rglob(
            "Pipfile"
        ):

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
        repository_path: Path
    ) -> list[dict]:

        dependencies = []

        for go_mod in repository_path.rglob(
            "go.mod"
        ):

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
        repository_path: Path
    ) -> list[dict]:

        dependencies = []

        for cargo_file in repository_path.rglob(
            "Cargo.toml"
        ):

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
        repository_path: Path
    ) -> list[dict]:

        dependencies = []

        for composer_file in repository_path.rglob(
            "composer.json"
        ):

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
        repository_path: Path
    ) -> list[dict]:

        dependencies = []

        for pom_file in repository_path.rglob(
            "pom.xml"
        ):

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
        repository_path: Path
    ) -> list[dict]:

        dependencies = []

        gradle_files = list(
            repository_path.rglob("build.gradle")
        )

        gradle_files.extend(
            repository_path.rglob(
                "build.gradle.kts"
            )
        )

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

        dependencies = []

        dependencies.extend(
            DependencyAnalyzer.parse_requirements_txt(
                repository_path
            )
        )

        dependencies.extend(
            DependencyAnalyzer.parse_package_json(
                repository_path
            )
        )

        dependencies.extend(
            DependencyAnalyzer.parse_pyproject_toml(
                repository_path
            )
        )

        dependencies.extend(
            DependencyAnalyzer.parse_pipfile(
                repository_path
            )
        )

        dependencies.extend(
            DependencyAnalyzer.parse_go_mod(
                repository_path
            )
        )

        dependencies.extend(
            DependencyAnalyzer.parse_cargo_toml(
                repository_path
            )
        )

        dependencies.extend(
            DependencyAnalyzer.parse_composer_json(
                repository_path
            )
        )

        dependencies.extend(
            DependencyAnalyzer.parse_pom_xml(
                repository_path
            )
        )

        dependencies.extend(
            DependencyAnalyzer.parse_build_gradle(
                repository_path
            )
        )

        return dependencies