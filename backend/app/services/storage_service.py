from pathlib import Path
import uuid
import shutil
import zipfile
from app.core.config import settings

class StorageService:

    @staticmethod
    def get_storage_root() -> Path:
        root = Path(settings.upload_dir).resolve()
        root.mkdir(parents=True, exist_ok=True)
        return root

    @staticmethod
    def create_repository_directory() -> tuple[str, Path]:
        repository_id = str(uuid.uuid4())
        repository_path = StorageService.get_storage_root() / repository_id
        repository_path.mkdir(parents=True, exist_ok=True)
        return repository_id, repository_path

    @staticmethod
    def save_zip(repository_path: Path, uploaded_file) -> Path:
        zip_path = repository_path / "source.zip"
        with open(zip_path, "wb") as buffer:
            shutil.copyfileobj(uploaded_file.file, buffer)
        return zip_path    

    @staticmethod
    def extract_zip(zip_path: Path, repository_path: Path) -> Path:
        extract_path = (repository_path / "extracted").resolve()
        extract_path.mkdir(exist_ok=True)

        if not zipfile.is_zipfile(zip_path):
            raise ValueError("Uploaded file is not a valid ZIP archive")

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            if zip_ref.testzip() is not None:
                raise ValueError("Corrupt ZIP archive")

            members = zip_ref.infolist()
            if len(members) > settings.max_file_count:
                raise ValueError(f"ZIP contains too many files (max: {settings.max_file_count})")

            total_size = 0
            for member in members:
                # Exempt internal .git version control history files from individual file size limit
                is_git_internal = ".git/" in member.filename or ".git\\" in member.filename
                if not is_git_internal and member.file_size > settings.max_individual_file_size:
                    raise ValueError(f"File {member.filename} exceeds maximum individual file size limit")
                total_size += member.file_size
                if total_size > settings.max_extracted_size:
                    raise ValueError(f"Extracted content exceeds maximum size limit ({settings.max_extracted_size} bytes)")

                # Prevent ZIP Slip / Path Traversal
                target_path = (extract_path / member.filename).resolve()
                if not str(target_path).startswith(str(extract_path)):
                    raise ValueError(f"Path traversal attempt detected in ZIP entry: {member.filename}")

            # Safe to extract
            zip_ref.extractall(extract_path)

        # Remove the uploaded source zip to save disk space
        if zip_path.exists():
            zip_path.unlink()

        return extract_path


            