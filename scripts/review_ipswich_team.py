from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TS = "2026-08-03T09:10:00+10:00"
STAMP = "0910-AEST"
REVIEW_LINK = "[[06 Reviews/2026/08/2026-08-03/0910-AEST-review]]"
CHANGES_LINK = "[[07 Changes/2026/08/2026-08-03/0910-AEST-changes]]"

players = [
    ("Hirst", 317, 205, "FWD", "Best established central-forward route and the strongest current raw-points case in the Ipswich group."),
    ("Akpom", 320, 223, "FWD", "Forward scarcity and senior scoring history keep him second, but minutes and hierarchy remain uncertain."),
    ("Al-Hamadi", 322, 226, "FWD", "Central attacking upside keeps him above the defenders, though role certainty is weak."),
    ("Diop", 259, 232, "DEF", "Defensive minutes and set-piece threat provide the safest non-forward floor."),
    ("Emersonn", 316, 234, "FWD", "Forward classification preserves speculative upside, but the first-team role is less established."),
    ("Palmer", 301, 290, "GKP", "Goalkeeper floor is replaceable and current role certainty is insufficient to move above the outfield options."),
]

board_path = ROOT / "vault/01 Current/Current Draft Board.md"
board = board_path.read_text()
# No rank changes: refresh Ipswich evidence timestamps only.
lines = board.splitlines()
for i, line in enumerate(lines):
    if not line.startswith("|"):
        continue
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) < 10 or not cells[0].isdigit() or cells[3] != "IPS":
        continue
    cells[8] = TS
    cells[9] = REVIEW_LINK
    lines[i] = "| " + " | ".join(cells) + " |"
board_path.write_text("\n".join(lines) + "\n")

team_path = ROOT / "vault/03 Teams/IPS.md"
team = team_path.read_text()
team = team.replace("last_reviewed: 2026-08-02T18:10:00+10:00", f"last_reviewed: {TS}")
team = team.replace("Source: [[01 Current/Current Draft Board]] · generated 2026-08-02T18:10:00+10:00", f"Source: [[01 Current/Current Draft Board]] · generated {TS}")
team += f"\n\n## {STAMP} team review\n\n- Full Ipswich intra-team ordering reviewed; no rank changes were justified.\n- Review: {REVIEW_LINK}.\n"
team_path.write_text(team)

for idx, (name, fpl_id, rank, pos, decision) in enumerate(players, start=1):
    p = ROOT / f"vault/02 Players/{name} - {fpl_id}.md"
    text = p.read_text()
    text += f"\n\n## {STAMP} Ipswich comparison\n\n- Ipswich order: **{idx} of {len(players)}**; overall rank **{rank}**.\n- Decision: {decision}\n- Evidence: {REVIEW_LINK}.\n"
    p.write_text(text)

review_path = ROOT / "vault/06 Reviews/2026/08/2026-08-03/0910-AEST-review.md"
review_path.parent.mkdir(parents=True, exist_ok=True)
review_path.write_text(f'''---
type: review
reviewed_at: {TS}
team: IPS
---

# Ipswich Town team ordering review

## Scope

Reviewed all six Ipswich players currently ranked on the canonical 350-player board.

## Comparator method

Raw expected FPL points were considered first, then expected minutes, role, penalties and set pieces, injury and rotation risk, floor and ceiling. Positional replacement value was applied afterward.

## Decisive comparisons

- **Hirst vs Akpom: Hirst first.** Hirst has the clearer established central-forward route; a confirmed Akpom starting role would make this close.
- **Akpom vs Al-Hamadi: Akpom first.** Senior scoring history and a broader established attacking profile outweigh Al-Hamadi's speculative upside.
- **Al-Hamadi vs Diop: Al-Hamadi first.** Raw attacking ceiling and forward scarcity narrowly beat Diop's safer defensive minutes.
- **Diop vs Emersonn: Diop first.** Diop has the stronger expected-minutes floor; repeated first-team starts for Emersonn would reverse it.
- **Emersonn vs Palmer: Emersonn first.** Outfield attacking upside beats replaceable goalkeeper value despite low confidence.

## Final Ipswich order

1. Hirst — overall 205
2. Akpom — 223
3. Al-Hamadi — 226
4. Diop — 232
5. Emersonn — 234
6. Palmer — 290

## Outcome

No rank movement was justified. The existing Ipswich ordering is internally coherent under current evidence.

## Uncertainties and reversal triggers

- Competitive first-team minutes and Ipswich's striker hierarchy remain the primary triggers.
- Penalty ownership could materially change the top three.
- Any player absent from the official FPL pool must be removed or relabelled rather than retained as an active rank.

## Validation

- No non-Ipswich rank changed.
- The canonical board validator must confirm ranks 1–350 are complete and FPL IDs unique.
''')

changes_path = ROOT / "vault/07 Changes/2026/08/2026-08-03/0910-AEST-changes.md"
changes_path.parent.mkdir(parents=True, exist_ok=True)
changes_path.write_text(f'''---
type: changes
changed_at: {TS}
team: IPS
---

# Ipswich Town ordering changes — {STAMP}

- Hirst: **205, unchanged**
- Akpom: **223, unchanged**
- Al-Hamadi: **226, unchanged**
- Diop: **232, unchanged**
- Emersonn: **234, unchanged**
- Palmer: **290, unchanged**

No non-Ipswich player rank changed. The board remains 350 unique, physically ordered ranks.
''')

for rel in ["vault/Home.md", "vault/Wiki.md"]:
    p = ROOT / rel
    text = p.read_text()
    text += f"\n\n- Latest team review: {REVIEW_LINK} · changes: {CHANGES_LINK}\n"
    p.write_text(text)

changed = [
    "vault/01 Current/Current Draft Board.md",
    "vault/03 Teams/IPS.md",
    *[f"vault/02 Players/{n} - {fid}.md" for n, fid, *_ in players],
    "vault/06 Reviews/2026/08/2026-08-03/0910-AEST-review.md",
    "vault/07 Changes/2026/08/2026-08-03/0910-AEST-changes.md",
    "vault/Home.md",
    "vault/Wiki.md",
    "vault/00 Meta/Document Changelog.md",
]
changelog = ROOT / "vault/00 Meta/Document Changelog.md"
text = changelog.read_text().rstrip() + "\n"
for path in changed:
    action = "Created" if "/0910-AEST-" in path else "Updated"
    text += f"| {TS} | `{path}` | {action} | Ipswich intra-team review; no manufactured movement | {REVIEW_LINK} | {REVIEW_LINK}; {CHANGES_LINK} |\n"
changelog.write_text(text)
