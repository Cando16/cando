import pytest
from backend.providers.null_provider import NullProvider
from backend.providers.base import ProviderUnavailable
from backend.providers import get_provider
from backend.config import settings

@pytest.mark.asyncio
async def test_null_provider():
    provider = NullProvider()
    
    status = await provider.test_connection()
    assert not status.reachable
    assert status.error_message == "NullProvider configured."
    
    with pytest.raises(ProviderUnavailable):
        await provider.complete("sys", "user", temperature=0.0)

def test_get_provider_null():
    original = settings.CANDO_AI_PROVIDER
    settings.CANDO_AI_PROVIDER = "none"
    try:
        provider = get_provider()
        assert isinstance(provider, NullProvider)
    finally:
        settings.CANDO_AI_PROVIDER = original
