from __future__ import annotations

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .db import Base, engine, get_db
from .odds import seed_default_mapping, get_points_for_odds


Base.metadata.create_all(bind=engine)

app = FastAPI(title="FootyComp")


@app.on_event("startup")
def startup() -> None:
    with next(get_db()) as db:
        seed_default_mapping(db)


@app.get("/points/{odds}")
def read_points(odds: str, db: Session = Depends(get_db)) -> dict[str, int | None]:
    return {"points": get_points_for_odds(db, odds)}
