# User Story 01: Player views weekly coupon

As a player, I want to see the weekly match coupon so that I know which fixtures I can pick.

## Acceptance Criteria
- Coupon lists all matches for the week with selection options
- Coupon is accessible via the web app and Facebook post
- Week numbers increment sequentially (1, 2, 3, ...)
- A new season resets the week number to 1

## Technical Implementation
- Create an API endpoint `GET /coupon` that returns fixtures for the requested `season` and `week`, defaulting to the latest week of the latest season.
- Expose the endpoint through a dedicated router and include it in the FastAPI app.
- Represent fixtures with a Pydantic model containing `id`, `season`, `week`, `home_team`, `away_team`, and `odds` fields.
- Store `season` and `week` alongside fixtures in the database.
- Add tests verifying the endpoint returns fixtures for the correct season and week.
