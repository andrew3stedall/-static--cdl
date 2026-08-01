---
name: run-fpl-review
description: Orchestrate one complete FPL Draft research iteration and leave the repository with a cited current board, immutable review record and explicit delta from the prior run.
---

# Run an FPL review

Use this skill for a scheduled or manually requested full review.

## Inputs

- Official FPL API player and fixture data.
- Current board and watchlist.
- Latest immutable review and changes record.
- New public evidence since the prior review.

## Procedure

1. Establish the review timestamp in Australia/Melbourne.
2. Read `AGENTS.md` and the canonical current documents.
3. Run `sync-fpl-api` and record player-pool additions, removals and metadata changes.
4. Run `collect-public-evidence`, focusing on developments since the previous review.
5. Run `assess-preseason` when preseason evidence exists.
6. Run `assess-transfer-risk` for transfer and squad-competition developments.
7. Run `rank-draft-board` to produce the complete top-220 order and positional priorities.
8. Run `document-fpl-review` to create the immutable review and delta documents and update current state.
9. Run `maintain-obsidian-vault` to update entity notes, links and the wiki.
10. Validate that every material claim has a specific citation and every changed Markdown file appears in the document changelog.

## Completion test

A run is incomplete unless it creates:

- one dated full review;
- one dated changes document;
- a reconciled current board;
- a reconciled current watchlist;
- updated affected entity notes;
- an updated wiki summary;
- a changelog entry for every changed Markdown document.

When there are no material changes, state that explicitly. Do not manufacture movement.
