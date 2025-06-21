from __future__ import annotations

from sqlalchemy.orm import Session

from .models import OddsMapping

DEFAULT_MAPPING = [
    {"points": 1, "odds": ["1/12", "1/11", "1/10", "1/9", "1/8", "1/7", "2/13", "1/6", "2/11", "1/5", "2/9", "1/4"]},
    {"points": 2, "odds": ["2/7", "3/10", "1/3", "4/11", "2/5", "4/9"]},
    {"points": 3, "odds": ["3/4", "1/2", "8/15", "4/7", "8/13", "4/6", "8/11"]},
    {"points": 6, "odds": ["4/5", "5/6", "10/11", "Evens", "11/10", "23/20", "6/5", "5/4", "13/10"]},
    {"points": 9, "odds": ["11/8", "7/5", "6/4", "8/5", "17/10", "13/8", "7/4", "9/5", "15/8", "2/1"]},
    {"points": 12, "odds": ["21/10", "23/10", "11/5", "9/4", "12/5", "5/2", "13/5", "11/4", "3/1", "10/3", "7/2"]},
    {"points": 15, "odds": ["4/1", "9/2", "5/1", "11/2", "6/1", "13/2", "7/1", "15/2", "8/1", "17/2", "9/1", "10/1", "11/1", "12/1", "14/1", "16/1", "18/1", "20/1", "22/1", "25/1", "28/1", "33/1"]},
]


def seed_default_mapping(db: Session) -> None:
    """Seed the default odds-to-points mapping."""
    for rule in DEFAULT_MAPPING:
        for odd in rule["odds"]:
            if not db.query(OddsMapping).filter_by(odds=odd).first():
                db.add(OddsMapping(odds=odd, points=rule["points"]))
    db.commit()


def get_points_for_odds(db: Session, odds: str) -> int | None:
    """Return points for given odds if mapping exists."""
    record = db.query(OddsMapping).filter_by(odds=odds).first()
    return record.points if record else None
