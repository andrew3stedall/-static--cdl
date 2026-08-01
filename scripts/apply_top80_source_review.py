#!/usr/bin/env python3
"""Apply the second evidence-based FPL Draft review to the canonical board.

The first board preserved a useful official-ID baseline but inherited too much of a
last-season points ordering. This script applies a reviewed top-80 order, then keeps
the prior relative order for the remaining player pool. Official FPL data remains
authoritative for identity, team, position and availability metadata.
"""
from __future__ import annotations

import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOARD_PATH = ROOT / "vault/01 Current/Current Draft Board.md"
SNAPSHOT_PATH = ROOT / "vault/09 Data/2026-08-01-1848-official-api-snapshot.json"
MOVEMENTS_PATH = ROOT / "vault/09 Data/2026-08-01-1848-top80-movements.json"
BOOTSTRAP_URL = "https://fantasy.premierleague.com/api/bootstrap-static/"
FIXTURES_URL = "https://fantasy.premierleague.com/api/fixtures/"
RUN_AT = "2026-08-01T18:48:00+10:00"
REVIEW_LINK = "[[06 Reviews/2026/08/2026-08-01/1848-AEST-review]]"

# Explicitly reviewed order. Stable official FPL element IDs are used throughout.
TOP_80_IDS = [
    411, 426, 12, 379, 106, 154, 55, 4,
    480, 165, 427, 428, 397, 25, 366, 40,
    452, 356, 13, 260, 346, 236, 398, 367,
    201, 229, 68, 70, 368, 155, 481, 95,
    96, 14, 15, 223, 527, 388, 391, 387,
    498, 112, 399, 400, 401, 525, 542, 237,
    94, 335, 338, 526, 208, 121, 122, 79,
    439, 490, 463, 465, 453, 431, 156, 512,
    515, 499, 142, 143, 533, 204, 6, 5,
    1, 384, 226, 82, 198, 84, 544, 261,
]

ROW_RE = re.compile(
    r"^\|\s*(?P<rank>\d+)\s*\|\s*(?P<player>[^|]+?)\s*\|\s*(?P<position>[^|]+?)\s*\|\s*"
    r"(?P<team>[^|]+?)\s*\|\s*(?P<segment>[^|]+?)\s*\|\s*(?P<tier>[^|]+?)\s*\|\s*"
    r"(?P<id>\d+)\s*\|\s*(?P<status>[^|]+?)\s*\|\s*(?P<changed>[^|]+?)\s*\|\s*"
    r"(?P<evidence>[^|]+?)\s*\|$"
)


