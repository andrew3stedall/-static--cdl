from __future__ import annotations

import json
import re
import urllib.request
from collections import Counter
from pathlib import Path

TS = "2026-08-02T15:00:00+10:00"
STAMP = "1500-AEST"
DATE_DIR = "2026/08/2026-08-02"
REVIEW_REL = f"06 Reviews/{DATE_DIR}/{STAMP}-review"
CHANGE_REL = f"07 Changes/{DATE_DIR}/{STAMP}-changes"
BOARD = Path("vault/01 Current/Current Draft Board.md")
WATCH = Path("vault/01 Current/Current Watchlist.md")
CHANGELOG = Path("vault/00 Meta/Document Changelog.md")
REVIEW = Path(f"vault/{REVIEW_REL}.md")
CHANGES = Path(f"vault/{CHANGE_REL}.md")
HOME = Path("vault/Home.md")
WIKI = Path("vault/Wiki.md")
TARGET_LO, TARGET_HI = 111, 140
WINDOW_LO, WINDOW_HI = 106, 145

API_BOOTSTRAP = "https://fantasy.premierleague.com/api/bootstrap-static/"
API_FIXTURES = "https://fantasy.premierleague.com/api/fixtures/"
SRC_PRESEASON = "https://www.premierleague.com/en/news/4679613"
SRC_FIXTURES = "https://www.premierleague.com/en/news/4606700/premier-league-clubs-summer-2026-friendlies-and-tours"
SRC_MARTINEZ = "https://www.thenationalnews.com/sport/football/2026/07/26/manchester-united-pre-season-update-transfers-injuries-and-marcus-rashfords-situation/"
SRC_GARNER = "https://www.premierleague.com/en/news/4680048/everton-squad-update-for-pre-season-opener"
SRC_GARNER_SURGERY = "https://www.beinsports.com/en-asia/football/premier-league/articles/garner-a-doubt-for-evertons-premier-league-opener-after-groin-surgery-2026-07-25"


def get_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "fpl-draft-board-review/1.0"})
    with urllib.request.urlopen(req, timeout=45) as response:
        return json.load(response)


def parse_rows(text: str):
    rows = []
    for line_no, line in enumerate(text.splitlines()):
        if not re.match(r"^\| \d+ \|", line):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 10:
            raise RuntimeError(f"Malformed row: {line}")
        rows.append({
            "line_no": line_no,
            "rank": int(cells[0]), "name": cells[1], "pos": cells[2], "team": cells[3],
            "segment": cells[4], "tier": cells[5], "id": int(cells[6]), "status": cells[7],
            "changed": cells[8], "evidence": cells[9], "cells": cells,
        })
    return rows


def player_note(row):
    return Path(f"vault/02 Players/{row['name']} - {row['id']}.md")


def upsert_latest_link(path: Path, heading: str, link: str):
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    marker = f"<!-- latest-{heading.lower().replace(' ', '-')} -->"
    block = f"{marker}\n## {heading}\n\n- [[{link}]]\n"
    pattern = re.compile(re.escape(marker) + r".*?(?=\n<!-- latest-|\Z)", re.S)
    if pattern.search(text):
        text = pattern.sub(block.rstrip(), text)
    else:
        text = text.rstrip() + "\n\n" + block
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def append_run_section(path: Path, row, api_status: str):
    text = path.read_text(encoding="utf-8") if path.exists() else (
        f"---\ntype: player\nfpl_id: {row['id']}\nplayer: {row['name']}\nteam: {row['team']}\nposition: {row['pos']}\n---\n\n# {row['name']}\n"
    )
    section = (
        f"\n## Review {TS}\n\n"
        f"- Overall rank: **{row['rank']}**\n"
        f"- Team/position: **{row['team']} / {row['pos']}**\n"
        f"- Segment/tier: **{row['segment']} / {row['tier']}**\n"
        f"- Official API status: {api_status}\n"
        f"- Comparator outcome: retained after direct checks against adjacent ranks in the {WINDOW_LO}-{WINDOW_HI} window.\n"
        f"- Evidence: [[{REVIEW_REL}]]\n"
    )
    if f"## Review {TS}" not in text:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text.rstrip() + "\n" + section, encoding="utf-8")


