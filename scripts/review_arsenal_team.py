from __future__ import annotations

import json
import re
import urllib.request
from collections import defaultdict
from pathlib import Path

TS = "2026-08-02T17:58:00+10:00"
STAMP = "1758-AEST"
REVIEW_LINK = "[[06 Reviews/2026/08/2026-08-02/1758-AEST-review]]"
CHANGE_LINK = "[[07 Changes/2026/08/2026-08-02/1758-AEST-changes]]"
BOARD = Path("vault/01 Current/Current Draft Board.md")
TEAM = Path("vault/03 Teams/ARS.md")
CHANGELOG = Path("vault/00 Meta/Document Changelog.md")

DESIRED = [
    "Saka", "Gabriel", "Gyökeres", "Eze", "Ødegaard", "Rice", "Havertz",
    "Martinelli", "Raya", "Calafiori", "Saliba", "J.Timber", "Hincapie",
    "Zubimendi", "Merino", "Tzolis", "Madueke", "White", "G.Jesus",
    "Lewis-Skelly", "Mosquera",
]

COMPARISONS = [
    ("Saka", "Gabriel", "Saka projects for more raw points through elite attacking volume, penalties and set pieces; draft Saka first."),
    ("Gabriel", "Gyökeres", "Gyökeres may edge raw attacking points, but Gabriel's elite minutes, clean sheets, aerial threat and defender scarcity keep Gabriel narrowly ahead in this league."),
    ("Gyökeres", "Eze", "Gyökeres has the clearer central-goal role and forward scarcity; Eze has more rotation and set-piece uncertainty."),
    ("Eze", "Ødegaard", "Eze carries the higher direct goal ceiling; Ødegaard has the steadier creative floor. Draft Eze first, close confidence."),
    ("Ødegaard", "Rice", "Ødegaard's advanced role gives him the higher attacking ceiling, while Rice's set pieces and defensive contributions give the safer floor."),
    ("Rice", "Havertz", "Rice projects for more secure minutes and repeatable accumulation; Havertz's forward scarcity narrows but does not reverse the order."),
    ("Havertz", "Martinelli", "Havertz's forward classification and central-role routes beat Martinelli's winger rotation risk, despite a close raw-points case."),
    ("Martinelli", "Raya", "Martinelli's attacking ceiling should be drafted before a replaceable goalkeeper even with rotation risk."),
    ("Raya", "Calafiori", "Raya has the safer season-long minutes floor; Calafiori has more attacking upside but greater availability and rotation risk."),
    ("Calafiori", "Saliba", "Calafiori's attacking routes narrowly beat Saliba while Saliba carries an unknown-return back injury; reverse when Saliba is fully fit and starting."),
    ("Saliba", "J.Timber", "Saliba's established centre-back minutes floor beats Timber's groin recovery and wider rotation possibilities."),
    ("J.Timber", "Hincapie", "Timber has the stronger proven Arsenal role and attacking full-back ceiling when fit; Hincapie remains a hierarchy watch."),
    ("Hincapie", "Zubimendi", "Hincapie's clean-sheet access and defensive scarcity edge Zubimendi's low attacking ceiling."),
    ("Zubimendi", "Merino", "Zubimendi has the clearer minutes floor; Merino needs a repeatable advanced or emergency-forward role to reverse it."),
    ("Merino", "Tzolis", "Merino's established minutes path beats Tzolis's high-upside but uncertain winger role."),
    ("Tzolis", "Madueke", "Tzolis has the stronger recent production profile, but this is a low-confidence rotation comparison."),
    ("Madueke", "White", "Madueke's attacking ceiling beats White's uncertain starting role; White would reverse with confirmed first-choice full-back minutes."),
    ("White", "G.Jesus", "White has a more credible path to usable minutes; Jesus remains a role and fitness watch despite forward scarcity."),
    ("G.Jesus", "Lewis-Skelly", "Jesus retains greater per-start scoring upside and forward scarcity, while Lewis-Skelly's FPL midfield role limits clean-sheet value."),
    ("Lewis-Skelly", "Mosquera", "Lewis-Skelly offers more attacking upside; Mosquera is primarily centre-back depth with a lower ceiling."),
]

