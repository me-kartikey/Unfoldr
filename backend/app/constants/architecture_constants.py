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
    ".gitignore",
    "vite.config.js",
    "vite.config.ts",
    "next.config.js",
    "composer.json",
    "pom.xml",
    "build.gradle"
]

LAYERED_FOLDERS = {
    "controllers",
    "services",
    "repositories",
    "models",
    "schemas",
    "routes",
    "middlewares"
}

MVC_FOLDERS = {
    "controllers",
    "models",
    "views"
}

CLEAN_ARCHITECTURE_FOLDERS = {
    "domain",
    "application",
    "infrastructure",
    "presentation"
}

MICROSERVICE_HINTS = {
    "docker-compose.yml",
    "kubernetes",
    "helm"
}

IGNORE_FOLDERS = {
    ".git",
    ".github",
    ".vscode",
    ".idea",
    "__pycache__",
    "node_modules",
    "venv",
    ".venv",
    "dist",
    "build"
}

HEXAGONAL_FOLDERS = {
    "adapters",
    "ports"
}


@staticmethod
def detect_architecture_pattern(
    root_folders: list[str]
) -> str:

    folders = {
        folder.lower()
        for folder in root_folders
    }

    if LAYERED_FOLDERS.issubset(folders):
        return "Layered"

    if MVC_FOLDERS.issubset(folders):
        return "MVC"

    if CLEAN_ARCHITECTURE_FOLDERS.issubset(folders):
        return "Clean Architecture"

    return "Unknown"