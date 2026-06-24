from pathlib import Path


class RepositoryAnalyzer:

    @staticmethod
    def count_files(
        repository_path: Path
    ) -> int:

        total_files = 0

        for item in repository_path.rglob("*"):
            if item.is_file():
                total_files += 1

        return total_files
    
    @staticmethod
    def detect_extensions(
        repository_path: Path
    ) -> set[str]:

        extensions = set()

        for item in repository_path.rglob("*"):
            if item.is_file():
                extensions.add(item.suffix.lower())

        return extensions