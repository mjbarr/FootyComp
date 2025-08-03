from __future__ import annotations

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .db import Base, engine, get_db
from .odds import seed_default_mapping, get_points_for_odds
from .routers.picks import router as picks_router
from .routers.odds import router as odds_router
from .routers.coupon import router as coupon_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="FootyComp")
app.include_router(picks_router)
app.include_router(odds_router)
app.include_router(coupon_router)


@app.on_event("startup")
def startup() -> None:
    with next(get_db()) as db:
        seed_default_mapping(db)


@app.get("/points/{odds}")
def read_points(odds: str, db: Session = Depends(get_db)) -> dict[str, int | None]:
    return {"points": get_points_for_odds(db, odds)}
