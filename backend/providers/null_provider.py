from backend.providers.base import AIProvider, ProviderStatus, ProviderUnavailable

class NullProvider(AIProvider):
    async def complete(self, system: str, user: str, *, temperature: float) -> str:
        raise ProviderUnavailable("AI provider is unavailable (NullProvider configured).")

    async def test_connection(self) -> ProviderStatus:
        return ProviderStatus(reachable=False, error_message="NullProvider configured.")
