# FootyComp Application Requirements

## Overview
- Build a friendly competition app for friends to pick a football team each week.
- Players earn points based on the odds of their selected team winning.
- The app fetches match odds and results automatically and maintains a league table.
- Facebook integration handles authentication and group interactions.

## Odds-Based Scoring
- Points values: **1, 3, 6, 9, 12, 15**.
- Define configurable odds boundaries that map to these points.
  - Example mappings:
    - 15/1 → 15 points.
    - 11/8 → 9 points.
    - Even money (1/1) → 6 points.
- Each points tier covers all odds up to the next tier (e.g., 1 point covers odds below the 3-point threshold).
- Provide admin UI or configuration file to adjust boundaries.

## Player Management
- Add and manage players in the competition.
- Facebook Login is required; every participant uses their Facebook account.

## Weekly Team Selection
- Each player selects one team per week.
- System records selections and verifies against allowed fixtures.
- Optional: prevent choosing the same team multiple times (future enhancement).

## Odds and Results Retrieval
- Use the Odds API to pull match odds each week.
- Fetch match results on Sunday or Monday (with option for live updates).
- Award points according to the configured odds boundaries.

## League Table
- Track cumulative scores for all players.
- Display current standings and historical weekly performance.

## Facebook Group Integration
- Post a generated coupon with match fixtures and odds every Thursday in the group.
- Monitor group responses to capture player selections.
- After matches conclude, post results and updated league table back to the group.

## Future Enhancements
- Real-time scoring updates during matches.
- Mobile-friendly front-end or standalone mobile app.
- Additional social media integrations or notification channels.
