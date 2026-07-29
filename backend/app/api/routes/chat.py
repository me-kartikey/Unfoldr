
from fastapi import APIRouter

from app.schemas.chat import (
    ChatRequest,
    ChatResponse
)
from app.services.ai_assistant_service import (
    AIAssistantService
)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

assistant = AIAssistantService()


@router.post(
    "/{repository_id}",
    response_model=ChatResponse
)
def chat(
    repository_id: str,
    request: ChatRequest
):

    response = assistant.ask_question(
        repository_id=repository_id,
        question=request.question
    )

    return ChatResponse(
        answer=response["answer"],
        sources=response["sources"]
        
    )