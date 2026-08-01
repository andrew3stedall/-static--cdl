---
type: policy
last_updated: 2026-08-01T12:54:00+10:00
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

## Every-run contract

Each complete review must:

1. create a full dated review document;
2. create a dated changes document;
3. update the current board and watchlist where warranted;
4. update all affected entity notes;
5. update the wiki;
6. append one changelog row for each changed Markdown file;
7. cite every material factual or ranking change to a specific source.

## Time and naming

- Use Australia/Melbourne local time.
- Store timestamps in ISO 8601 with offset.
- Use `HHmm-AEST` or `HHmm-AEDT` in file names as applicable.
- Structure reviews and changes as `YYYY/MM/YYYY-MM-DD/`.

## History and corrections

Do not silently edit dated history. A correction must be labelled, timestamped, explain the original error and link to the correcting evidence. Superseded conclusions remain visible.

## Context reset

Before clearing a chat or agent context, confirm that all new evidence, considered alternatives, decisions, uncertainties and next actions are stored in the current run document.
