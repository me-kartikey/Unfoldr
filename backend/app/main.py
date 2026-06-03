from fastapi import FastAPI

from app.core.config import settings


app = FastAPI(
    title=settings.app_name
)


@app.get("/")
async def health_check():
    return {
        "app": settings.app_name,
        "environment": settings.environment,
        "status": "healthy"
    }