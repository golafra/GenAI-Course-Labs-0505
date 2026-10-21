"""T004 — Startup configuration gates (phase 1, still valid)."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from blog_lab.api.config import Settings
from blog_lab.api.main import create_app


def test_valid_settings_allow_host_health(valid_settings: Settings) -> None:
    app = create_app(settings=valid_settings)
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_blank_database_path_fails_fast() -> None:
    with pytest.raises(ValidationError) as exc_info:
        Settings(database_path="   ")
    message = str(exc_info.value).lower()
    assert "database path" in message
    assert "password" not in message


def test_missing_database_path_fails_fast(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("BLOG_LAB_DATABASE_PATH", raising=False)
    with pytest.raises(ValidationError):
        Settings()  # type: ignore[call-arg]


def test_directory_as_database_path_rejected(tmp_path) -> None:
    with pytest.raises(ValidationError):
        Settings(database_path=str(tmp_path))


def test_startup_does_not_create_sqlite_file(valid_settings: Settings) -> None:
    app = create_app(settings=valid_settings, init_schema=False)
    with TestClient(app):
        pass
    assert not valid_settings.database_file.exists()
