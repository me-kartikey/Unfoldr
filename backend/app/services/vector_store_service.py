from pathlib import Path

from chromadb import PersistentClient

from app.core.config import settings


class VectorStoreService:

    def __init__(self):
        Path(settings.chroma_db_path).mkdir(
            parents=True,
            exist_ok=True
        )

        self.client = PersistentClient(
            path=settings.chroma_db_path
        )

        self.collection = self.client.get_or_create_collection(
            name=settings.chroma_collection_name
        )