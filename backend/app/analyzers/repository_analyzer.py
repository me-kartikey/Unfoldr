from pathlib import Path
from app.core.constants import EXTENSION_LANGUAGE_MAP
from app.core.constants import FRAMEWORK_PATTERNS
from app.core.constants import LIBRARY_PATTERNS

class RepositoryAnalyzer:

# count the total number of files in the repository
    @staticmethod
    def count_files(
        repository_path: Path
    ) -> int:

        total_files = 0

        for item in repository_path.rglob("*"):
            if item.is_file():
                total_files += 1

        return total_files
    
    # detect the extensions of the files in the repository
    @staticmethod
    def detect_extensions(
        repository_path: Path
    ) -> set[str]:

        extensions = set()

        for item in repository_path.rglob("*"):
            if item.is_file():
                extensions.add(item.suffix.lower())

        return extensions
    
    # detect the programming languages used in the repository based on the file extensions
    @staticmethod
    def detect_languages(
    repository_path: Path
    ) -> set[str]:
        languages = set()
        extensions = RepositoryAnalyzer.detect_extensions(repository_path)
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

        total_files = RepositoryAnalyzer.count_files(repository_path)
        extensions = RepositoryAnalyzer.detect_extensions(repository_path)
        languages = RepositoryAnalyzer.detect_languages(repository_path)
        frameworks = RepositoryAnalyzer.detect_frameworks(repository_path)
        libraries = RepositoryAnalyzer.detect_libraries(repository_path)

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
        repository_path: Path
        ) -> set[str]:

            frameworks = set()
            for item in repository_path.rglob("*"):
                if (item.is_file() and item.name in FRAMEWORK_PATTERNS):
                    content = item.read_text(
                    encoding="utf-8",
                    errors="ignore"
                ).lower()
                    for keyword, framework in FRAMEWORK_PATTERNS[item.name].items():
                        if keyword.lower() in content:
                            frameworks.add(framework)
            return frameworks
        
     # detect the libraries used in the repository based on the presence of specific files and keywords
    @staticmethod
    def detect_libraries(
        repository_path: Path
        ) -> set[str]:

            libraries = set()
            for item in repository_path.rglob("*"):
                if (item.is_file() and item.name in LIBRARY_PATTERNS):
                    content = item.read_text(
                    encoding="utf-8",
                    errors="ignore"
                ).lower()
                    for keyword, library in LIBRARY_PATTERNS[item.name].items():
                        if keyword.lower() in content:
                            libraries.add(library)
            return libraries



      



 
  