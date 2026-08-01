# FPL Draft Research Vault

This repository is the canonical research and decision record for an eight-manager Fantasy Premier League Draft league with 20 selections per manager.

The project separates:

- **current state** — the single live draft board and watchlist;
- **evidence** — cited player, team, source and tactical notes;
- **history** — immutable, timestamped review and change documents;
- **agent workflows** — concise Codex skills under `.agents/skills/`.

## Start here

Open `vault/` as an Obsidian vault, then begin at [[Home]].

Repository users should read [AGENTS.md](AGENTS.md). A complete research run starts with `.agents/skills/run-fpl-review/SKILL.md` and loads only the narrower skills needed for the task.

## Canonical documents

- [Current Draft Board](vault/01%20Current/Current%20Draft%20Board.md)
- [Current Watchlist](vault/01%20Current/Current%20Watchlist.md)
- [Wiki](vault/Wiki.md)
- [Document Changelog](vault/00%20Meta/Document%20Changelog.md)
- [Repository Contract](vault/00%20Meta/Repository%20Contract.md)

## Directory map

```text
.agents/skills/       Focused Codex workflows
vault/00 Meta/        Rules, schemas, templates and changelog
vault/01 Current/     Canonical live recommendations
vault/02 Players/     One note per FPL player
vault/03 Teams/       One note per Premier League team
vault/04 Positions/   Position-level strategy and scarcity
vault/05 Sources/     Source and account notes
vault/06 Reviews/     Immutable full review records by date
vault/07 Changes/     Immutable deltas between reviews by date
vault/08 Strategy/    Durable draft strategy
vault/09 Data/        API and data-contract documentation
```

Historical records are append-only. Current documents may be replaced, but every material edit must be recorded in the timestamped changelog and linked to supporting evidence.
