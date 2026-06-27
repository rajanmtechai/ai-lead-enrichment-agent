from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = Field(default="AI Lead Enrichment Agent")
    environment: str = Field(default="local")
    api_host: str = Field(default="0.0.0.0")
    api_port: int = Field(default=8000)
    database_url: str = Field(default="sqlite+pysqlite:///./lead_enrichment.db")
    redis_url: str = Field(default="redis://localhost:6379/0")
    qdrant_url: str = Field(default="http://localhost:6333")
    jwt_secret_key: str = Field(default="change-me")
    jwt_algorithm: str = Field(default="HS256")
    jwt_access_token_expire_minutes: int = Field(default=60)
    cors_origins: list[str] = Field(default=["http://localhost:3000"])
    openai_api_key: str | None = Field(default=None)
    anthropic_api_key: str | None = Field(default=None)
    firecrawl_api_key: str | None = Field(default=None)
    tavily_api_key: str | None = Field(default=None)
    serper_api_key: str | None = Field(default=None)
    brave_api_key: str | None = Field(default=None)
    apollo_api_key: str | None = Field(default=None)
    hunter_api_key: str | None = Field(default=None)
    pdl_api_key: str | None = Field(default=None)
    clearbit_api_key: str | None = Field(default=None)
    hubspot_api_key: str | None = Field(default=None)
    lemlist_api_key: str | None = Field(default=None)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()