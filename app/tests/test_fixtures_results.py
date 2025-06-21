from __future__ import annotations

from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import Base
from app.models import Fixture
from app.fixtures import filter_weekend_fixtures, ingest_fixtures
from app.results import record_result, is_home_win


SessionLocal = None


def setup_module(module):
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    module.engine = engine
    module.SessionLocal = TestingSessionLocal


def test_filter_weekend_fixtures():
    fixtures = [
        {"kickoff": datetime(2024, 6, 22), "home_team": "A", "away_team": "B", "odds": "1/1"},
        {"kickoff": datetime(2024, 6, 24), "home_team": "C", "away_team": "D", "odds": "2/1"},
    ]
    weekend = filter_weekend_fixtures(fixtures)
    assert len(weekend) == 1
    assert weekend[0]["home_team"] == "A"


def test_ingest_and_record_result():
    db = SessionLocal()
    fixtures = [
        {"home_team": "TeamA", "away_team": "TeamB", "odds": "2/1", "kickoff": datetime(2024, 6, 22)},
        {"home_team": "TeamA", "away_team": "TeamB", "odds": "2/1", "kickoff": datetime(2024, 6, 22)},
    ]
    ingest_fixtures(db, fixtures)
    assert db.query(Fixture).count() == 1

    fixture_id = db.query(Fixture.id).first()[0]
    record_result(db, fixture_id, 2, 1)
    from app.models import Result
    res = db.query(Result).filter_by(fixture_id=fixture_id).first()
    assert res is not None
    assert is_home_win(res) is True
    # Update result
    record_result(db, fixture_id, 0, 0)
    res = db.query(Result).filter_by(fixture_id=fixture_id).first()
    assert res.home_score == 0
    db.close()
