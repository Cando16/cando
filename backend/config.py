from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    CANDO_AI_PROVIDER: str = "openrouter"
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_MODEL: str = ""

    CANDO_HOST: str = "127.0.0.1"
    CANDO_PORT: int = 8765

    CANDO_HISTORY_ENABLED: bool = True
    CANDO_LOCAL_CLEANUP: bool = True
    CANDO_WARN_BEFORE_REMOTE: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
