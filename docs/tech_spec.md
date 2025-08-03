# FootyComp Technical Specification

## Overview
The FootyComp application enables friends to participate in a weekly football picking competition with odds-based scoring. This document describes the technical architecture, technologies, and deployment strategy. In addition to posting weekly coupons, the app reads reply comments to automatically capture players' picks. Players may also play a **joker** twice per season—once before Christmas and once after—to double the points of a winning selection.

## Architecture
FootyComp follows a service-oriented architecture composed of the following components:

- **Frontend** – React application styled with Tailwind CSS for responsive UI.
- **API** – FastAPI service handling authentication, business logic, and data persistence.
- **Background Worker** – Celery worker for scheduled tasks such as fetching odds, results, posting updates to Facebook, and parsing reply comments for player selections.
- **Database** – PostgreSQL relational database storing competition data.
- **Cache/Broker** – Redis instance used by Celery and optional caching.

Each service runs in its own Docker container and is deployed as a Render service.

## Technology Stack

| Area | Technology |
| ---- | ---------- |
| Frontend | React 18, TypeScript, Vite, Tailwind CSS |
| API | Python 3.11, FastAPI, SQLAlchemy, Pydantic |
| Background Tasks | Celery, Redis |
| Database | PostgreSQL 15 |
| Auth | Facebook OAuth via Facebook Graph API |
| API Integration | Odds API for match odds and results |
| Testing | pytest, Testing Library for React |
| Tooling | Docker, Docker Compose, Pre-commit, GitHub Actions |

## Services

### Frontend Service
- Built with React and TypeScript using Vite for rapid development.
- Tailwind CSS configured for styling.
- Compiled static assets served by Render's static site hosting.
- Environment variables supplied at build time for API base URL and Facebook App ID.

### API Service
- FastAPI application exposing REST endpoints:
  - Player management and authentication
  - Weekly team selection with optional joker flag
  - Points allocation boundary management
  - Odds provider selection
  - League table retrieval
- Uses SQLAlchemy ORM for database interactions and Alembic for migrations.
- JWT session tokens stored in HTTP-only cookies after Facebook OAuth login.

### Background Worker Service
- Celery worker scheduled via Celery Beat to:
  - Fetch weekly match odds from the Odds API using the configured UK provider(s).
  - Retrieve match results and award points, applying joker multipliers and points boundaries.
  - Post coupons and results to the Facebook group.
  - Read reply comments on coupon posts and forward valid picks to the API.
- Communicates with API and database directly.

### Database Service
- Managed PostgreSQL instance on Render.
- Connection handled via SQLAlchemy with async engine.

### Cache/Broker Service
- Redis instance on Render.
- Serves as Celery message broker and result backend.

## Data Model
Key tables and relationships:

- `players` (id, facebook_id, name, joker_pre_used, joker_post_used, created_at)
- `teams` (id, name, league)
- `matches` (id, home_team_id, away_team_id, kickoff, odds_home, odds_draw, odds_away, result)
- `selections` (id, player_id, match_id, chosen_team_id, week, is_joker, created_at)
- `points_rules` (id, min_odds, max_odds, points)
- `settings` (id, odds_providers)
- `scores` (id, player_id, week, points, created_at)

## Deployment on Render

1. **Dockerization**
   - Each service (frontend, API, worker) has its own Dockerfile.
   - Multi-stage builds minimize image size.
   - Docker Compose file for local development.
2. **Render Services**
   - API: Web Service using Dockerfile, exposes HTTPS on port 8000.
   - Frontend: Static Site from built assets or Docker-based web service.
   - Worker: Background Worker using worker Dockerfile.
   - Redis: Render Redis instance.
   - PostgreSQL: Render managed PostgreSQL database.
3. **Environment Variables & Secrets**
   - Managed via Render's built-in secret management; no secrets committed to code.
   - `FACEBOOK_APP_ID`, `FACEBOOK_APP_SECRET`
   - `ODDS_API_KEY`
   - `DATABASE_URL`
   - `REDIS_URL`
4. **CI/CD**
   - GitHub Actions pipeline runs linters and tests on push.
   - Render auto-deploys on successful build of main branch.

## Security & Compliance
- All secrets managed through Render's encrypted environment groups and never committed to the repository.
- HTTPS enforced for all services.
- Input validation via Pydantic and server-side checks.
- Regular dependency scanning with Dependabot.

## Future Work
- Add mobile-friendly enhancements.
- Introduce real-time scoring updates using WebSockets.
- Implement team reuse restrictions per player.

