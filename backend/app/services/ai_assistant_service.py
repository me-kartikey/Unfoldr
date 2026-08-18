import re
from pathlib import Path
from google import genai

from app.core.config import settings
from app.services.embedding_service import EmbeddingService
from app.services.vector_store_service import VectorStoreService
from app.db.session import session_local
from app.repositories.repository_repository import RepositoryRepository


class AIAssistantService:

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.google_api_key
        )

        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStoreService()

        self.model = "gemini-2.5-flash"

    def retrieve_context(
        self,
        repository_id: str,
        question: str
    ):
        query_embedding = self.embedding_service.generate_embedding(
            question
        )

        results = self.vector_store.search(
            query_embedding=query_embedding,
            repository_id=repository_id,
            n_results=10
        )

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]

        context = "\n\n".join(documents)

        sources = []

        for metadata in metadatas:
            title = metadata.get("title")

            if title and title not in sources:
                sources.append(title)

        return context, sources

    def _get_repository_root(self, repository_id: str) -> Path | None:
        """Find the root path where repository files are unzipped."""
        db = session_local()
        try:
            repository = RepositoryRepository.get_by_id(db, repository_id)
            if not repository or not repository.storage_path:
                return None
            extracted_path = Path(repository.storage_path) / "extracted"
            if not extracted_path.exists():
                return None
            # Find first nested directory if present, otherwise use extracted_path
            try:
                repository_root = next(
                    item for item in extracted_path.iterdir() if item.is_dir()
                )
            except StopIteration:
                repository_root = extracted_path
            return repository_root
        except Exception as e:
            print(f"Error resolving repository root: {e}")
            return None
        finally:
            db.close()

    def _get_codebase_files(self, repository_root: Path) -> list[Path]:
        """Collect all text/code files recursively, ignoring environment and git folders."""
        file_paths = []
        ignored_patterns = {".git", "__pycache__", "node_modules", ".venv", "venv", ".idea", ".vscode", "dist", "build"}
        valid_extensions = {
            ".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".go", ".cpp", ".c", ".h", 
            ".cs", ".php", ".rb", ".rs", ".swift", ".kt", ".kts", ".sql", ".sh", 
            ".html", ".css", ".json", ".yaml", ".yml", ".md", ".txt", ".xml", ".properties", ".gradle"
        }
        try:
            for item in repository_root.rglob("*"):
                if item.is_file() and item.suffix.lower() in valid_extensions:
                    if not any(part in ignored_patterns for part in item.parts):
                        file_paths.append(item)
        except Exception as e:
            print(f"Error collecting codebase files: {e}")
        return file_paths

    def _find_referenced_files(self, question: str, file_paths: list[Path], repository_root: Path) -> list[Path]:
        """Identify files mentioned explicitly in the question."""
        matched = []
        question_lower = question.lower()
        for path in file_paths:
            try:
                rel_path = path.relative_to(repository_root)
                rel_path_str = str(rel_path).replace("\\", "/").lower()
                filename = path.name.lower()
                if filename in question_lower or rel_path_str in question_lower:
                    matched.append(path)
            except Exception:
                pass
        return matched

    def _find_symbol_files(self, question: str, file_paths: list[Path]) -> list[Path]:
        """Identify files declaring class, function, or interface symbols mentioned in the question."""
        words = re.findall(r"\b[a-zA-Z_][a-zA-Z0-9_]*\b", question)
        matched = []
        ignored_words = {
            "class", "def", "function", "import", "from", "return", "const", "let", 
            "var", "public", "private", "interface", "void", "async", "await",
            "what", "where", "when", "does", "how", "explain", "code", "file",
            "folder", "path", "database", "connection", "login", "auth", "user"
        }
        target_words = [w for w in words if w.lower() not in ignored_words and len(w) >= 3]
        if not target_words:
            return matched
            
        for path in file_paths:
            if len(matched) >= 3:
                break
            try:
                content = path.read_text(errors="ignore")
                for word in target_words:
                    pattern = r"\b(class|def|function|interface|struct)\s+" + re.escape(word) + r"\b"
                    if re.search(pattern, content):
                        if path not in matched:
                            matched.append(path)
                            break
            except Exception:
                pass
        return matched

    def _load_file_contents(self, file_paths: list[Path], repository_root: Path) -> tuple[str, list[str]]:
        """Read and format the content of matched files within safe token boundaries."""
        context_parts = []
        retrieved_sources = []
        max_chars_per_file = 80000
        for path in file_paths:
            try:
                rel_path = path.relative_to(repository_root)
                rel_path_str = str(rel_path).replace("\\", "/")
                content = path.read_text(errors="ignore")
                if len(content) > max_chars_per_file:
                    content = content[:max_chars_per_file] + "\n\n... [Content Truncated due to size constraints] ..."
                context_parts.append(f"--- START FILE: {rel_path_str} ---\n{content}\n--- END FILE: {rel_path_str} ---")
                retrieved_sources.append(rel_path_str)
            except Exception as e:
                print(f"Error reading file {path}: {e}")
        return "\n\n".join(context_parts), retrieved_sources

    def ask_question(
        self,
        repository_id: str,
        question: str
    ) -> str:
        rag_context, sources = self.retrieve_context(
            repository_id,
            question
        )

        source_code_context = ""
        source_files = []
        
        # Edited on 14-08-2026: Enhanced AI Assistant to load codebase file contents dynamically when users ask about files, classes, or functions.
        root_path = self._get_repository_root(repository_id)
        if root_path:
            all_files = self._get_codebase_files(root_path)
            matched_files = self._find_referenced_files(question, all_files, root_path)
            if not matched_files:
                matched_files = self._find_symbol_files(question, all_files)
            if matched_files:
                source_code_context, source_files = self._load_file_contents(matched_files, root_path)
                for src in source_files:
                    if src not in sources:
                        sources.append(src)

        prompt = f"""
You are an AI Developer Onboarding Assistant.

Your task is to answer the user's question using the repository documentation and source code files provided below.

Rules:
1. Use the provided Source Code Files first when answering questions about specific files, functions, classes, imports, database configurations, or execution flow.
2. If the user question is general (e.g. general programming concepts, algorithms, syntax explanations, or frameworks definitions) and the repository context does not contain the answer, answer using your general knowledge.
3. If the question is repository-specific (regarding files, classes, configurations, dependencies, ORMs) and the answer is NOT present in either the source code or documentation context, reply:
   "I couldn't find that information in the repository source code or documentation."
4. If a file is explicitly asked about, base your explanation on its actual code content and explain, where applicable:
   - Purpose of the file
   - Its role in the project
   - Imports and their purpose
   - Classes and functions
   - Important variables
   - Execution/control flow
   - Dependencies on other project files
   - APIs/routes handled
   - How it interacts with the rest of the application
   - Important points for a new developer
5. Give a clear, professional, and natural explanation.

Source Code Files:
{source_code_context if source_code_context else "[No specific source code matched for this query]"}

Repository Documentation:
{rag_context}

User Question:
{question}

Answer:
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        return {
            "answer": response.text,
            "sources": sources
        }