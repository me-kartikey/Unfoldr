from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.chat import router as chat_router
from app.api.v1.repositories import router as repository_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name
)

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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