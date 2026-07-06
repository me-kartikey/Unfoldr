from pathlib import Path

from app.analyzers.dependency_analyzer import (
    DependencyAnalyzer
)

repository_path = Path(
    "storage/repositories_collection/66dd93d1-3ba6-40f2-bcf3-83792c884b7a/extracted/mine"
)

dependencies = (
    DependencyAnalyzer.detect_dependencies(
        repository_path
    )
)

print(dependencies)