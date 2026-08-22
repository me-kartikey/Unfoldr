from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.middleware.base import BaseHTTPMiddleware
import hmac
import hashlib

from app.api.routes.chat import router as chat_router
from app.api.routes.auth import router as auth_router
from app.api.v1.repositories import router as repository_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
import app.models.user
import app.models.repository

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title=settings.app_name
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CSRF Middleware
class CSRFMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method in ["POST", "PUT", "DELETE", "PATCH"]:
            # Skip CSRF for login/register
            if request.url.path.rstrip("/") in ["/auth/login", "/auth/register"]:
                return await call_next(request)
            
            token = request.cookies.get("access_token")
            csrf_token_header = request.headers.get("x-csrf-token")
            
            if not token or not csrf_token_header:
                return JSONResponse(
                    status_code=status.HTTP_403_FORBIDDEN,
                    content={"detail": "CSRF token missing"}
                )
                
            expected_csrf = hmac.new(
                settings.csrf_secret_key.encode(),
                token.encode(),
                hashlib.sha256
            ).hexdigest()
            
            if not hmac.compare_digest(csrf_token_header, expected_csrf):
                return JSONResponse(
                    status_code=status.HTTP_403_FORBIDDEN,
                    content={"detail": "CSRF token mismatch"}
                )
        return await call_next(request)

app.add_middleware(CSRFMiddleware)

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the newly created authentication routes
app.include_router(auth_router)
app.include_router(repository_router)
app.include_router(chat_router)

@app.on_event("startup")
async def startup_event():
    import logging
    logger = logging.getLogger("uvicorn")
    logger.info(f"Loaded CORS Allowed Origins: {settings.allowed_origins}")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables verified/created successfully.")

@app.get("/health")
async def health_check():
    return {
        "app": settings.app_name,
        "environment": settings.environment,
        "status": "healthy",
        "allowed_origins": settings.allowed_origins
    }