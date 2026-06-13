from pathlib import Path

from app.services.storage_service import StorageService


class FakeUploadFile:
    def __init__(self, file_path: str):
        self.file = open(file_path, "rb")


repo_id, repo_path = (
    StorageService.create_repository_directory()
)

print("Repository ID:", repo_id)
print("Repository Path:", repo_path)

uploaded_file = FakeUploadFile(
    "sample_testing.zip"
)

zip_path = StorageService.save_zip(
    repo_path,
    uploaded_file
)

print("ZIP Path:", zip_path)

extract_path = StorageService.extract_zip(
    zip_path,
    repo_path
)

print("Extract Path:", extract_path)