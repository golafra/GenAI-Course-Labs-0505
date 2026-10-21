from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from blog_lab.api.config import Settings
from blog_lab.api.main import create_app


@pytest.fixture
def valid_settings(tmp_path) -> Settings:
    return Settings(database_path=str(tmp_path / "lab.db"))


@pytest.fixture
def app(valid_settings: Settings):
    return create_app(settings=valid_settings, init_schema=True)


@pytest.fixture
def client(app):
    return TestClient(app)


@pytest.fixture
def provision(client: TestClient):
    def _provision(**kwargs) -> dict:
        payload = {
            "display_name": kwargs.get("display_name", "user"),
            "can_write": kwargs.get("can_write", False),
            "can_review": kwargs.get("can_review", False),
            "can_publish": kwargs.get("can_publish", False),
        }
        response = client.post("/api/ops/provision", json=payload)
        assert response.status_code == 200, response.text
        return response.json()

    return _provision


def auth_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}
