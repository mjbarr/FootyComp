from __future__ import annotations

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app
from app.models import Fixture

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


def test_read_coupon_defaults_to_latest_week_and_season():
    db = SessionLocal()
    db.add_all(
        [
            Fixture(
                home_team="Team A",
                away_team="Team B",
                odds="1/1",
                season=1,
                week=1,
            ),
            Fixture(
                home_team="Team C",
                away_team="Team D",
                odds="2/1",
                season=1,
                week=2,
            ),
            Fixture(
                home_team="Team E",
                away_team="Team F",
                odds="3/1",
                season=2,
                week=1,
            ),
        ]
    )
    db.commit()
    db.close()

    client = TestClient(app)
    resp = client.get("/coupon")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["home_team"] == "Team E"
    assert data[0]["season"] == 2
    assert data[0]["week"] == 1

    resp = client.get("/coupon", params={"season": 1})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["home_team"] == "Team C"
    assert data[0]["week"] == 2

    resp = client.get("/coupon", params={"season": 1, "week": 1})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["home_team"] == "Team A"
