---
type: data_contract
last_updated: 2026-08-01T12:54:00+10:00
---

# FPL API

## Authority

The official Fantasy Premier League API is the canonical source for the current game player pool and identifiers.

## Endpoints

- [Bootstrap static](https://fantasy.premierleague.com/api/bootstrap-static/)
- [Fixtures](https://fantasy.premierleague.com/api/fixtures/)
- Player summary: `https://fantasy.premierleague.com/api/element-summary/{element_id}/`

## Identity contract

- Use `elements[].id` as the stable player key.
- Resolve team names from `teams` in the same bootstrap payload.
- Resolve position names from `element_types` in the same payload.
- Do not use display names as primary keys.
- Record retrieval timestamps and endpoint failures.

## Interpretation limits

API presence establishes registration in the current FPL game, not guaranteed Premier League minutes. API news and status fields can lag club reporting and should be treated as game metadata rather than definitive medical or transfer evidence.

## Required reconciliation

Every full review compares the current payload with the previous review for additions, removals, team changes, position changes, availability changes and fixture changes.
