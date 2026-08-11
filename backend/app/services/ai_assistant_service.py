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
        # Edited on 2026-08-11: Increased search top-k results from 3 to 10 to fetch all short markdown sections.
        query_embedding = self.embedding_service.generate_embedding(
            question
        )

        results = self.vector_store.search(
            query_embedding=query_embedding,
            repository_id=repository_id,
            n_results=10
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
        # Edited on 2026-08-11: Refined prompt rules to support answering general queries as well as repository documentation.
        context, sources = self.retrieve_context(
            repository_id,
            question
        )

        prompt = f"""
You are an AI Developer Onboarding Assistant.

Your task is to answer the user's question using the repository documentation provided below.

Rules:
1. Use the retrieved repository context when answering repository-specific questions (regarding directory structures, language configuration, databases, dependencies, or framework details).
2. If the retrieved context contains the answer, answer directly. Do not claim the information is missing when it is present.
3. If the user question is general (e.g. general programming concepts, algorithms, syntax explanations, or frameworks definitions) and the repository context does not contain the answer, answer using your general knowledge.
4. If the question is repository-specific and the answer is NOT present in the documentation, reply:
   "I couldn't find that information in the repository documentation."
5. Give a clear, professional, and natural explanation. Do not copy documentation verbatim unless necessary.

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