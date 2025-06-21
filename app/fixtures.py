from __future__ import annotations

from datetime import datetime
from typing import Iterable

from sqlalchemy.orm import Session

from .models import Fixture


WeekendDays = {5, 6}  # Saturday=5, Sunday=6


def filter_weekend_fixtures(fixtures: Iterable[dict]) -> list[dict]:
    """Return only fixtures played on Saturday or Sunday."""
    weekend = []
    for f in fixtures:
        kickoff = f.get("kickoff")
        if isinstance(kickoff, datetime) and kickoff.weekday() in WeekendDays:
            weekend.append(f)
    return weekend


def ingest_fixtures(db: Session, fixtures: Iterable[dict]) -> None:
    """Store fixtures in the database if not already present."""
    for data in fixtures:
        home = data["home_team"]
        away = data["away_team"]
        odds = data["odds"]
        exists = (
            db.query(Fixture)
            .filter_by(home_team=home, away_team=away, odds=odds)
            .first()
        )
        if not exists:
            db.add(Fixture(home_team=home, away_team=away, odds=odds))
    db.commit()