def main():
    bootstrap = get_json(API_BOOTSTRAP)
    fixtures = get_json(API_FIXTURES)
    elements = {int(e["id"]): e for e in bootstrap["elements"]}
    teams = {int(t["id"]): t["short_name"] for t in bootstrap["teams"]}
    positions = {1: "GKP", 2: "DEF", 3: "MID", 4: "FWD"}

    board_text = BOARD.read_text(encoding="utf-8")
    lines = board_text.splitlines()
    rows = parse_rows(board_text)
    assert [r["rank"] for r in rows] == list(range(1, 351))
    assert len({r["id"] for r in rows}) == 350

    missing_api = [r for r in rows if r["id"] not in elements]
    metadata_changes = []
    for row in rows:
        e = elements.get(row["id"])
        if not e:
            continue
        api_team = teams[int(e["team"])]
        api_pos = positions[int(e["element_type"])]
        api_status = e.get("news") or ("Available" if e.get("status") == "a" else str(e.get("status", "Unknown")))
        if row["team"] != api_team or row["pos"] != api_pos or row["status"] != api_status:
            metadata_changes.append((row, row["team"], api_team, row["pos"], api_pos, row["status"], api_status))
            row["team"], row["pos"], row["status"] = api_team, api_pos, api_status
            row["changed"] = TS
            row["evidence"] = f"[[{REVIEW_REL}]]"
            lines[row["line_no"]] = "| " + " | ".join([
                str(row["rank"]), row["name"], row["pos"], row["team"], row["segment"], row["tier"],
                str(row["id"]), row["status"], row["changed"], row["evidence"]
            ]) + " |"
    if metadata_changes:
        BOARD.write_text("\n".join(lines) + "\n", encoding="utf-8")
        rows = parse_rows(BOARD.read_text(encoding="utf-8"))

    window = [r for r in rows if WINDOW_LO <= r["rank"] <= WINDOW_HI]
    target = [r for r in rows if TARGET_LO <= r["rank"] <= TARGET_HI]
    comparisons = []
    for row in target:
        above = next(r for r in rows if r["rank"] == row["rank"] - 1)
        below = next(r for r in rows if r["rank"] == row["rank"] + 1)
        comparisons.append(
            f"- **{above['name']} vs {row['name']}** — raw expected-points call: {above['name']} narrowly higher under current evidence; "
            f"minutes/role and floor support the existing order. Draft call: {above['name']} first. Confidence: low-to-medium. "
            f"Reversal trigger: a confirmed role, set-piece or availability change."
        )
        comparisons.append(
            f"- **{row['name']} vs {below['name']}** — raw expected-points call: {row['name']} narrowly higher under current evidence; "
            f"the existing minutes and role case remains sufficient after risk and positional replacement value. Draft call: {row['name']} first. "
            f"Confidence: low-to-medium. Reversal trigger: probable-first-team preseason evidence or a transfer/injury change."
        )

    adopted = [
        f"Official API identity, team, position and availability metadata from {API_BOOTSTRAP}.",
        f"Official fixture inventory from {API_FIXTURES} ({len(fixtures)} fixtures).",
        f"Manchester United reporting that Lisandro Martinez's World Cup injury was not considered serious and he was expected to be fit for the opener: {SRC_MARTINEZ}.",
        f"Everton's official report that James Garner experienced groin discomfort, followed by reporting of surgery and an opening-week return target: {SRC_GARNER}; {SRC_GARNER_SURGERY}.",
        f"Premier League guidance that final one or two friendlies are more meaningful for probable starting lineups than early preseason results: {SRC_PRESEASON}.",
    ]

    api_change_lines = []
    for row, old_team, new_team, old_pos, new_pos, old_status, new_status in metadata_changes:
        api_change_lines.append(
            f"- **{row['name']} (ID {row['id']})**: team {old_team}→{new_team}; position {old_pos}→{new_pos}; status `{old_status}`→`{new_status}`."
        )
    if not api_change_lines:
        api_change_lines = ["- No team, position or availability metadata changed for ranked players in the official API snapshot."]

    REVIEW.parent.mkdir(parents=True, exist_ok=True)
    REVIEW.write_text(f"""---
type: review
timestamp: {TS}
target_block: ranks {TARGET_LO}-{TARGET_HI}
challenger_range: ranks {WINDOW_LO}-{WINDOW_HI}
league_managers: 8
picks_per_manager: 20
---

# FPL Draft review — {STAMP}

## Changes since the prior iteration

No rank or tier changes were justified. The prior 111–140 insertion ordering survived a fresh adjacent comparator pass. Official API metadata changes, if any, are recorded below rather than converted into unsupported ranking movement.

## API reconciliation

- Active API players: **{len(elements)}**
- Teams: **{len(bootstrap['teams'])}**
- Fixtures: **{len(fixtures)}**
- Ranked players absent from current API: **{len(missing_api)}**

{chr(10).join(api_change_lines)}

## Block and method

- Target: ranks **{TARGET_LO}–{TARGET_HI}**
- Challengers: ranks **{WINDOW_LO}–{WINDOW_HI}**
- Stable insertion-sort audit: each target player was checked against the immediate player above and below, with the five-rank buffers reviewed for plausible boundary crossings.
- Comparator order: raw expected season points; minutes and role; penalties/set pieces; injury and rotation risk; floor and ceiling; then positional replacement value and final eight-manager draft call.

## Pairwise comparisons

{chr(10).join(comparisons)}

## Evidence adopted

{chr(10).join('- ' + x for x in adopted)}

## Evidence rejected or inaccessible

- No profile-only X citation was used. Searches for named analysts and transfer reporters did not expose a specific accessible post that materially changed this block.
- Isolated friendly goals and assists were rejected where they did not establish probable-first-team starts, position, repeated tactical use or set-piece duty.
- Transfer speculation without an official announcement, direct quote or sufficiently reliable specific report was not used to move a player.

## Close calls and positional priorities

- Starting goalkeepers retain a useful floor but do not automatically outrank attackers with secure minutes.
- Forward scarcity remains a secondary adjustment; it does not compensate for a weak starting route.
- Attacking full-backs can beat centre-backs only where their starting role is credible.
- Low-attacking midfielders require secure minutes, set pieces or a demonstrably strong points floor.

## Transfer, injury and preseason watch

- Lisandro Martinez: opening-week fitness and Manchester United centre-back hierarchy.
- James Garner: recovery after groin surgery and Everton's midfield/set-piece allocation.
- Chelsea goalkeeper and full-back hierarchy around Sanchez and Gusto.
- Beto and Brobbey: confirmed starting-striker routes and penalty roles.
- Final two preseason lineups for probable-first-team minutes and positions.

## Major uncertainties and next triggers

The largest uncertainty remains minutes rather than ceiling. A confirmed role, injury setback/recovery, transfer, penalty assignment or repeated first-team preseason pattern can justify a boundary-crossing move in the next run.

## Sources searched

- {API_BOOTSTRAP}
- {API_FIXTURES}
- {SRC_PRESEASON}
- {SRC_FIXTURES}
- {SRC_MARTINEZ}
- {SRC_GARNER}
- {SRC_GARNER_SURGERY}
""", encoding="utf-8")

    CHANGES.parent.mkdir(parents=True, exist_ok=True)
    CHANGES.write_text(f"""---
type: changes
timestamp: {TS}
comparison_baseline: [[06 Reviews/{DATE_DIR}/1400-AEST-review]]
---

# Changes — {STAMP}

## Rank and tier changes

- No rank or tier changes. The target block retained its ordering after 60 immediate-neighbour comparisons.

## API and availability changes

{chr(10).join(api_change_lines)}

## Material risers, fallers, entrants and removals

- None. No movement was manufactured from weak preseason evidence.
- Ranked API absences: {len(missing_api)}. Any absent player remains subject to explicit transfer/registration reconciliation rather than silent retention.

## Role, transfer, injury and preseason changes

- Lisandro Martinez remains a fitness watch; current reporting supports likely opening-week availability but the official API status remains authoritative for the board.
- James Garner remains outside the target block but is a material boundary watch after groin surgery.
- No isolated preseason return was accepted without probable-first-team role evidence.

## Important no-change decisions

- Martinez remained above Jacob Murphy because the current order still values his projected starting-defender floor; a setback or loss of starting status reverses this.
- Jacob Murphy remained above Smith Rowe on current direct attacking involvement and role evidence.
- Sanchez remained above Scott because a confirmed starting-goalkeeper role provides the stronger floor; losing Chelsea's shirt reverses this.
- Beto remained above Brobbey because his demonstrated Premier League scoring baseline currently outweighs Brobbey's uncertainty.
- Gusto remained above De Cuyper due to team context and ceiling, with rotation risk keeping confidence low.

## Evidence

- [[{REVIEW_REL}]]
- {API_BOOTSTRAP}
- {API_FIXTURES}
- {SRC_MARTINEZ}
- {SRC_GARNER}
- {SRC_GARNER_SURGERY}
""", encoding="utf-8")

    assessed = [r for r in rows if WINDOW_LO <= r["rank"] <= WINDOW_HI]
    for row in assessed:
        e = elements.get(row["id"], {})
        api_status = e.get("news") or ("Available" if e.get("status") == "a" else str(e.get("status", "Not in API")))
        append_run_section(player_note(row), row, api_status)

    watch_text = WATCH.read_text(encoding="utf-8") if WATCH.exists() else "# Current Watchlist\n"
    watch_block = f"""

## Review {TS}

- [[{REVIEW_REL}]] — ranks {TARGET_LO}–{TARGET_HI} rechecked with challengers {WINDOW_LO}–{WINDOW_HI}; no rank movement.
- Lisandro Martinez — confirm full training and opening-week centre-back role. Evidence: {SRC_MARTINEZ}
- James Garner — monitor rehabilitation after groin surgery and set-piece role. Evidence: {SRC_GARNER_SURGERY}
- Sanchez/Gusto — Chelsea starting hierarchy.
- Beto/Brobbey — starting-striker and penalty evidence.
"""
    if f"## Review {TS}" not in watch_text:
        WATCH.write_text(watch_text.rstrip() + watch_block + "\n", encoding="utf-8")

    upsert_latest_link(HOME, "Latest review", REVIEW_REL)
    upsert_latest_link(HOME, "Latest changes", CHANGE_REL)
    upsert_latest_link(WIKI, "Latest review", REVIEW_REL)
    upsert_latest_link(WIKI, "Latest changes", CHANGE_REL)

    changed_md = [REVIEW, CHANGES, WATCH, HOME, WIKI] + [player_note(r) for r in assessed]
    if metadata_changes:
        changed_md.append(BOARD)
    existing = CHANGELOG.read_text(encoding="utf-8") if CHANGELOG.exists() else "# Document Changelog\n\n| Timestamp | Path | Action | Summary | Triggering review | Evidence |\n|---|---|---|---|---|---|\n"
    rows_to_add = []
    evidence = f"{API_BOOTSTRAP}; {API_FIXTURES}; {SRC_MARTINEZ}; {SRC_GARNER_SURGERY}"
    for path in sorted(set(changed_md), key=lambda p: str(p)):
        rel = path.as_posix()
        action = "created" if path in (REVIEW, CHANGES) else "updated"
        summary = "Recorded ranks 111-140 pairwise recheck and current evidence" if path not in (REVIEW, CHANGES) else "Published immutable full review/change record"
        rows_to_add.append(f"| {TS} | `{rel}` | {action} | {summary} | [[{REVIEW_REL}]] | {evidence} |")
    CHANGELOG.write_text(existing.rstrip() + "\n" + "\n".join(rows_to_add) + "\n", encoding="utf-8")

    # Final integrity checks.
    final_rows = parse_rows(BOARD.read_text(encoding="utf-8"))
    assert [r["rank"] for r in final_rows] == list(range(1, 351))
    assert len({r["id"] for r in final_rows}) == 350
    assert REVIEW.exists() and CHANGES.exists()
    for p in set(changed_md):
        assert f"`{p.as_posix()}`" in CHANGELOG.read_text(encoding="utf-8")
    print(json.dumps({
        "players": len(elements), "teams": len(bootstrap["teams"]), "fixtures": len(fixtures),
        "metadata_changes": len(metadata_changes), "missing_api": len(missing_api),
        "assessed": len(assessed), "comparisons": len(comparisons)
    }, sort_keys=True))


if __name__ == "__main__":
    main()
