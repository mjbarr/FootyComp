from __future__ import annotations

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app
from app.models import User, Fixture, Pick

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


def test_get_user_picks():
    db = SessionLocal()
    user = User(email="foo@example.com", hashed_password="x")
    fixture = Fixture(home_team="A", away_team="B", odds="1/1")
    db.add_all([user, fixture])
    db.commit()
    user_id = user.id
    fixture_id = fixture.id
    pick = Pick(user_id=user_id, fixture_id=fixture_id, joker=0)
    db.add(pick)
    db.commit()
    db.close()

    client = TestClient(app)
    resp = client.get(f"/users/{user_id}/picks")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["fixture_id"] == fixture_id
