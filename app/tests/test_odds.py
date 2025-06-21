from __future__ import annotations
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import Base
from app.odds import seed_default_mapping, get_points_for_odds
SessionLocal = None
engine = None



def setup_module(module):
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    module.engine = engine
    module.SessionLocal = TestingSessionLocal


def test_default_mapping_seed_and_query():
    db = SessionLocal()
    seed_default_mapping(db)

    assert get_points_for_odds(db, "1/4") == 1
    assert get_points_for_odds(db, "2/5") == 2
    assert get_points_for_odds(db, "4/6") == 3
    assert get_points_for_odds(db, "5/4") == 6
    assert get_points_for_odds(db, "7/4") == 9
    assert get_points_for_odds(db, "5/2") == 12
    assert get_points_for_odds(db, "10/1") == 15

    # Unknown odds return None
    assert get_points_for_odds(db, "100/1") is None
    db.close()
