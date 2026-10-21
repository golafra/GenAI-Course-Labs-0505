"""FastAPI host — phase 1 skeleton (no Auth/Post yet)."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from blog_lab.api.config import Settings, load_settings


def create_app(settings: Settings | None = None) -> FastAPI:
    """Compose the HTTP application.

    Startup does not run migrations or provision users (Constitution / Research R4).

    Uvicorn: ``uvicorn blog_lab.api.main:create_app --factory --app-dir src``
    """

    resolved = settings if settings is not None else load_settings()

    @asynccontextmanager
    async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
        # Ensure parent directory can exist later; do not create schema here.
        resolved.database_file.parent.mkdir(parents=True, exist_ok=True)
        yield

    application = FastAPI(
        title="blog-content-assistant",
        version="0.1.0",
        description="Spec-driven blog lab — phase 1 host only",
        lifespan=lifespan,
    )
    application.state.settings = resolved

    @application.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return application
