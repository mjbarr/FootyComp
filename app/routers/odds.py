from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import OddsMapping


class OddsRead(BaseModel):
    odds: str
    points: int

    class Config:
        from_attributes = True


class OddsUpdate(BaseModel):
    points: int


router = APIRouter()


@router.get("/odds", response_model=list[OddsRead])
def list_odds(db: Session = Depends(get_db)) -> list[OddsMapping]:
    """Return all odds-to-points mappings."""
    return db.query(OddsMapping).all()


@router.post(
    "/odds",
    status_code=status.HTTP_201_CREATED,
    response_model=OddsRead,
)
def create_odds(mapping: OddsRead, db: Session = Depends(get_db)) -> OddsMapping:
    """Create a new odds mapping."""
    exists = db.query(OddsMapping).filter_by(odds=mapping.odds).first()
    if exists:
        raise HTTPException(status_code=409, detail="Odds already mapped")
    record = OddsMapping(odds=mapping.odds, points=mapping.points)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.put("/odds/{odds:path}", response_model=OddsRead)
def update_odds(
    odds: str, data: OddsUpdate, db: Session = Depends(get_db)
) -> OddsMapping:
    """Update points for an odds mapping."""
    record = db.query(OddsMapping).filter_by(odds=odds).first()
    if not record:
        raise HTTPException(status_code=404, detail="Mapping not found")
    record.points = data.points
    db.commit()
    db.refresh(record)
    return record
