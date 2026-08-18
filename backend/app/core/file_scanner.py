import os
from pathlib import Path

# Edited on 2026-08-13: Added recursive directory scanner that skips ignored directories (e.g. node_modules, .git, venv) to optimize file system traversal.

IGNORE_FOLDERS = {
    "node_modules",
    ".git",
    "venv",
    "venv_linux",
    "__pycache__",
    ".pytest_cache",
    ".idea",
    ".vscode",
    "dist",
    "build",
    "target",
    "out",
    "storage"
}

class FileScanner:
    @staticmethod
    def scan_repository(repository_path: Path) -> list[Path]:
        tracked_files = []
        repo_abs = repository_path.resolve()
        
        for root, dirs, files in os.walk(repo_abs):
            # Modify dirs in-place to prevent os.walk from descending into ignored directories
            dirs[:] = [d for d in dirs if d not in IGNORE_FOLDERS]
            
            for file in files:
                file_path = Path(root) / file
                tracked_files.append(file_path)
                
        return tracked_files
