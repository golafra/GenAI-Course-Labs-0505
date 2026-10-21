"""FastAPI host — workshop steps 11–15 composition root."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from blog_lab.api.config import Settings, load_settings
from blog_lab.api.deps import UnauthorizedError, unauthorized_handler
from blog_lab.api.routes import author_router, editor_router, ops_router, public_router
from blog_lab.infrastructure.sqlite_store import SqliteBlogStore


def create_app(settings: Settings | None = None, *, init_schema: bool = False) -> FastAPI:
    """Compose HTTP app.

    Normal startup does NOT migrate/provision. Tests/ops may pass init_schema=True
    or call ``POST /api/ops/provision`` which initializes schema.
    """

    resolved = settings if settings is not None else load_settings()
    store = SqliteBlogStore(resolved.database_path)
    if init_schema:
        store.init_schema()

    @asynccontextmanager
    async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
        resolved.database_file.parent.mkdir(parents=True, exist_ok=True)
        yield

    application = FastAPI(
        title="blog-content-assistant",
        version="0.2.0",
        description="Spec-driven blog lab — Author/Editor/Public workflow (steps 11–15)",
        lifespan=lifespan,
    )
    application.state.settings = resolved
    application.state.store = store
    application.add_exception_handler(UnauthorizedError, unauthorized_handler)

    @application.get("/health", tags=["health"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    application.include_router(author_router)
    application.include_router(editor_router)
    application.include_router(public_router)
    application.include_router(ops_router)
    return application
