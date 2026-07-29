from fastapi import FastAPI
from app.api.routes.chat import router as chat_router

from app.core.config import settings
from app.api.v1.repositories import router as repository_router

app = FastAPI(
    title=settings.app_name
)

app.include_router(repository_router)
app.include_router(chat_router)

@app.get("/")
async def health_check():
    return {
        "app": settings.app_name,
        "environment": settings.environment,
        "status": "healthy"
    }