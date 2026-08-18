
from fastapi import APIRouter, Depends

from app.schemas.chat import (
    ChatRequest,
    ChatResponse
)
from app.services.ai_assistant_service import (
    AIAssistantService
)
from app.api.deps import check_repository_owner
from app.models.repository import Repository

# Edited on 13-08-2026: Protect the chat endpoint via check_repository_owner authorization

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
    request: ChatRequest,
    repository: Repository = Depends(check_repository_owner)
):

    response = assistant.ask_question(
        repository_id=repository_id,
        question=request.question
    )

    return ChatResponse(
        answer=response["answer"],
        sources=response["sources"]
        
    )