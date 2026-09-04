import httpx
from backend.providers.base import AIProvider, ProviderStatus, ProviderUnavailable

class OllamaProvider(AIProvider):
    BASE_URL = "http://127.0.0.1:11434/api"

    async def complete(self, system: str, user: str, *, temperature: float) -> str:
        # Just stubbed out for now, assuming model is "llama3" or something similar
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.BASE_URL}/generate",
                    json={
                        "model": "llama3", # Would come from settings
                        "system": system,
                        "prompt": user,
                        "stream": False,
                        "options": {
                            "temperature": temperature
                        }
                    },
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                return data["response"]
            except Exception as e:
                raise ProviderUnavailable(f"Ollama request failed: {e}")

    async def test_connection(self) -> ProviderStatus:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.BASE_URL}/tags",
                    timeout=5.0
                )
                response.raise_for_status()
                data = response.json()
                models = [m["name"] for m in data.get("models", [])]
                return ProviderStatus(reachable=True, models_available=models)
            except Exception as e:
                return ProviderStatus(reachable=False, error_message=f"Ollama not reachable: {e}")
