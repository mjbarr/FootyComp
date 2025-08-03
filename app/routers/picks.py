from __future__ import annotations

import re

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Fixture, Pick


class PickRead(BaseModel):
    id: int
    fixture_id: int
    selection: str
    joker: int

    class Config:
        from_attributes = True


router = APIRouter()


@router.get("/users/{user_id}/picks", response_model=list[PickRead])
def get_user_picks(user_id: int, db: Session = Depends(get_db)) -> list[Pick]:
    """Return all picks for the given user."""
    return db.query(Pick).filter_by(user_id=user_id).all()


class PickSubmission(BaseModel):
    message: str


def _parse_picks(message: str) -> list[tuple[int, str]]:
    tokens = message.replace(",", " ").split()
    picks: list[tuple[int, str]] = []
    for token in tokens:
        match = re.fullmatch(r"(\d+)([HAD])", token, re.IGNORECASE)
        if not match:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=f"Invalid pick format: {token}")
        fixture_id, selection = match.groups()
        picks.append((int(fixture_id), selection.upper()))
    if not picks:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="No picks provided")
    return picks


@router.post(
    "/users/{user_id}/picks",
    response_model=list[PickRead],
    status_code=status.HTTP_201_CREATED,
)
def submit_picks(
    user_id: int, submission: PickSubmission, db: Session = Depends(get_db)
) -> list[Pick]:
    """Parse a reply message and store picks for the user."""
    picks_data = _parse_picks(submission.message)
    saved: list[Pick] = []
    for fixture_id, selection in picks_data:
        fixture = db.get(Fixture, fixture_id)
        if not fixture:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail=f"Unknown fixture id {fixture_id}",
            )
        pick = Pick(user_id=user_id, fixture_id=fixture_id, selection=selection, joker=0)
        db.add(pick)
        saved.append(pick)
    db.commit()
    for pick in saved:
        db.refresh(pick)
    return saved
