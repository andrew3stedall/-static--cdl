from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

TS = "2026-08-02T18:10:00+10:00"
BOARD = Path("vault/01 Current/Current Draft Board.md")
CHANGELOG = Path("vault/00 Meta/Document Changelog.md")
START = "<!-- ranked-players:start -->"
END = "<!-- ranked-players:end -->"
POSITION_FILES = {"GKP": ("Goalkeeper", 1), "DEF": ("Defender", 2), "MID": ("Midfielder", 3), "FWD": ("Forward", 4)}


def parse_board():
    rows = []
    for line in BOARD.read_text(encoding="utf-8").splitlines():
        if not re.match(r"^\| \d+ \|", line):
            continue
        c = [x.strip() for x in line.strip("|").split("|")]
        if len(c) < 10:
            raise SystemExit(f"Malformed board row: {line}")
        rows.append({"rank": int(c[0]), "name": c[1], "position": c[2], "team": c[3], "segment": c[4], "tier": c[5], "id": int(c[6]), "status": c[7]})
    if [r["rank"] for r in rows] != list(range(1, 351)):
        raise SystemExit("Canonical board is not physically ordered 1..350")
    if len({r["id"] for r in rows}) != 350:
        raise SystemExit("Canonical board contains duplicate FPL IDs")
    return rows


def player_link(r):
    return f"[[02 Players/{r['name']} - {r['id']}|{r['name']}]]"


def block(rows, heading):
    lines = [START, f"## {heading}", "", "Players are listed in canonical overall draft rank order.", ""]
    for r in rows:
        lines.append(f"{r['rank']}. {player_link(r)} — {r['position']}, {r['team']}; {r['segment']} / {r['tier']}; {r['status']}")
    lines += ["", f"Source: [[01 Current/Current Draft Board]] · generated {TS}", END]
    return "\n".join(lines)


def replace_or_append(text, generated):
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    if pattern.search(text):
        return pattern.sub(generated, text).rstrip() + "\n"
    return text.rstrip() + "\n\n" + generated + "\n"


def team_note(path, team):
    if path.exists():
        text = path.read_text(encoding="utf-8")
        return re.sub(r"last_reviewed: .*", f"last_reviewed: {TS}", text, count=1)
    return f"---\ntype: team\nteam_name: {team}\nteam_short: {team}\nlast_reviewed: {TS}\n---\n\n# {team}\n"


def position_note(path, name, element_type):
    if path.exists():
        text = path.read_text(encoding="utf-8")
        return re.sub(r"last_reviewed: .*", f"last_reviewed: {TS}", text, count=1)
    return f"---\ntype: position\nposition_name: {name}\nfpl_element_type: {element_type}\nlast_reviewed: {TS}\n---\n\n# {name}\n"


def main():
    rows = parse_board()
    by_team, by_position = defaultdict(list), defaultdict(list)
    for r in rows:
        by_team[r["team"]].append(r)
        by_position[r["position"]].append(r)

    changed = []
    for team, group in sorted(by_team.items()):
        path = Path(f"vault/03 Teams/{team}.md")
        existed = path.exists()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(replace_or_append(team_note(path, team), block(group, "Players by overall rank")), encoding="utf-8")
        changed.append((path, "Updated" if existed else "Created", f"Indexed {len(group)} ranked players for {team} in canonical order."))

    for code, (name, element_type) in POSITION_FILES.items():
        group = by_position.get(code, [])
        path = Path(f"vault/04 Positions/{name}.md")
        existed = path.exists()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(replace_or_append(position_note(path, name, element_type), block(group, "Players by overall rank")), encoding="utf-8")
        changed.append((path, "Updated" if existed else "Created", f"Indexed {len(group)} {name.lower()}s in canonical overall rank order."))

    changelog = CHANGELOG.read_text(encoding="utf-8")
    changelog = re.sub(r"last_updated: .*", f"last_updated: {TS}", changelog, count=1)
    evidence = "[[01 Current/Current Draft Board]]; `scripts/validate_draft_board.py`"
    trigger = "Team and position rank-index refresh"
    for path, action, summary in changed:
        changelog += f"\n| {TS} | `{path.as_posix()}` | {action} | {summary} | {trigger} | {evidence} |"
    changelog += f"\n| {TS} | `vault/00 Meta/Document Changelog.md` | Updated | Recorded every team and position note changed by the canonical rank-index refresh. | {trigger} | {evidence} |\n"
    CHANGELOG.write_text(changelog, encoding="utf-8")

    if sum(map(len, by_team.values())) != 350 or sum(map(len, by_position.values())) != 350:
        raise SystemExit("Entity index coverage is not exactly 350 players")
    print({"players": 350, "teams": len(by_team), "positions": {k: len(by_position.get(k, [])) for k in POSITION_FILES}, "markdown_files": len(changed) + 1})


if __name__ == "__main__":
    main()
