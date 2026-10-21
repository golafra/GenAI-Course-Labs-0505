from __future__ import annotations

import pytest

from blog_lab.api.config import Settings
from blog_lab.api.main import create_app


@pytest.fixture
def valid_settings(tmp_path) -> Settings:
    db_path = tmp_path / "lab.db"
    return Settings(database_path=str(db_path))


@pytest.fixture
def app(valid_settings: Settings):
    return create_app(settings=valid_settings)
