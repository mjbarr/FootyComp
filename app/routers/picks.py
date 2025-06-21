from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Pick


class PickRead(BaseModel):
    id: int
    fixture_id: int
    joker: int

    class Config:
        from_attributes = True


router = APIRouter()


@router.get("/users/{user_id}/picks", response_model=list[PickRead])
def get_user_picks(user_id: int, db: Session = Depends(get_db)) -> list[Pick]:
    """Return all picks for the given user."""
    return db.query(Pick).filter_by(user_id=user_id).all()
