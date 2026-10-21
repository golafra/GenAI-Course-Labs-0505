"""FastAPI dependencies — auth extracts identity only."""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends, Header, Request

from blog_lab.api.problems import problem_response
from blog_lab.application.results import AppError
from blog_lab.application.security import UserAccess
from blog_lab.application.services import AuthorPostService, EditorPostService, PublicPostService
from blog_lab.infrastructure.sqlite_store import SqliteBlogStore


def get_store(request: Request) -> SqliteBlogStore:
    return request.app.state.store


def get_author_service(store: Annotated[SqliteBlogStore, Depends(get_store)]) -> AuthorPostService:
    return AuthorPostService(store)


def get_editor_service(store: Annotated[SqliteBlogStore, Depends(get_store)]) -> EditorPostService:
    return EditorPostService(store)


def get_public_service(store: Annotated[SqliteBlogStore, Depends(get_store)]) -> PublicPostService:
    return PublicPostService(store)


class UnauthorizedError(Exception):
    def __init__(self, error: AppError) -> None:
        self.error = error


def require_user(
    request: Request,
    authorization: Annotated[str | None, Header()] = None,
) -> UserAccess:
    store: SqliteBlogStore = request.app.state.store
    if not authorization or not authorization.lower().startswith("bearer "):
        raise UnauthorizedError(
            AppError(code="unauthorized", message="valid bearer token required", http_hint=401)
        )
    raw = authorization.split(" ", 1)[1].strip()
    if not raw:
        raise UnauthorizedError(
            AppError(code="unauthorized", message="valid bearer token required", http_hint=401)
        )
    access = store.verify_token(raw)
    if access is None:
        raise UnauthorizedError(
            AppError(code="unauthorized", message="valid bearer token required", http_hint=401)
        )
    # Permission is NOT inferred here — only identity/access snapshot from server store.
    return access


def unauthorized_handler(_request: Request, exc: UnauthorizedError):
    return problem_response(exc.error)
