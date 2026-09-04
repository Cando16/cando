from abc import ABC, abstractmethod
from pydantic import BaseModel

class ProviderStatus(BaseModel):
    reachable: bool
    models_available: list[str] = []
    error_message: str | None = None

class ProviderUnavailable(Exception):
    pass

class AIProvider(ABC):
    @abstractmethod
    async def complete(self, system: str, user: str, *, temperature: float) -> str:
        ...

    @abstractmethod
    async def test_connection(self) -> ProviderStatus:
        ...
