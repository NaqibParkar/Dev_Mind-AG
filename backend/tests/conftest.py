import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

TEST_DATABASE = Path(__file__).parent / "test-devmind.db"
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DATABASE.as_posix()}"
os.environ["JWT_SECRET_KEY"] = "test-secret-that-is-not-used-in-production"

from app.db import models  # noqa: E402
from app.db.session import engine  # noqa: E402
from app.main import app  # noqa: E402
from app.routers import activity  # noqa: E402


@pytest.fixture(autouse=True)
def clean_database():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    yield
    models.Base.metadata.drop_all(bind=engine)
    engine.dispose()
    TEST_DATABASE.unlink(missing_ok=True)


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(activity.tracker, "start", lambda: None)
    monkeypatch.setattr(activity.tracker, "stop", lambda: None)
    with TestClient(app) as test_client:
        yield test_client
