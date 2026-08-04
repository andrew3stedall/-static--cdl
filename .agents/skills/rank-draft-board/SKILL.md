---
name: rank-draft-board
description: Produce and reconcile the single top-220 FPL Draft ordering for an eight-manager, 20-round league, including positional scarcity and explicit movement reasons.
---

# Rank the draft board

Rank expected Draft usefulness over the relevant season. Ignore player price, ownership and value for money.

## League model

- 8 managers.
- 20 picks each.
- 160 players drafted.
- Maintain at least 220 ranked players.

## Core factors

- expected minutes and starting security;
- attacking and clean-sheet potential;
- role, position, set pieces and penalties;
- team and manager tactics;
- injury, suspension and rotation risk;
- preseason evidence;
- transfer risk;
- fixture outlook;
- season-long ceiling and floor;
- positional scarcity and replacement level.

Do not let recent noise override durable role evidence without justification.

## Draft-horizon injury weighting

Judge injury risk over the full season because a drafted player can be held through recovery. Do not apply redraft-style or Gameweek-1 penalties mechanically.

- Expected return within about four weeks: small discount unless recurrence or role loss is credible.
- Roughly five to ten weeks: moderate discount, scaled by player ceiling, benchability and replacement value.
- More than ten weeks, repeated setbacks, major surgery or no credible return date: substantial discount.
- Season-ending or career-altering injury: severe discount.
- On return, assess whether the player should immediately regain the same role and minutes.

Use official club updates and FPL metadata first. Use Premier Injuries (`https://www.premierinjuries.com/injury-table.php`) as a specialist expected-return source when accessible, recording access failures and corroborating material claims.

## Segments

- **Franchise:** picks 1–8.
- **Foundation:** picks 9–32.
- **Core:** picks 33–80.
- **Depth:** picks 81–128.
- **Endgame:** picks 129–160.
- **Undrafted buffer:** picks 161–220.

Segments are planning aids, not claims that all players within a segment are interchangeable.

## Output rules

For every ranked player include at least:

- overall pick order;
- player;
- FPL ID;
- position;
- team;
- segment;
- tier;
- concise rationale;
- status/risk;
- evidence reference;
- last-change timestamp.

Compare with the prior board. Quantify old rank, new rank and reason for every material move. A stable player should remain stable unless evidence or relative scarcity changes.
