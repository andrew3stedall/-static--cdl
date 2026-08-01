---
name: sync-fpl-api
description: Reconcile the official Fantasy Premier League player pool, teams, positions, availability metadata and fixtures before any ranking work.
---

# Synchronise official FPL data

The official FPL API is authoritative for whether a player exists in the current game and for the game's current player, team and position identifiers.

## Endpoints

- `https://fantasy.premierleague.com/api/bootstrap-static/`
- `https://fantasy.premierleague.com/api/fixtures/`
- Player detail endpoint when needed: `https://fantasy.premierleague.com/api/element-summary/{element_id}/`

## Procedure

1. Fetch the current endpoints; record retrieval timestamp and HTTP outcome.
2. Preserve `element.id` as the stable player identifier.
3. Map team and element-type IDs to names from the same payload.
4. Diff against the previous run for:
   - new players;
   - removed players;
   - team changes;
   - position changes;
   - availability/news changes;
   - fixture changes.
5. Never infer that a removed player completed a transfer without a corroborating source.
6. Keep transferred or unregistered players on a labelled watchlist only when the uncertainty remains decision-relevant.
7. Pass all material API deltas to the ranking and documentation skills.

## Evidence record

For each API-derived change, cite the endpoint and retrieval timestamp. Where the API exposes ambiguous or stale text, say so rather than treating it as definitive medical or transfer reporting.
