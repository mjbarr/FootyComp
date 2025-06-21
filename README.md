# FootyComp

A minimal FastAPI application scaffolding for a football score prediction game. It includes:

- SQLAlchemy models for users, fixtures, picks, results and joker usage.
- Odds to points mapping with seed and lookup utilities.
- Helper modules for ingesting fixtures and recording match results.
- Basic tests demonstrating database interactions.

Run tests and lint checks with:

```bash
ruff check .
pytest -q
```
