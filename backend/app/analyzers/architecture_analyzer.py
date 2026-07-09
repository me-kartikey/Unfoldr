from pathlib import Path


ENTRY_POINTS = [
    "main.py",
    "app.py",
    "manage.py",
    "server.py",
    "index.js",
    "server.js",
    "main.js",
    "index.ts",
    "main.ts",
    "Program.cs"
]

CONFIG_FILES = [
    "requirements.txt",
    "package.json",
    "pyproject.toml",
    "Dockerfile",
    "docker-compose.yml",
    ".env",
    ".env.example",
    "README.md",
    ".gitignore"
]


class ArchitectureAnalyzer:

    @staticmethod
    def analyze_repository(
        repository_path: Path
    ) -> dict:

        root_folders = []
        entry_points = []
        config_files = []

        for item in repository_path.iterdir():

            if item.is_dir():

                root_folders.append(item.name)

            elif item.name in ENTRY_POINTS:

                entry_points.append(item.name)

            if item.name in CONFIG_FILES:

                config_files.append(item.name)

        return {
            "project_type": "Unknown",
            "entry_points": sorted(entry_points),
            "root_folders": sorted(root_folders),
            "config_files": sorted(config_files)
        }