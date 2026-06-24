from pathlib import Path
from app.analyzers.repository_analyzer import (
    RepositoryAnalyzer
)

repository_path = Path(
    "storage/repositories_collection/81f5dc0a-76ae-457d-a0a9-29b71a2513b7/extracted"
)

total_files = RepositoryAnalyzer.count_files(
    repository_path
)

print(
    f"Total Files: {total_files}"
)