"""Health check endpoint."""
from fastapi import APIRouter

from ..config import get_settings

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/")
def health() -> dict[str, str]:
    settings = get_settings()
    return {
        "status": "ok",
        "environment": settings.env,
    }
