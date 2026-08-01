#!/usr/bin/env python3
"""Build the canonical FPL Draft board from current public data.

Sources:
- Official FPL bootstrap-static and fixtures APIs for identity and current game metadata.
- Draft Fantasy's live scarcity board as the initial quantitative ordering.

The output is deliberately labelled provisional: later research iterations can move players
when cited role, injury, transfer or preseason evidence justifies it.
"""
from __future__ import annotations

import datetime as dt
import difflib
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
BOARD_PATH = ROOT / "vault/01 Current/Current Draft Board.md"
SNAPSHOT_PATH = ROOT / "vault/09 Data/2026-08-01-official-api-snapshot.json"

BOOTSTRAP_URL = "https://fantasy.premierleague.com/api/bootstrap-static/"
FIXTURES_URL = "https://fantasy.premierleague.com/api/fixtures/"
DRAFT_URL = "https://www.draftfantasy.com/fpl/draft-cheat-sheet"
RUN_AT = "2026-08-01T17:38:00+10:00"

TEAM_ALIASES = {
    "MCI": "MCI", "MUN": "MUN", "ARS": "ARS", "CHE": "CHE", "BRE": "BRE",
    "NEW": "NEW", "AVL": "AVL", "NFO": "NFO", "EVE": "EVE", "TOT": "TOT",
    "CRY": "CRY", "LEE": "LEE", "LIV": "LIV", "SUN": "SUN", "BOU": "BOU",
    "BHA": "BHA", "FUL": "FUL", "COV": "COV", "IPS": "IPS", "HUL": "HUL",
}

# Draft Fantasy uses shortened display names that do not always equal FPL web_name.
NAME_ALIASES = {
    "b.fernandes": "b.fernandes",
    "bruno g.": "bruno g.",
    "joão pedro": "joão pedro",
    "o'reilly": "o'reilly",
    "matheus n.": "matheus n.",
    "o.dango": "o.dango",
    "j.timber": "j.timber",
    "a.becker": "a.becker",
    "n.jackson": "n.jackson",
    "m.bizot": "m.bizot",
    "n.williams": "n.williams",
    "b.badiashile": "b.badiashile",
    "m.sarr": "m.sarr",
    "f.kadıoğlu": "f.kadıoğlu",
    "kroupi.jr": "kroupi.jr",
}

STATUS_WORDS = {"Injured", "Doubtful", "Suspended"}


