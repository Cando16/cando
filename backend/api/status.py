from fastapi import APIRouter
from pydantic import BaseModel
from backend.config import settings
from backend.providers import get_provider

router = APIRouter()

class StatusResponse(BaseModel):
    version: str
    provider_configured: bool
    provider_reachable: bool

@router.get("/status", response_model=StatusResponse)
async def get_status():
    provider = get_provider()
    status = await provider.test_connection()
    
    return StatusResponse(
        version="0.1.0",
        provider_configured=bool(settings.OPENROUTER_API_KEY) if settings.CANDO_AI_PROVIDER == "openrouter" else True,
        provider_reachable=status.reachable
    )
