from backend.config import settings
from backend.providers.base import AIProvider
from backend.providers.openrouter import OpenRouterProvider
from backend.providers.ollama import OllamaProvider
from backend.providers.null_provider import NullProvider

def get_provider() -> AIProvider:
    provider = settings.CANDO_AI_PROVIDER.lower()
    if provider == "openrouter":
        return OpenRouterProvider()
    elif provider == "ollama":
        return OllamaProvider()
    else:
        return NullProvider()
