from pydantic import BaseModel
import os

class Settings(BaseModel):
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "hub")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "hubpass")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "hubdb")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "postgres")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", 5432))

    REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379/0")

    API_SECRET_KEY: str = os.getenv("API_SECRET_KEY", "dev-secret")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "http://localhost:3000")

    USE_LOCAL_EMBEDDINGS: bool = os.getenv("USE_LOCAL_EMBEDDINGS", "true").lower() == "true"
    MODEL_NAME: str = os.getenv("MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")

    ENABLE_SERVER_LLM: bool = os.getenv("ENABLE_SERVER_LLM", "true").lower() == "true"
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

settings = Settings()
