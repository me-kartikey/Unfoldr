from pathlib import Path
import uuid
import shutil
import zipfile

class StorageService:

    STORAGE_ROOT = Path("storage/repositories_collection")
    # created for create the folder
    @staticmethod
    def create_repository_directory() -> tuple[str, Path]:
        repository_id = str(uuid.uuid4())
        repository_path = StorageService.STORAGE_ROOT / repository_id
        repository_path.mkdir(parents=True, exist_ok=True)
        return repository_id, repository_path
    # for saving the zip file
    @staticmethod
    def save_zip(
        repository_path: Path,
        uploaded_file) -> Path:
        zip_path = repository_path / "source.zip"

        with open(zip_path, "wb") as buffer:
            shutil.copyfileobj(uploaded_file.file, buffer)
            return zip_path    
        #  for extracting
    @staticmethod
    def extract_zip(
    zip_path: Path,
    repository_path: Path
    ) -> Path:

        extract_path = repository_path / "extracted"

        extract_path.mkdir(
        exist_ok=True
        )

        with zipfile.ZipFile(
        zip_path,
        "r"
        ) as zip_ref:

            zip_ref.extractall(
            extract_path
         )

        return extract_path   

            