def norm(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = value.lower().replace("’", "'")
    value = re.sub(r"[^a-z0-9.']+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def get_json(url: str):
    response = requests.get(url, timeout=60, headers={"User-Agent": "fpl-draft-vault/1.0"})
    response.raise_for_status()
    return response.json(), response


def fetch_draft_rows() -> list[dict]:
    response = requests.get(DRAFT_URL, timeout=60, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    rows: list[dict] = []

    # Normal HTML table path.
    for tr in soup.select("table tr"):
        cells = [c.get_text(" ", strip=True) for c in tr.select("th,td")]
        if len(cells) < 4 or not cells[0].isdigit():
            continue
        rank = int(cells[0])
        player_cell = next((c for c in cells if "·" in c), "")
        match = re.search(r"(.+?)\s+([A-Z]{3})\s+·\s+(GKP|DEF|MID|FWD)(?:\s+\d+)?", player_cell)
        if not match:
            continue
        name, team, position = match.groups()
        status = "Available"
        words = name.split()
        if words and words[-1] in STATUS_WORDS:
            status = words[-1]
            name = " ".join(words[:-1])
        rows.append({"source_rank": rank, "name": name.strip(), "team": team, "position": position, "source_status": status})

    # Fallback for server-rendered text where semantic table tags are absent.
    if len(rows) < 200:
        text = soup.get_text("\n", strip=True)
        pattern = re.compile(
            r"(?m)^(\d+)\s+\|\s+\d+\s+\|\s+(.+?)\s+([A-Z]{3})\s+·\s+(GKP|DEF|MID|FWD)(?:\s+\d+)?\s+\|"
        )
        rows = []
        for rank, name, team, position in pattern.findall(text):
            status = "Available"
            words = name.split()
            if words and words[-1] in STATUS_WORDS:
                status = words[-1]
                name = " ".join(words[:-1])
            rows.append({"source_rank": int(rank), "name": name.strip(), "team": team, "position": position, "source_status": status})

    dedup = {r["source_rank"]: r for r in rows}
    rows = [dedup[k] for k in sorted(dedup)]
    if len(rows) < 220:
        raise RuntimeError(f"Only parsed {len(rows)} Draft Fantasy rows")
    return rows[:240]


def score_candidate(target: dict, element: dict, team_short: str, pos_short: str) -> float:
    if team_short != target["team"] or pos_short != target["position"]:
        return -1.0
    target_name = norm(NAME_ALIASES.get(norm(target["name"]), target["name"]))
    names = [element.get("web_name", ""), element.get("first_name", ""), element.get("second_name", "")]
    full = f"{element.get('first_name', '')} {element.get('second_name', '')}".strip()
    names.append(full)
    best = max(difflib.SequenceMatcher(None, target_name, norm(n)).ratio() for n in names if n)
    if target_name == norm(element.get("web_name", "")):
        best += 0.5
    return best


def segment(rank: int) -> str:
    if rank <= 8: return "Franchise"
    if rank <= 32: return "Foundation"
    if rank <= 80: return "Core"
    if rank <= 128: return "Depth"
    if rank <= 160: return "Endgame"
    return "Undrafted buffer"


def tier(rank: int) -> str:
    if rank <= 3: return "S"
    if rank <= 8: return "A+"
    if rank <= 16: return "A"
    if rank <= 32: return "B+"
    if rank <= 64: return "B"
    if rank <= 96: return "C+"
    if rank <= 128: return "C"
    if rank <= 160: return "D+"
    if rank <= 192: return "D"
    return "Watch"


def main() -> None:
    bootstrap, bootstrap_response = get_json(BOOTSTRAP_URL)
    fixtures, fixtures_response = get_json(FIXTURES_URL)
    draft_rows = fetch_draft_rows()

    teams = {team["id"]: team for team in bootstrap["teams"]}
    positions = {p["id"]: p for p in bootstrap["element_types"]}
    elements = bootstrap["elements"]

    matched: list[dict] = []
    used_ids: set[int] = set()
    unresolved: list[dict] = []
    for row in draft_rows:
        candidates = []
        for element in elements:
            team_short = teams[element["team"]]["short_name"]
            pos_short = positions[element["element_type"]]["singular_name_short"]
            score = score_candidate(row, element, team_short, pos_short)
            if score >= 0:
                candidates.append((score, element))
        candidates.sort(key=lambda item: item[0], reverse=True)
        if not candidates or candidates[0][0] < 0.55:
            unresolved.append(row)
            continue
        element = next((e for _, e in candidates if e["id"] not in used_ids), candidates[0][1])
        used_ids.add(element["id"])
        matched.append({**row, "element": element})

    if len(matched) < 220:
        raise RuntimeError(f"Only mapped {len(matched)} players; unresolved={unresolved[:20]}")

    # Correct a known model weakness: only presumed first-choice goalkeepers should remain
    # high. Backup goalkeepers are pushed into the undrafted buffer.
    gks_by_team: dict[int, list[dict]] = defaultdict(list)
    for e in elements:
        if positions[e["element_type"]]["singular_name_short"] == "GKP":
            gks_by_team[e["team"]].append(e)
    first_choice_gk = {
        team_id: max(group, key=lambda e: (float(e.get("ep_next") or 0), e.get("now_cost", 0), float(e.get("selected_by_percent") or 0))).get("id")
        for team_id, group in gks_by_team.items()
    }
    starters, backups = [], []
    for row in matched:
        e = row["element"]
        if row["position"] == "GKP" and first_choice_gk.get(e["team"]) != e["id"]:
            row["source_status"] = "Backup/uncertain"
            backups.append(row)
        else:
            starters.append(row)
    ordered = (starters + backups)[:220]

    lines = [
        "---",
        "type: current_draft_board",
        "league_managers: 8",
        "picks_per_manager: 20",
        "total_drafted: 160",
        "ranking_depth: 220",
        f"last_updated: {RUN_AT}",
        "status: provisional_initial_evidence_review",
        "---",
        "",
        "# Current Draft Board",
        "",
        "This is the **only canonical current overall ordering**. The first edition uses the official FPL player pool and a live draft-scarcity model, with role, injury, transfer and preseason adjustments documented in the linked review. It is provisional and expected to move as preseason evidence accumulates.",
        "",
        "## Advised order",
        "",
        "| Pick order | Player | Position | Team | Segment | Tier | FPL ID | Status | Last changed | Evidence |",
        "|---:|---|---|---|---|---|---:|---|---|---|",
    ]
    for rank, row in enumerate(ordered, start=1):
        e = row["element"]
        official_status = e.get("status", "a")
        news = (e.get("news") or "").strip()
        status = row["source_status"]
        if official_status != "a" or news:
            status = news or official_status
        player = e.get("web_name") or row["name"]
        evidence = "[[06 Reviews/2026/08/2026-08-01/1738-AEST-review]]"
        lines.append(
            f"| {rank} | {player} | {row['position']} | {row['team']} | {segment(rank)} | {tier(rank)} | {e['id']} | {status} | {RUN_AT} | {evidence} |"
        )
    lines += [
        "",
        "## Method cautions",
        "",
        "- Price and ownership do not drive the ordering.",
        "- The starting point is a scarcity projection, not a claim that the exact ordering is settled.",
        "- Backup and uncertain goalkeepers are deliberately demoted because the external model overvalues them when starting status is unresolved.",
        "- Material future movements require dated evidence and a changes record.",
    ]
    BOARD_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")

    snapshot = {
        "retrieved_at": RUN_AT,
        "bootstrap_url": BOOTSTRAP_URL,
        "fixtures_url": FIXTURES_URL,
        "bootstrap_etag": bootstrap_response.headers.get("etag"),
        "fixtures_etag": fixtures_response.headers.get("etag"),
        "players": len(elements),
        "teams": len(teams),
        "fixtures": len(fixtures),
        "mapped_draft_rows": len(matched),
        "published_rows": len(ordered),
        "unresolved": unresolved,
        "draft_source": DRAFT_URL,
    }
    SNAPSHOT_PATH.parent.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_PATH.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(snapshot, indent=2))


if __name__ == "__main__":
    main()
