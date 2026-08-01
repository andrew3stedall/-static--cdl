---
type: policy
last_updated: 2026-08-01T16:43:00+10:00
---

# Repository Contract

## Objective

Preserve the complete reasoning and evidence behind an FPL Draft ranking while keeping active agent context small enough to work reliably.

## Canonical versus historical documents

| Purpose | Canonical path | Mutation policy |
|---|---|---|
| Overall advised order | `vault/01 Current/Current Draft Board.md` | Replace current state; log every edit |
| Current unresolved risks | `vault/01 Current/Current Watchlist.md` | Replace current state; log every edit |
| Navigational summary | `vault/Wiki.md` | Update after every run |
| Full run record | `vault/06 Reviews/...` | Immutable after publication |
| Delta from prior run | `vault/07 Changes/...` | Immutable after publication |
| Document audit trail | `vault/00 Meta/Document Changelog.md` | Append-only |

## Every-run content contract

Each complete review must:

1. create a full dated review document;
2. create a dated changes document;
3. update the current board and watchlist where warranted;
4. update all affected entity notes;
5. update the wiki;
6. append one changelog row for each changed Markdown file;
7. cite every material factual or ranking change to a specific source.

## Every-run Git lifecycle

Each scheduled or manually requested full review must use this lifecycle:

1. read the latest `main` and create a new unique `codex/fpl-review-YYYYMMDD-HHmm-<short-slug>` branch from it;
2. perform the entire review only on that branch;
3. commit the run-specific files and open one non-draft pull request to `main`;
4. inspect the complete diff, verify citations, links, timestamps and changelog coverage, confirm mergeability, and confirm all configured checks pass;
5. squash-merge only when the review is complete and consistent;
6. verify the merged commit is present on `main`;
7. delete the merged head branch.

A previous run branch must never be reused. A review must never be committed directly to `main`. A failed, conflicting or incomplete PR must remain unmerged with the blocking evidence recorded. Branch deletion is part of completion, not optional cleanup.

## Time and naming

- Use Australia/Melbourne local time.
- Store timestamps in ISO 8601 with offset.
- Use `HHmm-AEST` or `HHmm-AEDT` in file names as applicable.
- Structure reviews and changes as `YYYY/MM/YYYY-MM-DD/`.

## History and corrections

Do not silently edit dated history. A correction must be labelled, timestamped, explain the original error and link to the correcting evidence. Superseded conclusions remain visible.

## Context reset

Before clearing a chat or agent context, confirm that all new evidence, considered alternatives, decisions, uncertainties and next actions are stored in the current run document.
