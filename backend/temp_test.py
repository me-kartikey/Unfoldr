from app.services.chunking_service import ChunkingService

doc = """
# Project Overview

This project is an AI onboarding platform.

## Languages

- Python
- JavaScript

## Frameworks

- FastAPI
- React

## Database

- PostgreSQL
"""

chunks = ChunkingService.chunk_document(doc)

for chunk in chunks:
    print(chunk)