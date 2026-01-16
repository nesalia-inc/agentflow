"""Database configuration management."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """Database configuration settings."""

    model_config = SettingsConfigDict(
        env_prefix="AGENTFLOW_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Database connection
    db_url: str = Field(
        default="postgresql+asyncpg://agentflow:agentflow@localhost:5432/agentflow",
        description="PostgreSQL database URL with asyncpg driver",
    )

    # Optional schema name
    db_schema: str = Field(
        default="public",
        description="Database schema name",
    )

    # Connection pool settings
    db_pool_size: int = Field(
        default=10,
        description="Connection pool size",
        ge=1,
        le=100,
    )

    db_max_overflow: int = Field(
        default=20,
        description="Maximum overflow connections",
        ge=0,
        le=100,
    )

    @property
    def async_url(self) -> str:
        """Get the async database URL."""
        return self.db_url


# Global settings instance
_db_settings: DatabaseSettings | None = None


def get_database_settings() -> DatabaseSettings:
    """Get the database settings instance (singleton)."""
    global _db_settings
    if _db_settings is None:
        _db_settings = DatabaseSettings()
    return _db_settings


def set_database_settings(settings: DatabaseSettings) -> None:
    """Set the database settings instance.

    Args:
        settings: Database settings to set as singleton
    """
    global _db_settings
    _db_settings = settings
