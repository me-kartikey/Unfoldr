from google import genai

from app.core.config import settings
from app.services.embedding_service import EmbeddingService
from app.services.vector_store_service import VectorStoreService


class AIAssistantService:

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.google_api_key
        )

        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStoreService()

        self.model = "gemini-2.5-flash"

    def retrieve_context(
        self,
        repository_id: str,
        question: str
    ):

        query_embedding = self.embedding_service.generate_embedding(
            question
        )

        results = self.vector_store.search(
            query_embedding=query_embedding,
            repository_id=repository_id
        )

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]

        context = "\n\n".join(documents)

        sources = []

        for metadata in metadatas:
            title = metadata.get("title")

            if title and title not in sources:
                sources.append(title)

        return context, sources

    def ask_question(
        self,
        repository_id: str,
        question: str
    ) -> str:

        context, sources = self.retrieve_context(
            repository_id,
            question
        )

        prompt = f"""
You are an AI Developer Onboarding Assistant.

Your task is to answer the user's question using ONLY the repository documentation provided below.

Rules:
1. Give a clear and natural explanation.
2. Do not copy the documentation verbatim unless necessary.
3. Do not make up information.
4. If the answer is not present in the documentation, reply:
   "I couldn't find that information in the repository documentation."

Repository Documentation:
{context}

User Question:
{question}

Answer:
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        return{
            "answer": response.text,
            "sources": sources
        }