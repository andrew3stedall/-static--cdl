---
type: schema
last_updated: 2026-08-01T12:54:00+10:00
---

# Entity Model

## Player note

Path: `vault/02 Players/{Player Name} - {FPL ID}.md`

```yaml
---
type: player
fpl_id: 123
player_name: Example Player
aliases: []
team: "[[03 Teams/Example FC]]"
position: "[[04 Positions/Midfielder]]"
api_status: available
current_rank: 42
current_segment: Core
last_reviewed: 2026-08-01T20:00:00+10:00
---
```

Recommended sections: current assessment, role and minutes, set pieces, preseason, transfer status, injury/availability, evidence timeline, ranking history and backlinks.

## Team note

```yaml
---
type: team
team_name: Example FC
fpl_team_id: 1
last_reviewed: 2026-08-01T20:00:00+10:00
---
```

Link to current squad notes, tactical structure, set pieces, fixtures, sources and affected reviews.

## Position note

```yaml
---
type: position
position_name: Midfielder
fpl_element_type: 3
last_reviewed: 2026-08-01T20:00:00+10:00
---
```

Record replacement level, scarcity, roster depth and draft-round implications.

## Source note

```yaml
---
type: source
source_name: Example Reporter
platform: X
handle: example
source_class: club_correspondent
reliability: high
last_reviewed: 2026-08-01T20:00:00+10:00
---
```

Store source strengths, weaknesses, relevant clubs/topics and a timeline of cited posts.

## Stable identity

The official FPL `element.id` is the primary player key. Names, teams and positions can change; IDs must not be replaced by name matching.