def get_json(url: str):
    request = urllib.request.Request(url, headers={"User-Agent": "fpl-draft-vault/2.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response), dict(response.headers.items())


def segment(rank: int) -> str:
    if rank <= 8:
        return "Franchise"
    if rank <= 32:
        return "Foundation"
    if rank <= 80:
        return "Core"
    if rank <= 128:
        return "Depth"
    if rank <= 160:
        return "Endgame"
    return "Undrafted buffer"


def tier(rank: int) -> str:
    if rank <= 2:
        return "S"
    if rank <= 8:
        return "A+"
    if rank <= 16:
        return "A"
    if rank <= 32:
        return "B+"
    if rank <= 64:
        return "B"
    if rank <= 96:
        return "C+"
    if rank <= 128:
        return "C"
    if rank <= 160:
        return "D+"
    if rank <= 192:
        return "D"
    return "Watch"


def parse_board(text: str) -> list[dict]:
    rows: list[dict] = []
    for line in text.splitlines():
        match = ROW_RE.match(line)
        if not match:
            continue
        row = match.groupdict()
        row["rank"] = int(row["rank"])
        row["id"] = int(row["id"])
        rows.append(row)
    if len(rows) != 220:
        raise RuntimeError(f"Expected 220 existing rows, found {len(rows)}")
    return rows


def official_status(element: dict) -> str:
    news = (element.get("news") or "").strip()
    if news:
        return news
    code = element.get("status", "a")
    return {
        "a": "Available",
        "d": "Doubtful",
        "i": "Injured",
        "s": "Suspended",
        "u": "Unavailable",
        "n": "Unavailable",
    }.get(code, code)


def main() -> None:
    bootstrap, bootstrap_headers = get_json(BOOTSTRAP_URL)
    fixtures, fixtures_headers = get_json(FIXTURES_URL)

    elements = {element["id"]: element for element in bootstrap["elements"]}
    teams = {team["id"]: team for team in bootstrap["teams"]}
    positions = {position["id"]: position for position in bootstrap["element_types"]}

    missing = [element_id for element_id in TOP_80_IDS if element_id not in elements]
    if missing:
        raise RuntimeError(f"Reviewed IDs missing from official FPL API: {missing}")
    if len(TOP_80_IDS) != 80 or len(set(TOP_80_IDS)) != 80:
        raise RuntimeError("TOP_80_IDS must contain 80 unique IDs")

    old_text = BOARD_PATH.read_text(encoding="utf-8")
    old_rows = parse_board(old_text)
    old_by_id = {row["id"]: row for row in old_rows}
    old_rank = {row["id"]: row["rank"] for row in old_rows}

    ordered_ids = TOP_80_IDS + [row["id"] for row in old_rows if row["id"] not in set(TOP_80_IDS)]
    ordered_ids = ordered_ids[:220]

    new_rows: list[dict] = []
    movements: list[dict] = []
    for rank, element_id in enumerate(ordered_ids, start=1):
        element = elements[element_id]
        team = teams[element["team"]]["short_name"]
        position = positions[element["element_type"]]["singular_name_short"]
        status = official_status(element)
        player = element.get("web_name") or f"{element.get('first_name', '')} {element.get('second_name', '')}".strip()
        previous = old_by_id.get(element_id)
        previous_rank = old_rank.get(element_id)
        changed = (
            previous is None
            or previous_rank != rank
            or previous["team"] != team
            or previous["position"] != position
            or previous["status"] != status
        )
        last_changed = RUN_AT if changed else previous["changed"]
        evidence = REVIEW_LINK if changed else previous["evidence"]
        new_rows.append(
            {
                "rank": rank,
                "player": player,
                "position": position,
                "team": team,
                "segment": segment(rank),
                "tier": tier(rank),
                "id": element_id,
                "status": status,
                "changed": last_changed,
                "evidence": evidence,
            }
        )
        if previous_rank != rank:
            movements.append(
                {
                    "fpl_id": element_id,
                    "player": player,
                    "old_rank": previous_rank,
                    "new_rank": rank,
                    "delta": None if previous_rank is None else previous_rank - rank,
                    "team": team,
                    "position": position,
                }
            )

    lines = [
        "---",
        "type: current_draft_board",
        "league_managers: 8",
        "picks_per_manager: 20",
        "total_drafted: 160",
        "ranking_depth: 220",
        f"last_updated: {RUN_AT}",
        "status: top80_source_corrected_second_review",
        "---",
        "",
        "# Current Draft Board",
        "",
        "This is the **only canonical current overall ordering**. The second review corrects the first board's excessive dependence on 2025/26 total points by weighting current role, minutes security, injury status, transfer context, preseason evidence, fixture environment and positional scarcity.",
        "",
        "## Advised order",
        "",
        "| Pick order | Player | Position | Team | Segment | Tier | FPL ID | Status | Last changed | Evidence |",
        "|---:|---|---|---|---|---|---:|---|---|---|",
    ]
    for row in new_rows:
        lines.append(
            f"| {row['rank']} | {row['player']} | {row['position']} | {row['team']} | "
            f"{row['segment']} | {row['tier']} | {row['id']} | {row['status']} | "
            f"{row['changed']} | {row['evidence']} |"
        )
    lines += [
        "",
        "## Method cautions",
        "",
        "- Price and ownership do not drive the ordering, although official pricing and expert commentary are useful expectation signals.",
        "- The top 80 have been manually corrected; ranks 81-220 retain the prior relative order unless official metadata changed.",
        "- Manchester City and Chelsea transfers are not automatic promotions because competition and rotation can offset team strength.",
        "- Goalkeepers remain deliberately delayed because the position is deep relative to forwards and elite attacking midfielders.",
        "- Material future movements require dated evidence and a changes record.",
    ]
    BOARD_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")

    snapshot = {
        "retrieved_at": RUN_AT,
        "bootstrap_url": BOOTSTRAP_URL,
        "fixtures_url": FIXTURES_URL,
        "bootstrap_etag": bootstrap_headers.get("ETag") or bootstrap_headers.get("Etag"),
        "fixtures_etag": fixtures_headers.get("ETag") or fixtures_headers.get("Etag"),
        "players": len(elements),
        "teams": len(teams),
        "fixtures": len(fixtures),
        "published_rows": len(new_rows),
        "reviewed_top_rows": len(TOP_80_IDS),
        "missing_reviewed_ids": missing,
    }
    SNAPSHOT_PATH.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    MOVEMENTS_PATH.write_text(
        json.dumps(
            {
                "reviewed_at": RUN_AT,
                "movement_count": len(movements),
                "movements": sorted(movements, key=lambda item: item["new_rank"]),
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps(snapshot, indent=2))
    print(f"Recorded {len(movements)} rank changes")


if __name__ == "__main__":
    main()
