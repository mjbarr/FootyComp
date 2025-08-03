# User Story 02: Player submits picks via Facebook reply

As a player, I want to submit my selections by replying to the coupon post so that my picks are recorded.

## Acceptance Criteria
- Reply format is documented for valid picks
- Picks are parsed and stored in the database
- Validation errors are reported back to the player

## Technical Implementation
- Describe the reply syntax as `<fixture_id><pick>` pairs separated by spaces (e.g. `1H 2A 3D` where `H`, `A`, `D` denote home win, away win, draw)
- Add a `selection` field to the `Pick` model to capture the player's choice
- Create a parser that validates the reply string and extracts fixture/pick pairs
- Expose a `POST /users/{user_id}/picks` endpoint accepting a `message` body and storing valid picks
- Return a list of stored picks on success or a 400 error with details for invalid formats or unknown fixtures
- Write tests for successful submission and validation failures
