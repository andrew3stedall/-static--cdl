---
name: document-fpl-review
description: Persist every FPL research run as a complete cited Markdown review, an explicit change record and fully traceable updates to canonical documents.
---

# Document an FPL review

This skill exists to prevent research loss and allow the working chat context to be cleared safely.

## Required files per run

Create immutable files using Australia/Melbourne time:

- `vault/06 Reviews/YYYY/MM/YYYY-MM-DD/HHmm-AEST-review.md`
- `vault/07 Changes/YYYY/MM/YYYY-MM-DD/HHmm-AEST-changes.md`

Update as required:

- `vault/01 Current/Current Draft Board.md`
- `vault/01 Current/Current Watchlist.md`
- affected player, team, position and source notes;
- `vault/Wiki.md`;
- `vault/00 Meta/Document Changelog.md`.

## Full review content

Capture:

1. scope and retrieval window;
2. sources searched and unavailable sources;
3. official FPL API state and deltas;
4. every material item learned;
5. evidence considered but not adopted;
6. ranking methodology and important trade-offs;
7. complete current recommendation or a link to the canonical board;
8. transfer, injury, preseason and role watchlists;
9. uncertainties and next-review triggers;
10. all citations.

## Changes document

Start with a concise delta table containing old rank/tier, new rank/tier, cause, confidence and citations. Include new entrants, removals, role changes, injury changes, transfer changes and unchanged high-priority watch items. State explicitly when no material change occurred.

## Document changelog

For every Markdown file created or modified, append one row containing:

- ISO timestamp;
- path;
- action: created, updated, corrected or superseded;
- concise summary;
- triggering review;
- evidence links.

Do not use a vague repository-wide entry when several documents changed.
