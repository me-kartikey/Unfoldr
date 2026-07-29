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
        """
        Generate embedding for a single text.
        """

        response = self.client.models.embed_content(
            model=self.model,
            contents=text,
        )

        return response.embeddings[0].values

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.
        """

        embeddings = []

        for text in texts:
            embeddings.append(
                self.generate_embedding(text)
            )

        return embeddings