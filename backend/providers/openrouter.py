import httpx
from backend.providers.base import AIProvider, ProviderStatus, ProviderUnavailable
from backend.config import settings

class OpenRouterProvider(AIProvider):
    BASE_URL = "https://openrouter.ai/api/v1"

    async def complete(self, system: str, user: str, *, temperature: float) -> str:
        if not settings.OPENROUTER_API_KEY:
            raise ProviderUnavailable("OpenRouter API key is missing.")

        model = settings.OPENROUTER_MODEL
        if not model:
            raise ProviderUnavailable("OpenRouter model is not configured.")

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.BASE_URL}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                        "HTTP-Referer": "http://localhost:5173", # Dev URL
                        "X-Title": "CANDO"
                    },
                    json={
                        "model": model,
                        "messages": [
                            {"role": "system", "content": system},
                            {"role": "user", "content": user}
                        ],
                        "temperature": temperature
                    },
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
            except Exception as e:
                raise ProviderUnavailable(f"OpenRouter request failed: {e}")

    async def test_connection(self) -> ProviderStatus:
        if not settings.OPENROUTER_API_KEY:
            return ProviderStatus(reachable=False, error_message="OpenRouter API key is missing.")

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.BASE_URL}/models",
                    timeout=10.0
                )
                response.raise_for_status()
                data = response.json()
                
                # Filter zero-cost models
                free_models = [
                    m["id"] for m in data.get("data", [])
                    if m.get("pricing", {}).get("prompt", "") == "0" and m.get("pricing", {}).get("completion", "") == "0"
                ]
                
                return ProviderStatus(reachable=True, models_available=free_models)
            except Exception as e:
                return ProviderStatus(reachable=False, error_message=f"Failed to fetch models: {e}")
