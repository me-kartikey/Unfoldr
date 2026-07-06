from pathlib import Path


class DependencyAnalyzer:

    @staticmethod
    def parse_requirements_txt(repository_path: Path) -> list[dict]:

        dependencies = []

        requirements_file = repository_path / "requirements.txt"

        if not requirements_file.exists():
            return dependencies

        with requirements_file.open(encoding="utf-8") as file:

            for line in file:

                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                version = None

                for operator in ["==", ">=", "<=", "~=", "!=", ">", "<"]:

                    if operator in line:

                        name, version = line.split(operator, 1)

                        dependencies.append(
                            {
                                "name": name.strip(),
                                "version": operator + version.strip(),
                                "language": "Python",
                                "package_manager": "pip",
                                "dependency_type": "production",
                            }
                        )

                        break

                else:

                    dependencies.append(
                        {
                            "name": line,
                            "version": None,
                            "language": "Python",
                            "package_manager": "pip",
                            "dependency_type": "production",
                        }
                    )

        return dependencies

    @staticmethod
    def detect_dependencies(repository_path: Path) -> list[dict]:

        dependencies = []

        dependencies.extend(DependencyAnalyzer.parse_requirements_txt(repository_path))

        # Future
        # dependencies.extend(
        #     DependencyAnalyzer.parse_package_json(
        #         repository_path
        #     )
        # )

        # dependencies.extend(
        #     DependencyAnalyzer.parse_pyproject_toml(
        #         repository_path
        #     )
        # )

        return dependencies
