from app.services.storage_service import StorageService
repo_id, path = StorageService.create_repository_directory()

print(repo_id)
print(path)