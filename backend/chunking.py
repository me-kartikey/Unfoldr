from app.services.chunking_service import ChunkingService
from app.services.embedding_service import EmbeddingService
from app.services.vector_store_service import VectorStoreService

document = """
# Project Overview

This project uses FastAPI and PostgreSQL.

## Authentication

JWT Authentication

## Database

PostgreSQL Database
"""

chunk_service = ChunkingService()
embedding_service = EmbeddingService()
vector_store = VectorStoreService()

chunks = chunk_service.chunk_document(document)

ids = []
documents = []
embeddings = []
metadatas = []

repository_id = "repo_1"

for chunk in chunks:

    ids.append(
        f"{repository_id}_{chunk['id']}"
    )

    documents.append(
        chunk["content"]
    )

    embeddings.append(
        embedding_service.generate_embedding(
            chunk["content"]
        )
    )

    metadatas.append(
        {
            "repository_id": repository_id,
            "title": chunk["title"]
        }
    )

vector_store.add_documents(
    ids=ids,
    documents=documents,
    embeddings=embeddings,
    metadatas=metadatas
)

print("Stored Successfully")