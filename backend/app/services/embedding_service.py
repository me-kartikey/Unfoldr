from typing import List

from google import genai

from app.core.config import settings


class EmbeddingService:
    def __init__(self):
        self.client = genai.Client(
            api_key=settings.google_api_key
        )

        self.model = "gemini-embedding-001"

    def generate_embedding(self, text: str) -> List[float]:
        # Edited on 2026-08-13: Preserved generate_embedding single text interface with single retry fallback.
        import time
        max_retries = 3
        delay = 2.0
        for attempt in range(max_retries):
            try:
                response = self.client.models.embed_content(
                    model=self.model,
                    contents=text,
                )
                return response.embeddings[0].values
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                time.sleep(delay)
                delay *= 2.0

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        # Edited on 2026-08-13: Refactored generate_embeddings to utilize controlled batching (max size 16) and rate-limit-safe retries with exponential backoff.
        import time
        batch_size = 16
        all_embeddings = []
        max_retries = 3

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            delay = 2.0
            for attempt in range(max_retries):
                try:
                    response = self.client.models.embed_content(
                        model=self.model,
                        contents=batch,
                    )
                    batch_vals = [emb.values for emb in response.embeddings]
                    all_embeddings.extend(batch_vals)
                    break
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    time.sleep(delay)
                    delay *= 2.0

        return all_embeddings