from fastapi import FastAPI
from app.api.v1.endpoints import router as api_router
from app.core.config import settings

app = FastAPI(title=settings.app_name)

app.include_router(api_router, prefix="/api/v1")