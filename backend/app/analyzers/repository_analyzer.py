from pathlib import Path
from app.core.constants import EXTENSION_LANGUAGE_MAP
from app.core.constants import FRAMEWORK_PATTERNS
from app.core.constants import LIBRARY_PATTERNS

class RepositoryAnalyzer:

# count the total number of files in the repository
    @staticmethod
    def count_files(
        tracked_files: list[Path]
    ) -> int:
        # Edited on 2026-08-13: Refactored to count from pre-scanned file list
        return len(tracked_files)
    
    # detect the extensions of the files in the repository
    @staticmethod
    def detect_extensions(
        tracked_files: list[Path]
    ) -> set[str]:
        # Edited on 2026-08-13: Refactored to extract extensions from pre-scanned file list
        extensions = set()
        for item in tracked_files:
            extensions.add(item.suffix.lower())
        return extensions
    
    # detect the programming languages used in the repository based on the file extensions
    @staticmethod
    def detect_languages(
        extensions: set[str]
    ) -> set[str]:
        # Edited on 2026-08-13: Refactored to check from pre-scanned extensions list
        languages = set()
        for ext in extensions:
            language=EXTENSION_LANGUAGE_MAP.get(ext)
            if language:
                languages.add(language)
        return languages
        
      # analyze the repository and return a dictionary with the total number of files, extensions, and languages
    @staticmethod
    def analyze_repository(
        repository_path: Path
    ) -> dict[str, any]:
        # Edited on 2026-08-13: Refactored to index repository files once and reuse the tracked files list
        from app.core.file_scanner import FileScanner

        tracked_files = FileScanner.scan_repository(repository_path)

        total_files = RepositoryAnalyzer.count_files(tracked_files)
        extensions = RepositoryAnalyzer.detect_extensions(tracked_files)
        languages = RepositoryAnalyzer.detect_languages(extensions)
        frameworks = RepositoryAnalyzer.detect_frameworks(tracked_files)
        libraries = RepositoryAnalyzer.detect_libraries(tracked_files)

        print("\n===== ANALYZER DEBUG =====")
        print(f"Repository Path: {repository_path}")
        print(f"Total Files: {total_files}")
        print(f"Extensions: {extensions}")
        print(f"Languages: {languages}")
        print(f"Frameworks: {frameworks}")
        print(f"Libraries: {libraries}")
        print("==========================\n")

        return {
            "total_files": total_files,
            "extensions": extensions,
            "languages": languages,
            "frameworks": frameworks,
            "libraries": libraries
        }
    
    # detect the frameworks used in the repository based on the presence of specific files and keywords
    @staticmethod
    def detect_frameworks(
        tracked_files: list[Path]
    ) -> set[str]:
        # Edited on 2026-08-13: Refactored to filter framework configuration files in-memory
        frameworks = set()
        for item in tracked_files:
            if item.name in FRAMEWORK_PATTERNS:
                try:
                    content = item.read_text(
                        encoding="utf-8",
                        errors="ignore"
                    ).lower()
                    for keyword, framework in FRAMEWORK_PATTERNS[item.name].items():
                        if keyword.lower() in content:
                            frameworks.add(framework)
                except Exception:
                    continue
        return frameworks
        
     # detect the libraries used in the repository based on the presence of specific files and keywords
    @staticmethod
    def detect_libraries(
        tracked_files: list[Path]
    ) -> set[str]:
        # Edited on 2026-08-13: Refactored to filter library configuration files in-memory
        libraries = set()
        for item in tracked_files:
            if item.name in LIBRARY_PATTERNS:
                try:
                    content = item.read_text(
                        encoding="utf-8",
                        errors="ignore"
                    ).lower()
                    for keyword, library in LIBRARY_PATTERNS[item.name].items():
                        if keyword.lower() in content:
                            libraries.add(library)
                except Exception:
                    continue
        return libraries



      



 
  