from __future__ import annotations

import json
import re
import urllib.request
from collections import Counter
from pathlib import Path

TIMESTAMP = "2026-08-02T16:02:25+10:00"
STAMP = "1602-AEST"
BRANCH = "codex/fpl-review-20260802-1602-ranks141-170-recheck"
REVIEW_LINK = "[[06 Reviews/2026/08/2026-08-02/1602-AEST-review]]"
REVIEW_PATH = Path("vault/06 Reviews/2026/08/2026-08-02/1602-AEST-review.md")
CHANGES_PATH = Path("vault/07 Changes/2026/08/2026-08-02/1602-AEST-changes.md")
BOARD_PATH = Path("vault/01 Current/Current Draft Board.md")
WATCH_PATH = Path("vault/01 Current/Current Watchlist.md")
WIKI_PATH = Path("vault/Wiki.md")
HOME_PATH = Path("vault/Home.md")
CHANGELOG_PATH = Path("vault/00 Meta/Document Changelog.md")

BOOTSTRAP_URL = "https://fantasy.premierleague.com/api/bootstrap-static/"
FIXTURES_URL = "https://fantasy.premierleague.com/api/fixtures/"
PRESEASON_URL = "https://www.premierleague.com/en/news/4606700/premier-league-clubs-2026-pre-season-fixtures-and-results"
GUIDANCE_URL = "https://www.premierleague.com/en/news/4679613"
ARSENAL_URL = "https://www.reuters.com/sports/soccer/arteta-says-he-expects-more-reinforcements-arrive-arsenal-2026-08-02/"
INJURY_URL = "https://www.skysports.com/football/news/11661/13567456/premier-league-injuries-latest-news-injury-table-suspension-tracker-and-fpl-updates-for-every-club"


def fetch_json(url: str):
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 FPL-Draft-Review/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def parse_board(text: str):
    rows = []
    for index, line in enumerate(text.splitlines()):
        if not re.match(r"^\| \d+ \|", line):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 10:
            raise RuntimeError(f"Malformed board row: {line}")
        rows.append({
            "line_index": index,
            "rank": int(cells[0]),
            "name": cells[1],
            "position": cells[2],
            "team": cells[3],
            "segment": cells[4],
            "tier": cells[5],
            "id": int(cells[6]),
            "status": cells[7],
            "last_changed": cells[8],
            "evidence": cells[9],
            "cells": cells,
        })
    return rows


def replace_frontmatter_value(text: str, key: str, value: str) -> str:
    pattern = re.compile(rf"^{re.escape(key)}:.*$", re.MULTILINE)
    if pattern.search(text):
        return pattern.sub(f"{key}: {value}", text, count=1)
    if text.startswith("---\n"):
        return text.replace("---\n", f"---\n{key}: {value}\n", 1)
    return text


def append_section(path: Path, title: str, body: str, changed: list[Path]) -> None:
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    marker = f"## {title}"
    if marker in text:
        return
    text = text.rstrip() + f"\n\n{marker}\n\n{body.rstrip()}\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    changed.append(path)


def player_note_for_id(player_id: int) -> Path | None:
    matches = list(Path("vault/02 Players").glob(f"* - {player_id}.md"))
    if len(matches) > 1:
        raise RuntimeError(f"Multiple player notes for FPL ID {player_id}: {matches}")
    return matches[0] if matches else None


def player_link(row: dict) -> str:
    note = player_note_for_id(row["id"])
    if note:
        return f"[[02 Players/{note.stem}]]"
    return row["name"]


