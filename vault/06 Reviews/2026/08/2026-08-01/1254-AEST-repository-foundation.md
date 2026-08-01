---
type: review
review_kind: repository_foundation
started: 2026-08-01T12:54:00+10:00
completed: 2026-08-01T12:54:00+10:00
material_ranking_change: false
---

# 2026-08-01 12:54 AEST Repository Foundation Review

## Scope

Establish a Codex skill structure and Obsidian-compatible documentation system for ongoing FPL Draft research in `andrew3stedall/-static--cdl`.

## Requirements captured

- Use focused Codex skills rather than one large global instruction file.
- Preserve all research and reasoning in Markdown so active chat context can be cleared safely.
- Create a complete review document on every run.
- Maintain a timestamped per-document changelog.
- Cite the relevant public post, article or API endpoint for material claims.
- Maintain an Obsidian vault linking players, teams, positions, sources, reviews and changes.
- Maintain a wiki-style summary of the work.
- Maintain one canonical current draft order containing player, position, team, pick order and segment.
- Store reviews and changes in date-based paths.
- Model an eight-manager, 20-pick league, requiring 160 drafted players and a deeper ranking buffer.

## Design decisions

### Small project layer, focused skills

The root `AGENTS.md` contains only stable project invariants and points to narrow skills under `.agents/skills/`. This follows guidance to use concise skills for task-specific workflows and keep long references outside always-on context. [Matt Pocock's usage guide](https://github.com/mattpocock/agent-rules-books/blob/main/docs/USAGE.md) recommends skills-first delivery, a small root project layer and retrieval or files for long reference material.

### Canonical current state versus immutable history

One current board prevents ranking divergence. Dated reviews retain everything learned and considered. Dated change records provide fast iteration-to-iteration comparison. The wiki points to these records without becoming a second board.

### Obsidian entity network

Stable FPL IDs distinguish players. Player notes link to team, position, source, review and change notes. This supports traversal without duplicating all evidence in the ranking table.

### Evidence discipline

The official FPL API is authoritative for game registration and identifiers. Public posts and reporting explain role, transfers, injuries, preseason and tactics. Each material claim must cite a specific source item.

## Skills created

- `run-fpl-review`
- `sync-fpl-api`
- `collect-public-evidence`
- `assess-preseason`
- `assess-transfer-risk`
- `rank-draft-board`
- `document-fpl-review`
- `maintain-obsidian-vault`

## Evidence considered but not adopted

- **One giant FPL skill:** rejected because it would mix stable rules, retrieval, ranking, transfer analysis and documentation into excessive context.
- **A separate current ranking in the wiki:** rejected because two current rankings would inevitably diverge.
- **Pre-populating a player order from memory:** rejected because the current FPL API and source review have not yet been run.
- **Organising primary player notes by date:** rejected because entity notes need stable paths. Date organisation is used for reviews and changes; entities link back to them.
- **Using player names as identifiers:** rejected because names, clubs and positions can change.

## Current result

The repository now has a documented operating contract and empty canonical board awaiting the first evidence-based run. No player ranking changed because no prior ranking existed and no player research was performed in this foundation review.

## Uncertainties and next triggers

- Run the official API reconciliation.
- Conduct the initial X, club, reporter, tactical, fixture, preseason and transfer scan.
- Populate the top-220 board and entity notes.
- Reassess segment boundaries after observing the first ranking distribution; boundaries are planning aids and may be revised with a recorded rationale.

## Sources

- User project requirements supplied on 2026-08-01 at 12:54 AEST.
- [Matt Pocock, agent-rules-books usage guidance](https://github.com/mattpocock/agent-rules-books/blob/main/docs/USAGE.md), retrieved 2026-08-01.
- [Official FPL bootstrap endpoint](https://fantasy.premierleague.com/api/bootstrap-static/), designated as the canonical player source; data not yet reconciled in this foundation review.

## Files changed

See [[../../../00 Meta/Document Changelog]].
