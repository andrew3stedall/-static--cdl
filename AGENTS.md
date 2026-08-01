# FPL Draft project instructions

## Purpose

Maintain an evidence-based FPL Draft board and Obsidian knowledge vault for an eight-manager league with 20 picks each. Exactly 160 players will be drafted; maintain at least 220 ranked players to preserve a replacement-level buffer.

## Context discipline

- Keep this file short and stable.
- Load task-specific procedures from `.agents/skills/*/SKILL.md` only when relevant.
- Keep detailed research, examples and history in `vault/`, not in agent instructions or chat memory.
- Treat repository documents, not conversational memory, as the canonical project record.

## Canonical state

- `vault/01 Current/Current Draft Board.md` is the only current overall ordering.
- `vault/01 Current/Current Watchlist.md` is the only current unresolved-risk list.
- `vault/Wiki.md` is the navigational summary of the work.
- Dated documents under `vault/06 Reviews/` and `vault/07 Changes/` are immutable after publication except for clearly labelled corrections.

## Source hierarchy

1. Official FPL API for player identity, team, position, availability metadata and fixtures.
2. Official club communications and direct manager/player comments.
3. Reliable club correspondents and specialist reporters.
4. High-signal tactical, fixture and FPL analysts.
5. Knowledgeable fan accounts and communities, corroborated for material claims.

Use stable FPL player IDs. Never silently merge similarly named players.

## Required review workflow

1. Read the current board, watchlist, latest review and latest change record.
2. Invoke `.agents/skills/sync-fpl-api/SKILL.md`.
3. Invoke the relevant evidence skills for public sources, preseason and transfers.
4. Invoke `.agents/skills/rank-draft-board/SKILL.md`.
5. Invoke `.agents/skills/document-fpl-review/SKILL.md`.
6. Invoke `.agents/skills/maintain-obsidian-vault/SKILL.md`.
7. Verify citations, links, timestamps and changelog coverage before finishing.

## Non-negotiable rules

- Rank for Draft usefulness, not price, ownership or value for money.
- Separate confirmed facts, credible reports and inference.
- Cite the specific post, article, API endpoint or official statement supporting each material change.
- Use Australia/Melbourne timestamps in ISO 8601 form.
- Do not overwrite historical review or change records.
- Record every changed Markdown document in `vault/00 Meta/Document Changelog.md` with timestamp, action, summary and evidence.
- Each run must create one full review document and one changes document, even when there are no material ranking changes.
- Capture rejected hypotheses and evidence considered, not only final conclusions.