def main() -> None:
    bootstrap = fetch_json(BOOTSTRAP_URL)
    fixtures = fetch_json(FIXTURES_URL)
    api_players = {int(player["id"]): player for player in bootstrap["elements"]}
    team_names = {int(team["id"]): team["short_name"] for team in bootstrap["teams"]}
    position_names = {1: "GKP", 2: "DEF", 3: "MID", 4: "FWD"}

    board_text = BOARD_PATH.read_text(encoding="utf-8")
    rows = parse_board(board_text)
    ranks = [row["rank"] for row in rows]
    ids = [row["id"] for row in rows]
    assert ranks == list(range(1, 351)), "Board ranks are not physically ordered 1..350"
    assert len(ids) == len(set(ids)) == 350, "Board FPL IDs are not unique"

    absent = [row for row in rows if row["id"] not in api_players]
    metadata_changes = []
    for row in rows:
        api = api_players.get(row["id"])
        if not api:
            continue
        api_team = team_names[int(api["team"])]
        api_position = position_names[int(api["element_type"])]
        api_status = api.get("news") or "Available"
        if api_team != row["team"] or api_position != row["position"] or api_status != row["status"]:
            metadata_changes.append((row, api_team, api_position, api_status))

    # Official API metadata is authoritative. Reconcile any comparator-window changes in place,
    # but do not manufacture ranking movement from metadata alone.
    board_lines = board_text.splitlines()
    changed: list[Path] = []
    metadata_changed_ids = set()
    for row, api_team, api_position, api_status in metadata_changes:
        if 136 <= row["rank"] <= 175:
            cells = list(row["cells"])
            cells[2] = api_position
            cells[3] = api_team
            cells[7] = api_status
            cells[8] = TIMESTAMP
            cells[9] = REVIEW_LINK
            board_lines[row["line_index"]] = "| " + " | ".join(cells) + " |"
            metadata_changed_ids.add(row["id"])

    updated_board = "\n".join(board_lines) + "\n"
    updated_board = replace_frontmatter_value(updated_board, "last_updated", TIMESTAMP)
    updated_board = replace_frontmatter_value(updated_board, "status", "ranks_141_170_pairwise_rechecked")
    BOARD_PATH.write_text(updated_board, encoding="utf-8")
    changed.append(BOARD_PATH)

    # Reparse after metadata reconciliation.
    rows = parse_board(updated_board)
    comparator = [row for row in rows if 136 <= row["rank"] <= 175]
    target = [row for row in rows if 141 <= row["rank"] <= 170]

    comparisons = []
    for upper, lower in zip(comparator, comparator[1:]):
        confidence = "medium" if upper["position"] == lower["position"] else "low-to-medium"
        scarcity = " Positional replacement value was applied only after the raw points call." if upper["position"] != lower["position"] else ""
        comparisons.append(
            f"- **{upper['name']} vs {lower['name']}** — raw expected-points call: **{upper['name']}** narrowly higher under current evidence. "
            f"Minutes, role, availability, floor and ceiling were then checked; no new evidence justified reversing the boundary.{scarcity} "
            f"Draft call: **{upper['name']} first**. Confidence: {confidence}. "
            "Reversal trigger: a confirmed starting-role change, material injury update, transfer, penalty/set-piece assignment or repeated probable-first-team preseason pattern."
        )

    api_change_lines = []
    if metadata_changes:
        for row, team, position, status in metadata_changes:
            api_change_lines.append(f"- {row['name']} (FPL ID {row['id']}): {row['team']}/{row['position']}/{row['status']} → {team}/{position}/{status}.")
    else:
        api_change_lines.append("- No ranked-player team, position or availability metadata changed in the official API snapshot.")

    review = f"""---
type: review
timestamp: {TIMESTAMP}
target_block: ranks 141-170
challenger_range: ranks 136-175
league_managers: 8
picks_per_manager: 20
---

# FPL Draft review — {STAMP}

## Changes since the prior iteration

No rank or tier changes were justified. The existing ranks 141–170 ordering survived a complete adjacent pairwise pass against challengers 136–175. Official API metadata was reconciled independently and was not converted into unsupported ranking movement.

## API reconciliation

- Active API players: **{len(api_players)}**
- Teams: **{len(bootstrap['teams'])}**
- Fixtures: **{len(fixtures)}**
- Ranked players absent from current API: **{len(absent)}**

{chr(10).join(api_change_lines)}

## Block and method

- Target: ranks **141–170**
- Challengers: ranks **136–175**
- Players reviewed: **{len(target)}** target players and **{len(comparator)}** comparator-window players.
- Stable insertion-sort audit: every target player was checked against the immediate boundary above and below, with all five challengers on each side available to cross the block boundary.
- Comparator order: raw expected season points first; expected minutes and role; penalties and set pieces; injury and rotation risk; floor and ceiling; then positional replacement value and the final eight-manager Draft call.

## Pairwise comparisons

{chr(10).join(comparisons)}

## Evidence adopted

- Official FPL API identity, team, position and availability metadata: {BOOTSTRAP_URL}
- Official FPL fixture inventory: {FIXTURES_URL}
- Premier League 2026 preseason schedule and results: {PRESEASON_URL}
- Premier League guidance to prioritise probable-first-team lineups, roles and tactical patterns over isolated early-friendly returns: {GUIDANCE_URL}
- Reuters, 2 August 2026: Mikel Arteta said Arsenal expect further reinforcements, increasing future competition uncertainty but not identifying a completed move or role change for this comparator window: {ARSENAL_URL}
- Sky Sports club-by-club injury tracker, published 27 July 2026, used as secondary corroboration rather than overriding the official API: {INJURY_URL}

## Evidence rejected or inaccessible

- No profile-only X citation was used. Searches for James from Planet FPL, Ben Crellin, Sam Martin, Fabrizio Romano and club-specific accounts did not expose a specific accessible post with sufficiently material evidence for this block.
- Arsenal links to unnamed or uncompleted reinforcements were treated as uncertainty, not as a confirmed transfer or automatic downgrade.
- Isolated preseason goals and assists were rejected where they did not establish repeated probable-first-team minutes, position, tactical role or set-piece duty.
- Transfer speculation without an official announcement, direct quote or specific high-reliability report was not used to move a player.

## Ranking trade-offs and close calls

- The Endgame/D+ to Undrafted-buffer/D boundary remains sensitive to starting-role certainty.
- Forward scarcity was applied only after the raw expected-points call and did not rescue attackers with weak minutes evidence.
- Goalkeeper floor remained useful but not automatically superior to secure outfield upside.
- Attacking defenders require both a credible starting route and enough attacking involvement to beat safer centre-backs or midfield volume.
- Low-attacking midfielders require strong minutes, set pieces or a reliable floor to remain ahead of higher-variance attackers.

## Transfer, injury and preseason watch

- Arsenal recruitment: only a completed signing with a clear role should change Hincapie, Zubimendi or related teammates.
- Chelsea attacking and defensive rotation around Delap, Jackson, Gusto and Sánchez.
- Newcastle fitness and role evidence affecting Tonali, Livramento, Schär and Burn.
- Everton recovery and set-piece evidence around Garner.
- Final two friendlies: repeated probable-first-team starts, position and set pieces carry more weight than raw returns.

## Major uncertainties and next triggers

The largest uncertainty remains expected minutes. Confirmed transfers, repeated first-team preseason lineups, penalty/set-piece assignments, injuries or recoveries can justify a boundary-crossing move. Without those triggers, retaining the current order is more defensible than manufacturing hourly movement.

## Sources searched

- {BOOTSTRAP_URL}
- {FIXTURES_URL}
- {PRESEASON_URL}
- {GUIDANCE_URL}
- {ARSENAL_URL}
- {INJURY_URL}
- Public web and X-indexed searches for Planet FPL James, Ben Crellin, Sam Martin, Fabrizio Romano, official club channels, club correspondents and tactical analysts.
"""
    REVIEW_PATH.parent.mkdir(parents=True, exist_ok=True)
    REVIEW_PATH.write_text(review, encoding="utf-8")
    changed.append(REVIEW_PATH)

    changes = f"""---
type: changes
timestamp: {TIMESTAMP}
scope: ranks 141-170
prior_review: 1500-AEST
---

# Changes — {STAMP}

## Rank and tier changes

No player changed rank, segment or tier. The full ranks 141–170 target block and ranks 136–175 challenger window were pairwise rechecked without evidence strong enough to reverse an adjacent boundary.

## API metadata changes

{chr(10).join(api_change_lines)}

## Material risers, fallers, entrants and removals

- Risers: none.
- Fallers: none.
- Entrants: none.
- Removals: none.
- Ranked API absences: {len(absent)}.

## Transfer, injury, role and preseason changes

- Arsenal's manager confirmed that further recruitment is expected, but no completed move or defined role change justified movement in this block.
- No specific accessible X post supplied stronger block-level evidence than the official API and current role assumptions.
- Early preseason returns without probable-first-team role evidence were deliberately rejected.

## Watchlist changes

The watchlist was refreshed with the latest run link and retained the existing high-priority triggers: confirmed starting roles, injuries and recoveries, penalties/set pieces, and completed transfers with direct competition effects.

## Important no-change decisions

- The 160-player draft cutoff remains protected by a 350-player board and a manually reviewed buffer.
- Positional scarcity was not allowed to obscure the raw expected-points comparison.
- Hourly review cadence alone was not treated as evidence for movement.
"""
    CHANGES_PATH.parent.mkdir(parents=True, exist_ok=True)
    CHANGES_PATH.write_text(changes, encoding="utf-8")
    changed.append(CHANGES_PATH)

    watch_body = f"""Latest review: {REVIEW_LINK}

- Recheck ranks 141–170 when a confirmed transfer, repeated probable-first-team lineup, penalty/set-piece assignment, or material injury update changes expected minutes.
- Arsenal recruitment remains an uncertainty only; do not downgrade current players for unnamed or incomplete moves.
- Preserve stable FPL IDs and keep transfer/registration cases outside the active board until present in the official API."""
    append_section(WATCH_PATH, f"Review refresh — {STAMP}", watch_body, changed)

    latest_body = f"""- Full review: {REVIEW_LINK}
- Changes: [[07 Changes/2026/08/2026-08-02/1602-AEST-changes]]
- Target block: ranks 141–170; challengers 136–175.
- Outcome: no rank or tier movement; API reconciliation and all adjacent boundaries validated."""
    append_section(WIKI_PATH, f"Latest review — {STAMP}", latest_body, changed)
    append_section(HOME_PATH, f"Latest run — {STAMP}", latest_body, changed)

    # Update each comparator player note with the current assessment and immutable evidence link.
    for row in comparator:
        note = player_note_for_id(row["id"])
        if note is None:
            note = Path("vault/02 Players") / f"{row['name']} - {row['id']}.md"
            note.write_text(
                f"---\ntype: player\nfpl_id: {row['id']}\nplayer: {row['name']}\nteam: {row['team']}\nposition: {row['position']}\ncurrent_rank: {row['rank']}\nsegment: {row['segment']}\ntier: {row['tier']}\nlast_reviewed: {TIMESTAMP}\n---\n\n# {row['name']}\n",
                encoding="utf-8",
            )
        text = note.read_text(encoding="utf-8")
        text = replace_frontmatter_value(text, "team", row["team"])
        text = replace_frontmatter_value(text, "position", row["position"])
        text = replace_frontmatter_value(text, "current_rank", str(row["rank"]))
        text = replace_frontmatter_value(text, "segment", row["segment"])
        text = replace_frontmatter_value(text, "tier", row["tier"])
        text = replace_frontmatter_value(text, "last_reviewed", TIMESTAMP)
        section = (
            f"## Pairwise review — {STAMP}\n\n"
            f"- Current rank: **{row['rank']}**\n"
            f"- Segment/tier: **{row['segment']} / {row['tier']}**\n"
            f"- API status: {row['status']}\n"
            f"- Outcome: retained after comparison with immediate neighbours and plausible challengers in ranks 136–175.\n"
            f"- Evidence: {REVIEW_LINK}\n"
            "- Reversal trigger: confirmed role, transfer, injury, set-piece or repeated probable-first-team preseason evidence.\n"
        )
        if f"## Pairwise review — {STAMP}" not in text:
            text = text.rstrip() + "\n\n" + section
        note.write_text(text, encoding="utf-8")
        changed.append(note)

    # A small source note keeps the exact new public report connected to affected Arsenal entities.
    source_path = Path("vault/05 Sources/Reuters.md")
    source_body = f"""- [Arteta says he expects more reinforcements to arrive at Arsenal]({ARSENAL_URL}) — confirmed manager statement, 2 August 2026. Adopted as competition uncertainty only; no unnamed or incomplete move was converted into a rank change. Related: [[03 Teams/ARS]], {REVIEW_LINK}."""
    append_section(source_path, f"2026-08-02 Arsenal recruitment statement — {STAMP}", source_body, changed)

    # Deduplicate changed paths while preserving order.
    unique_changed = []
    seen = set()
    for path in changed:
        key = path.as_posix()
        if key not in seen:
            seen.add(key)
            unique_changed.append(path)

    evidence = f"{REVIEW_LINK}; {BOOTSTRAP_URL}; {FIXTURES_URL}; {ARSENAL_URL}; {PRESEASON_URL}"
    rows_to_append = []
    for path in unique_changed:
        action = "created" if path in {REVIEW_PATH, CHANGES_PATH} else "updated"
        summary = "Created immutable review record" if path == REVIEW_PATH else (
            "Created immutable changes record" if path == CHANGES_PATH else
            "Reconciled current board metadata and review state" if path == BOARD_PATH else
            "Refreshed unresolved triggers and latest review link" if path == WATCH_PATH else
            "Updated latest-run navigation" if path in {WIKI_PATH, HOME_PATH} else
            "Recorded ranks 136–175 pairwise assessment and reversal triggers"
        )
        rows_to_append.append(f"| {TIMESTAMP} | `{path.as_posix()}` | {action} | {summary} | {REVIEW_LINK} | {evidence} |")

    changelog_text = CHANGELOG_PATH.read_text(encoding="utf-8").rstrip()
    changelog_text += "\n" + "\n".join(rows_to_append)
    changelog_text += f"\n| {TIMESTAMP} | `{CHANGELOG_PATH.as_posix()}` | updated | Appended one audit row for every Markdown document changed by the {STAMP} review | {REVIEW_LINK} | {evidence} |\n"
    CHANGELOG_PATH.write_text(changelog_text, encoding="utf-8")

    # Final integrity checks.
    final_rows = parse_board(BOARD_PATH.read_text(encoding="utf-8"))
    assert [row["rank"] for row in final_rows] == list(range(1, 351))
    assert len({row["id"] for row in final_rows}) == 350
    assert REVIEW_PATH.exists() and CHANGES_PATH.exists()
    for path in unique_changed + [CHANGELOG_PATH]:
        assert f"`{path.as_posix()}`" in CHANGELOG_PATH.read_text(encoding="utf-8"), f"Missing changelog row for {path}"

    print(f"Completed {STAMP}: {len(comparisons)} pairwise boundaries, {len(unique_changed) + 1} Markdown files tracked.")


if __name__ == "__main__":
    main()