SOURCES = [
    "https://fantasy.premierleague.com/api/bootstrap-static/",
    "https://www.premierleague.com/en/news/4430457/who-are-the-best-arsenal-picks-in-fantasy",
    "https://www.premierleague.com/en/news/4681056/fpl-prices-revealed-for-arsenal-winger-tzolis-and-two-other-signings",
    "https://www.premierleague.com/en/news/4650977/just-how-important-is-saka-to-arsenal",
    "https://www.premierleague.com/en/news/4655472/who-are-the-best-arsenal-players-to-own-for-gameweek-37",
]


def parse_board(text: str):
    rows = []
    for idx, line in enumerate(text.splitlines()):
        if not re.match(r"^\| \d+ \|", line):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        rows.append({"idx": idx, "rank": int(cells[0]), "name": cells[1], "pos": cells[2], "team": cells[3], "segment": cells[4], "tier": cells[5], "id": int(cells[6]), "status": cells[7], "changed": cells[8], "evidence": cells[9]})
    return rows


def render(r):
    return "| " + " | ".join([str(r["rank"]), r["name"], r["pos"], r["team"], r["segment"], r["tier"], str(r["id"]), r["status"], r["changed"], r["evidence"]]) + " |"


def replace_frontmatter(text: str, key: str, value: str) -> str:
    pattern = rf"(?m)^{re.escape(key)}:.*$"
    if re.search(pattern, text):
        return re.sub(pattern, f"{key}: {value}", text, count=1)
    if text.startswith("---\n"):
        return text.replace("---\n", f"---\n{key}: {value}\n", 1)
    return text


