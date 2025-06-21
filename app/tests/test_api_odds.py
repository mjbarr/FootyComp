from __future__ import annotations

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app

SessionLocal = None
engine = None


def setup_module(module):
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    module.engine = engine
    module.SessionLocal = TestingSessionLocal

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db


def teardown_module(module):
    app.dependency_overrides.clear()


def test_create_and_update_odds():
    client = TestClient(app)
    resp = client.post("/odds", json={"odds": "1/1", "points": 5})
    assert resp.status_code == 201
    data = resp.json()
    assert data["odds"] == "1/1"
    assert data["points"] == 5

    resp = client.put("/odds/1%2F1", json={"points": 10})
    assert resp.status_code == 200
    assert resp.json()["points"] == 10

    resp = client.get("/odds")
    assert resp.status_code == 200
    items = resp.json()
    assert len(items) == 1
    assert items[0]["points"] == 10
