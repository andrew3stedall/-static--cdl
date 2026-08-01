#!/usr/bin/env python3
"""Apply the second evidence-based FPL Draft review to the canonical board.

The reviewed order is compared with the immutable 17:38 AEST official-ID order
embedded below. This makes the board and movement export deterministic and prevents
reruns from erasing the original review delta. Official FPL data remains authoritative
for identity, team, position and availability.
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
BASELINE_AT = "2026-08-01T17:38:00+10:00"
REVIEW_LINK = "[[06 Reviews/2026/08/2026-08-01/1848-AEST-review]]"

# Exact official FPL IDs from the first 220-player board on main.
BASELINE_IDS = [
    411, 426, 4, 165, 106, 397, 452, 55, 388, 13, 12, 480, 236, 387, 498, 533,
    201, 346, 481, 356, 335, 229, 260, 389, 1, 40, 391, 200, 427, 390, 67, 527,
    368, 61, 154, 155, 380, 428, 8, 25, 223, 95, 439, 112, 384, 208, 5, 136,
    143, 399, 124, 142, 532, 542, 231, 529, 327, 82, 500, 418, 68, 400, 463, 371,
    237, 398, 202, 28, 79, 465, 336, 60, 535, 473, 338, 491, 366, 84, 256, 26,
    442, 525, 226, 198, 253, 238, 130, 6, 512, 445, 350, 552, 203, 156, 415, 379,
    69, 204, 447, 392, 367, 544, 85, 269, 109, 412, 9, 94, 172, 467, 496, 469,
    261, 248, 499, 257, 429, 19, 166, 490, 14, 122, 32, 45, 96, 503, 337, 526,
    239, 417, 129, 123, 450, 114, 332, 152, 159, 448, 393, 404, 113, 516, 230,
    446, 394, 328, 149, 362, 364, 120, 504, 492, 63, 334, 543, 125, 30, 249,
    232, 471, 401, 329, 472, 396, 561, 146, 153, 150, 92, 91, 93, 117, 119, 118,
    47, 488, 81, 108, 493, 15, 193, 316, 295, 557, 347, 210, 17, 86, 377, 73,
    515, 196, 195, 194, 320, 322, 317, 553, 54, 127, 137, 549, 98, 170, 372,
    78, 453, 431, 41, 222, 102, 16, 482, 519, 461, 105, 53, 224, 139, 441,
]

# Explicitly reviewed top 80, using stable official FPL IDs.
TOP_80_IDS = [
    411, 426, 12, 379, 106, 154, 55, 4, 480, 165, 427, 428, 397, 25, 366, 40,
    452, 356, 13, 260, 346, 236, 398, 367, 201, 229, 68, 70, 368, 155, 481, 95,
    96, 14, 15, 223, 527, 388, 391, 387, 498, 112, 399, 400, 401, 525, 542, 237,
    94, 335, 338, 526, 208, 136, 122, 79, 439, 490, 463, 465, 453, 431, 156, 512,
    515, 499, 142, 143, 533, 204, 6, 5, 1, 384, 226, 82, 198, 84, 544, 261,
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
        raise RuntimeError(f"Expected 220 board rows, found {len(rows)}")
    return rows


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


def official_status(element: dict) -> str:
    news = (element.get("news") or "").strip()
    if news:
        return news
    return {
        "a": "Available",
        "d": "Doubtful",
        "i": "Injured",
        "s": "Suspended",
        "u": "Unavailable",
        "n": "Unavailable",
    }.get(element.get("status", "a"), element.get("status", "a"))


def main() -> None:
    if len(BASELINE_IDS) != 220 or len(set(BASELINE_IDS)) != 220:
        raise RuntimeError("BASELINE_IDS must contain 220 unique IDs")
    if len(TOP_80_IDS) != 80 or len(set(TOP_80_IDS)) != 80:
        raise RuntimeError("TOP_80_IDS must contain 80 unique IDs")

    bootstrap, bootstrap_headers = get_json(BOOTSTRAP_URL)
    fixtures, fixtures_headers = get_json(FIXTURES_URL)
    elements = {element["id"]: element for element in bootstrap["elements"]}
    teams = {team["id"]: team for team in bootstrap["teams"]}
    positions = {position["id"]: position for position in bootstrap["element_types"]}

    missing = [element_id for element_id in TOP_80_IDS if element_id not in elements]
    if missing:
        raise RuntimeError(f"Reviewed IDs missing from official FPL API: {missing}")

    current_rows = parse_board(BOARD_PATH.read_text(encoding="utf-8"))
    current_by_id = {row["id"]: row for row in current_rows}
    baseline_rank = {element_id: rank for rank, element_id in enumerate(BASELINE_IDS, start=1)}
    reviewed = set(TOP_80_IDS)
    ordered_ids = (TOP_80_IDS + [element_id for element_id in BASELINE_IDS if element_id not in reviewed])[:220]

    new_rows: list[dict] = []
    movements: list[dict] = []
    for rank, element_id in enumerate(ordered_ids, start=1):
        element = elements[element_id]
        team = teams[element["team"]]["short_name"]
        position = positions[element["element_type"]]["singular_name_short"]
        status = official_status(element)
        player = element.get("web_name") or f"{element.get('first_name', '')} {element.get('second_name', '')}".strip()
        current = current_by_id.get(element_id)
        old_rank = baseline_rank.get(element_id)
        changed_from_baseline = old_rank != rank
        if current is None:
            changed_from_baseline = True
        elif current["team"] != team or current["position"] != position or current["status"] != status:
            changed_from_baseline = True
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
                "changed": RUN_AT if changed_from_baseline else current["changed"],
                "evidence": REVIEW_LINK if changed_from_baseline else current["evidence"],
            }
        )
        if old_rank != rank:
            movements.append(
                {
                    "fpl_id": element_id,
                    "old_rank": old_rank,
                    "new_rank": rank,
                    "delta": None if old_rank is None else old_rank - rank,
                }
            )

    removed_ids = [element_id for element_id in BASELINE_IDS if element_id not in ordered_ids]
    entrant_ids = [element_id for element_id in ordered_ids if element_id not in baseline_rank]

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
        "baseline_reviewed_at": BASELINE_AT,
        "bootstrap_url": BOOTSTRAP_URL,
        "fixtures_url": FIXTURES_URL,
        "bootstrap_etag": bootstrap_headers.get("ETag") or bootstrap_headers.get("Etag"),
        "fixtures_etag": fixtures_headers.get("ETag") or fixtures_headers.get("Etag"),
        "players": len(elements),
        "teams": len(teams),
        "fixtures": len(fixtures),
        "baseline_rows": len(BASELINE_IDS),
        "published_rows": len(new_rows),
        "reviewed_top_rows": len(TOP_80_IDS),
        "missing_reviewed_ids": missing,
    }
    SNAPSHOT_PATH.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    MOVEMENTS_PATH.write_text(
        json.dumps(
            {
                "reviewed_at": RUN_AT,
                "baseline_reviewed_at": BASELINE_AT,
                "movement_count": len(movements),
                "entrants": [
                    {"fpl_id": element_id, "new_rank": ordered_ids.index(element_id) + 1}
                    for element_id in entrant_ids
                ],
                "removed_from_board": [
                    {"fpl_id": element_id, "old_rank": baseline_rank[element_id]}
                    for element_id in removed_ids
                ],
                "movements": movements,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps(snapshot, indent=2))
    print(f"Recorded {len(movements)} rank changes against immutable baseline")


if __name__ == "__main__":
    main()
