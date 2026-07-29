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

    def add_documents(
        self,
        ids: list[str],
        documents: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict]
    ):
        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

    def search(
        self,
        query_embedding: list[float],
        repository_id: str,
        n_results: int = 3
    ):
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where={
                "repository_id": repository_id
            },
            include=[
                "documents",
                "metadatas",
                "distances"
            ]
        )