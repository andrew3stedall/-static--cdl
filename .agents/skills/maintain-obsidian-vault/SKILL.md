---
name: maintain-obsidian-vault
description: Maintain an Obsidian-compatible network of player, team, position, source, strategy, review and change notes with stable links and minimal duplication.
---

# Maintain the Obsidian vault

Use the repository's `vault/` directory as the vault root.

## Entity notes

- Players: `vault/02 Players/{Player Name} - {FPL ID}.md`
- Teams: `vault/03 Teams/{Team Name}.md`
- Positions: `vault/04 Positions/{Position}.md`
- Sources: `vault/05 Sources/{Source Name}.md`

Use YAML frontmatter defined in `vault/00 Meta/Entity Model.md`.

## Linking rules

- Link players to current team, FPL position, relevant sources, dated reviews and dated change records.
- Link teams to players and team-level tactical notes.
- Link positions to scarcity analysis and ranked players.
- Link source notes to specific cited posts and affected entities.
- Prefer `[[wikilinks]]` for internal notes and Markdown links for external evidence.
- Do not create duplicate notes for spelling variants; use aliases in frontmatter.

## Wiki maintenance

Update `vault/Wiki.md` after each run with:

- latest review and changes links;
- current top-level conclusions;
- key active uncertainties;
- navigation to entities and strategy;
- durable methodological decisions.

The wiki summarises and links. It must not become a second competing draft board.

## Integrity checks

- Resolve broken internal links where possible.
- Ensure FPL IDs match the official API.
- Preserve historical backlinks.
- Record every changed Markdown note in the document changelog.