def main():
    with urllib.request.urlopen("https://fantasy.premierleague.com/api/bootstrap-static/", timeout=30) as response:
        api = json.load(response)
    api_ids = {int(p["id"]) for p in api["elements"]}

    text = BOARD.read_text(encoding="utf-8")
    lines = text.splitlines()
    rows = parse_board(text)
    assert [r["rank"] for r in rows] == list(range(1, 351))
    assert len({r["id"] for r in rows}) == 350

    arsenal = [r for r in rows if r["team"] == "ARS"]
    by_name = {r["name"]: r for r in arsenal}
    missing = [name for name in DESIRED if name not in by_name]
    extras = [r["name"] for r in arsenal if r["name"] not in DESIRED]
    if missing or extras:
        raise SystemExit(f"Arsenal pool mismatch: missing={missing}, extras={extras}")
    if any(r["id"] not in api_ids for r in arsenal):
        raise SystemExit("An Arsenal board FPL ID is absent from the live API")

    old_rank = {r["name"]: r["rank"] for r in arsenal}
    slots = sorted(r["rank"] for r in arsenal)
    slot_meta = {r["rank"]: (r["segment"], r["tier"]) for r in rows}
    new_rows = {}
    for rank, name in zip(slots, DESIRED, strict=True):
        src = dict(by_name[name])
        src["rank"] = rank
        src["segment"], src["tier"] = slot_meta[rank]
        src["changed"] = TS
        src["evidence"] = REVIEW_LINK
        new_rows[rank] = src

    for r in rows:
        if r["rank"] in new_rows:
            lines[r["idx"]] = render(new_rows[r["rank"]])
    updated_board = "\n".join(lines) + "\n"
    BOARD.write_text(updated_board, encoding="utf-8")

    final_rows = parse_board(updated_board)
    assert [r["rank"] for r in final_rows] == list(range(1, 351))
    assert len({r["id"] for r in final_rows}) == 350
    assert [r["name"] for r in final_rows if r["team"] == "ARS"] == DESIRED

    final_arsenal = [r for r in final_rows if r["team"] == "ARS"]
    ranked_lines = ["<!-- ranked-players:start -->", "## Players by overall rank", "", "Players are listed in canonical overall draft rank order after the Arsenal internal comparison.", ""]
    for r in final_arsenal:
        ranked_lines.append(f'{r["rank"]}. [[02 Players/{r["name"]} - {r["id"]}|{r["name"]}]] — {r["pos"]}, ARS; {r["segment"]} / {r["tier"]}; {r["status"]}')
    ranked_lines += ["", f"Source: [[01 Current/Current Draft Board]] · reviewed {TS}", "<!-- ranked-players:end -->"]
    team_text = TEAM.read_text(encoding="utf-8")
    team_text = replace_frontmatter(team_text, "last_reviewed", TS)
    team_text = re.sub(r"<!-- ranked-players:start -->.*?<!-- ranked-players:end -->", "\n".join(ranked_lines), team_text, flags=re.S)
    review_section = "\n\n## 1758-AEST internal team review\n\n" + "\n".join(f"- **{a} over {b}:** {why}" for a,b,why in COMPARISONS) + f"\n\n- Review: {REVIEW_LINK}\n- Changes: {CHANGE_LINK}\n"
    team_text += review_section
    TEAM.write_text(team_text, encoding="utf-8")

    changed_md = [BOARD, TEAM]
    for r in final_arsenal:
        matches = list(Path("vault/02 Players").glob(f"* - {r['id']}.md"))
        if len(matches) != 1:
            raise SystemExit(f"Expected one player note for {r['id']}, found {matches}")
        p = matches[0]
        t = p.read_text(encoding="utf-8")
        t = replace_frontmatter(t, "current_rank", str(r["rank"]))
        t = replace_frontmatter(t, "segment", r["segment"])
        t = replace_frontmatter(t, "tier", r["tier"])
        t = replace_frontmatter(t, "last_reviewed", TS)
        marker = "## 1758-AEST Arsenal internal comparison"
        if marker not in t:
            prev = old_rank[r["name"]]
            t += f"\n\n{marker}\n\n- Previous overall rank: **{prev}**\n- New overall rank: **{r['rank']}**\n- Arsenal order: **{DESIRED.index(r['name']) + 1} of {len(DESIRED)}**\n- Placement was decided by raw expected points first, then minutes, role, set pieces, injury/rotation risk, floor/ceiling and finally positional replacement value.\n- Review: {REVIEW_LINK}\n- Changes: {CHANGE_LINK}\n"
        p.write_text(t, encoding="utf-8")
        changed_md.append(p)

    review_path = Path("vault/06 Reviews/2026/08/2026-08-02/1758-AEST-review.md")
    change_path = Path("vault/07 Changes/2026/08/2026-08-02/1758-AEST-changes.md")
    review_path.parent.mkdir(parents=True, exist_ok=True)
    change_path.parent.mkdir(parents=True, exist_ok=True)

    adopted = "\n".join(f"- {u}" for u in SOURCES)
    comps = "\n".join(f"- **{a} over {b}:** {why}" for a,b,why in COMPARISONS)
    review_path.write_text(f"""---
type: review
timestamp: {TS}
scope: Arsenal internal ordering
---

# Arsenal internal team review

## API reconciliation

The live official FPL bootstrap endpoint was fetched during generation. All 21 Arsenal players on the canonical board retained stable IDs present in the active API pool. The canonical board remained exactly 350 physically ordered ranks with 350 unique FPL IDs.

## Method

Every Arsenal player was insertion-compared within the club. Each comparison considered raw expected season points first, then expected minutes, tactical role, penalties and set pieces, injury and rotation risk, floor and ceiling. Positional replacement value was applied only after the raw-points assessment. The Arsenal players were reassigned only across the club's existing overall-rank slots, preserving every non-Arsenal player's rank.

## Final Arsenal order

""" + "\n".join(f"{i}. **{name}** — overall rank {next(r['rank'] for r in final_arsenal if r['name']==name)}" for i,name in enumerate(DESIRED,1)) + f"""

## Decisive comparisons

{comps}

## Evidence adopted

{adopted}

## Evidence rejected or limited

- Price and ownership were not used as draft value.
- Historical single-Gameweek recommendations were used only for role and scoring-route context, not copied as a season ranking.
- Tzolis's Belgian production was treated as ceiling evidence, not proof of Arsenal minutes.
- Injury flags from the live API were retained, but unknown return dates were not converted into false recovery probabilities.

## Close calls and reversal triggers

- Gabriel versus Gyökeres reverses if Gyökeres secures penalties and an uninterrupted central-forward role while Gabriel's minutes become managed.
- Eze versus Ødegaard remains close and reverses if Ødegaard reclaims a clearly more advanced role or a larger set-piece share.
- Havertz versus Martinelli reverses if Martinelli becomes the repeated first-choice left winger and Havertz loses central minutes.
- Calafiori versus Saliba reverses immediately when Saliba is fully fit and starting regularly.
- Tzolis versus Madueke depends on repeated probable-first-team starts and set-piece evidence.

## Next triggers

Monitor the next strongest-XI friendly, penalty and corner duties, Saliba and Timber training status, the left-wing hierarchy, and Havertz's central minutes.
""", encoding="utf-8")

    changes = []
    for name in DESIRED:
        nr = next(r["rank"] for r in final_arsenal if r["name"] == name)
        orank = old_rank[name]
        if nr != orank:
            changes.append(f"- **{name}: {orank} → {nr}**")
    change_path.write_text(f"""---
type: changes
timestamp: {TS}
scope: Arsenal internal ordering
---

# Changes — Arsenal internal ordering

## Rank changes

""" + "\n".join(changes) + """

## Important no-change decisions

- Saka remained Arsenal's first player and overall rank 3.
- Gabriel remained above Gyökeres after a close raw-points-versus-scarcity comparison.
- All non-Arsenal players retained their prior overall ranks.
- No player was added to or removed from the 350-player board.

## Tier and segment effects

Arsenal players inherited the segment and tier attached to their new overall-rank slot. This keeps the canonical rank, segment and tier hierarchy internally consistent.
""", encoding="utf-8")
    changed_md += [review_path, change_path]

    for nav in [Path("vault/Home.md"), Path("vault/Wiki.md")]:
        t = nav.read_text(encoding="utf-8")
        block = f"\n\n## Latest Arsenal team review\n\n- {REVIEW_LINK}\n- {CHANGE_LINK}\n"
        if REVIEW_LINK not in t:
            t += block
            nav.write_text(t, encoding="utf-8")
            changed_md.append(nav)

    watch = Path("vault/01 Current/Current Watchlist.md")
    wt = watch.read_text(encoding="utf-8")
    if REVIEW_LINK not in wt:
        wt += f"\n\n## Arsenal internal-order triggers — {STAMP}\n\n- Saliba and Timber fitness; Havertz central minutes; left-wing hierarchy among Martinelli, Tzolis and Madueke; penalty and set-piece duties.\n- Evidence: {REVIEW_LINK}\n"
        watch.write_text(wt, encoding="utf-8")
        changed_md.append(watch)

    changed_md = list(dict.fromkeys(changed_md))
    changelog = CHANGELOG.read_text(encoding="utf-8")
    evidence = "; ".join(SOURCES)
    rows_to_append = []
    for p in changed_md:
        action = "Created" if p in {review_path, change_path} else "Updated"
        rows_to_append.append(f"| {TS} | `{p.as_posix()}` | {action} | Arsenal internal player ordering and linked evidence refreshed. | {REVIEW_LINK} | {evidence} |")
    CHANGELOG.write_text(changelog.rstrip() + "\n" + "\n".join(rows_to_append) + "\n", encoding="utf-8")

    print(json.dumps({"old": old_rank, "new": {r['name']: r['rank'] for r in final_arsenal}, "changed_markdown": len(changed_md) + 1}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
