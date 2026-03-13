"""Application configuration using pydantic-settings."""

from functools import lru_cache
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # App
    app_name: str = "Python OOP Journey API"
    debug: bool = False
    environment: str = "development"
    secret_key: str = Field(default="dev-secret", description="Secret key for JWT and sessions")

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # CORS
    allowed_origins_raw: str = Field(default="http://localhost:3000", alias="ALLOWED_ORIGINS")

    @property
    def allowed_origins(self) -> List[str]:
        """Get allowed origins as list."""
        return [origin.strip() for origin in self.allowed_origins_raw.split(",")]

    # Database
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/oop_journey",
        description="Async PostgreSQL connection URL",
    )
    database_pool_size: int = 10
    database_max_overflow: int = 20

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Email
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_from: str = "noreply@oopjourney.com"
    
    # SendGrid
    sendgrid_api_key: str = ""

    # JWT
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60
    jwt_refresh_token_expire_days: int = 7
    jwt_access_token_expire_days: int = 7  # For new magic link auth

    # Magic Link
    magic_link_expire_minutes: int = 15
    magic_link_base_url: str = ""  # Base URL for magic links (defaults to first allowed_origin)

    # Code Execution
    docker_timeout: int = 30
    max_code_length: int = 10000

    # AI Integration
    openai_api_key: str = Field(default="", description="OpenAI API key")
    anthropic_api_key: str = Field(default="", description="Anthropic API key")
    ai_hint_model: str = Field(default="gpt-4o-mini", description="Model for hints")
    ai_review_model: str = Field(default="gpt-4o", description="Model for code reviews")
    ai_rate_limit_per_hour: int = Field(default=10, description="AI requests per hour")
    ai_cache_ttl_hours: int = Field(default=24, description="AI cache TTL in hours")

    # Logging
    log_level: str = "INFO"

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.environment.lower() == "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.environment.lower() == "production"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
