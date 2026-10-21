"""Application settings — fail-fast on invalid persistence path."""

from __future__ import annotations

from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration loaded from environment."""

    model_config = SettingsConfigDict(
        env_prefix="BLOG_LAB_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_path: str = Field(
        ...,
        description="Local SQLite file path. Required; empty values are rejected.",
    )

    @field_validator("database_path")
    @classmethod
    def database_path_must_be_usable(cls, value: str) -> str:
        cleaned = (value or "").strip()
        if not cleaned:
            # Do not echo the raw value — keep the message generic.
            raise ValueError("database path is missing or blank")
        path = Path(cleaned)
        if path.exists() and path.is_dir():
            raise ValueError("database path must be a file path, not a directory")
        return cleaned

    @property
    def database_file(self) -> Path:
        return Path(self.database_path)


def load_settings() -> Settings:
    """Load settings or raise a configuration error without leaking secrets."""
    return Settings()  # type: ignore[call-arg]
