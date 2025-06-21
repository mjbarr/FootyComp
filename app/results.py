from __future__ import annotations

from sqlalchemy.orm import Session

from .models import Result


def record_result(db: Session, fixture_id: int, home_score: int, away_score: int) -> None:
    """Insert or update a fixture result."""
    result = db.query(Result).filter_by(fixture_id=fixture_id).first()
    if not result:
        result = Result(
            fixture_id=fixture_id, home_score=home_score, away_score=away_score
        )
        db.add(result)
    else:
        result.home_score = home_score
        result.away_score = away_score
    db.commit()


def is_home_win(result: Result) -> bool:
    """Return True if the home team won."""
    return result.home_score > result.away_score
