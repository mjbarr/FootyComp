from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel

from ..db import get_db
from ..models import Fixture


class FixtureRead(BaseModel):
    id: int
    season: int
    week: int
    home_team: str
    away_team: str
    odds: str

    class Config:
        from_attributes = True


router = APIRouter()


@router.get("/coupon", response_model=list[FixtureRead])
def read_coupon(
    season: int | None = None,
    week: int | None = None,
    db: Session = Depends(get_db),
) -> list[Fixture]:
    """Return fixtures for the requested season and week.

    Defaults to the latest week of the latest season.
    """
    if season is None:
        season = db.query(func.max(Fixture.season)).scalar() or 1
    query = db.query(Fixture).filter(Fixture.season == season)

    if week is None:
        week = (
            db.query(func.max(Fixture.week))
            .filter(Fixture.season == season)
            .scalar()
            or 1
        )
    query = query.filter(Fixture.week == week)
    return query.all()
