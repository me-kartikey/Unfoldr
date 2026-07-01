from pathlib import Path
from app.analyzers.repository_analyzer import (
    RepositoryAnalyzer
)

repository_path = Path(
    "storage/repositories_collection/040957f6-4c80-4882-9ee5-743b518dad8c/extracted"
)

total_files = RepositoryAnalyzer.count_files(
    repository_path
)

print(
    f"Total Files: {total_files}"
)

extensions = (
    RepositoryAnalyzer.detect_extensions(
        repository_path
    )
)
print(
    f"Extensions: {extensions}"
)

languages = RepositoryAnalyzer.detect_languages(repository_path)
print(
    f"Languages: {languages}"
)
