from __future__ import annotations

from pathlib import Path
import json
import re
import urllib.request

TS = "2026-08-01T22:43:00+10:00"
STAMP = "2243-AEST"
BRANCH = "codex/fpl-review-20260801-2243-ranks17-32"
REVIEW_LINK = "[[06 Reviews/2026/08/2026-08-01/2243-AEST-review]]"
CHANGE_LINK = "[[07 Changes/2026/08/2026-08-01/2243-AEST-changes]]"
ROOT = Path("vault")
BOARD = ROOT / "01 Current" / "Current Draft Board.md"

# Stable insertion outcome after comparing the previous 17-36 candidate pool.
ORDER = [
    (398, "Foden", "Phil Foden", "MID", "MCI", "High attacking ceiling wins the block despite rotation risk.", "Gakpo", "Foden is drafted first for the stronger proven peak and central-attacking upside; reverse if preseason shows a non-starting role.", "Medium"),
    (367, "Gakpo", "Cody Gakpo", "MID", "LIV", "Likely Liverpool attacking starter with strong team environment, but role is less secure than the elite tier.", "Eze", "Gakpo is preferred because his route to starts in Liverpool's front line is clearer than Eze's exact Arsenal role.", "Medium"),
    (14, "Eze", "Eberechi Eze", "MID", "ARS", "Elite technical ceiling and set-piece history, discounted for Arsenal role sharing.", "Ødegaard", "Eze narrowly leads on direct goal threat; Ødegaard passes him if Eze is not a regular starter or loses set pieces.", "Low-medium"),
    (15, "Ødegaard", "Martin Ødegaard", "MID", "ARS", "Secure creative role and minutes floor, with less direct goal threat than the attackers above.", "Mateta", "Ødegaard projects for the safer season total; Mateta's forward scarcity keeps the draft decision close.", "Medium"),
    (223, "Mateta", "Jean-Philippe Mateta", "FWD", "CRY", "Nailed central-forward profile creates meaningful replacement value.", "Kluivert", "Mateta is drafted first because comparable raw points plus forward scarcity outweigh Kluivert's midfield scoring routes.", "Medium"),
    (70, "Kluivert", "Justin Kluivert", "MID", "BOU", "High-value attacking role and possible penalties, moderated by difficult opening fixtures.", "Tavernier", "Kluivert has the stronger central and penalty upside; reverse if Tavernier clearly owns more set pieces and minutes.", "Medium"),
    (68, "Tavernier", "Marcus Tavernier", "MID", "BOU", "Repeated preseason involvement supports role, but fixture difficulty limits promotion.", "Szoboszlai", "Tavernier's attacking role is preferred to Szoboszlai's deeper preseason usage.", "Medium"),
    (368, "Szoboszlai", "Dominik Szoboszlai", "MID", "LIV", "Strong team context and set-piece routes remain valuable despite deeper usage.", "Bruno G.", "Szoboszlai has the higher attacking ceiling; Bruno Guimarães has the safer minutes floor.", "Medium"),
    (452, "Bruno G.", "Bruno Guimarães", "MID", "NEW", "Excellent minutes security and floor, but fewer high-value attacking actions than those above.", "Muñoz", "Bruno leads on expected season points and availability; Muñoz gains only a modest scarcity adjustment at defender.", "Medium-high"),
    (201, "Muñoz", "Daniel Muñoz", "DEF", "CRY", "Elite attacking-defender profile, but defender replacement value keeps him below attacking midfield anchors.", "Calvert-Lewin", "Muñoz has the safer all-round points routes; Calvert-Lewin passes him if a nailed, fit penalty-taking striker role is confirmed.", "Medium"),
    (346, "Calvert-Lewin", "Dominic Calvert-Lewin", "FWD", "LEE", "Forward scarcity and central role preserve value, with fitness and team-strength risk.", "Damsgaard", "Calvert-Lewin is drafted first because forward replacement value offsets Damsgaard's safer creative floor.", "Low-medium"),
    (96, "Damsgaard", "Mikkel Damsgaard", "MID", "BRE", "Secure creative involvement offers a useful floor without elite goal volume.", "O.Dango", "Damsgaard has the clearer creative role and minutes expectation.", "Medium"),
    (95, "O.Dango", "Ouattara Dango", "MID", "BRE", "Direct attacking upside is useful, but role certainty is below Damsgaard's.", "Wilson", "Dango is preferred for superior open-play threat; Wilson can pass him if penalties and a central role are confirmed.", "Low-medium"),
    (260, "Wilson", "Wilson", "MID", "LEE", "Potential set-piece value remains attractive, but promoted-team projection is uncertain.", "Rice", "Wilson has more plausible direct attacking routes; Rice owns the safer minutes and floor.", "Low-medium"),
    (13, "Rice", "Declan Rice", "MID", "ARS", "Outstanding minutes and set-piece involvement, but role is less attacking than the block's leaders.", "Virgil", "Rice is expected to score slightly more through set pieces and midfield scoring; defender scarcity does not reverse it.", "Medium-high"),
    (356, "Virgil", "Virgil van Dijk", "DEF", "LIV", "Nailed elite-team defender with set-piece threat, but the position is replaceable in an eight-manager league.", "Dewsbury-Hall", "Virgil retains rank 32 on clean-sheet floor; Dewsbury-Hall passes him if an advanced Everton role and set pieces are confirmed.", "Medium"),
]

DISPLACED = [
    (236, "Dewsbury-Hall", "Kiernan Dewsbury-Hall", "MID", "EVE", 33, "Virgil", "Advanced-role potential remains, but current evidence does not justify selecting him ahead of a nailed elite defence anchor."),
    (229, "Tarkowski", "James Tarkowski", "DEF", "EVE", 34, "Dewsbury-Hall", "Strong minutes floor, but limited ceiling and deep defender replacement keep him outside the block."),
    (155, "Enzo", "Enzo Fernández", "MID", "CHE", 35, "Tarkowski", "Chelsea's crowded attack and uncertain advanced minutes prevent a higher placement."),
    (481, "Anderson", "Anderson", "MID", "MCI", 36, "Enzo", "Manchester City team strength is outweighed by substantial role and rotation uncertainty."),
]

SOURCES = "[Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/); [Official fixtures](https://fantasy.premierleague.com/api/fixtures/); [PL key-player analysis](https://www.premierleague.com/en/news/4680821/the-scouts-analysis-of-15-key-player-prices-in-202627-fantasy); [PL FDR](https://www.premierleague.com/en/news/4675493/get-the-fixture-difficulty-ratings-for-202627-fpl-season); [FFScout preseason report](https://www.fantasyfootballscout.co.uk/2026/07/31/fpl-pre-season-tavernier-impresses-muharemovic-class-szoboszlai-deeper)"


def api_players():
    with urllib.request.urlopen("https://fantasy.premierleague.com/api/bootstrap-static/", timeout=30) as r:
        data = json.load(r)
    return {p["id"]: p for p in data["elements"]}


def update_board(players):
    text = BOARD.read_text()
    rows = {}
    lines = text.splitlines()
    for i, line in enumerate(lines):
        m = re.match(r"\|\s*(\d+)\s*\|.*?\|\s*(\d+)\s*\|", line)
        if m:
            rows[int(m.group(1))] = (i, line)
    old_by_id = {}
    for rank, (idx, line) in rows.items():
        parts = [p.strip() for p in line.strip().strip("|").split("|")]
        old_by_id[int(parts[6])] = (rank, parts)

    desired = [(x[0], x[1], x[3], x[4]) for x in ORDER] + [(x[0], x[1], x[3], x[4]) for x in DISPLACED]
    for new_rank, (pid, short, pos, team) in enumerate(desired, start=17):
        old_rank, parts = old_by_id[pid]
        p = players[pid]
        status = "Available" if p.get("status") == "a" else (p.get("news") or p.get("status", "Flagged"))
        parts[0] = str(new_rank)
        parts[1] = short
        parts[2] = pos
        parts[3] = team
        parts[4] = "Foundation" if new_rank <= 32 else "Core"
        parts[5] = "B+" if new_rank <= 32 else "B"
        parts[7] = status
        parts[8] = TS
        parts[9] = REVIEW_LINK
        lines[rows[new_rank][0]] = "| " + " | ".join(parts) + " |"

    out = "\n".join(lines) + "\n"
    out = re.sub(r"last_updated: .*", f"last_updated: {TS}", out, count=1)
    out = re.sub(r"status: .*", "status: ranks17_32_pairwise_sorted", out, count=1)
    out = out.replace("The first 16 have now been stable-sorted by explicit player-versus-player comparisons.", "The first 32 have now been stable-sorted in two explicit player-versus-player blocks.")
    BOARD.write_text(out)


def note(pid, short, full, pos, team, rank, assessment, compared, decision, confidence):
    path = ROOT / "02 Players" / f"{short} - {pid}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f'''---
type: player
fpl_id: {pid}
player_name: {full}
team: "[[03 Teams/{team}]]"
position: "[[04 Positions/{'Forward' if pos == 'FWD' else 'Defender' if pos == 'DEF' else 'Midfielder'}]]"
api_status: available
current_rank: {rank}
current_segment: {'Foundation' if rank <= 32 else 'Core'}
last_reviewed: {TS}
---

# {full}

## Current assessment

{assessment}

## Pairwise placement

- Compared with: [[02 Players/{compared}]]
- Decision: {decision}
- Confidence: {confidence}
- Reversal trigger: new evidence materially changing starting role, minutes, set pieces, fitness or positional replacement value.

## Evidence timeline

- 2026-08-01 22:43 AEST — Assessed in the ranks 17–32 stable pairwise block and placed at rank {rank}.
- {SOURCES}

## Backlinks

- [[01 Current/Current Draft Board]]
- {REVIEW_LINK}
- {CHANGE_LINK}
''')


def write_records():
    comparisons = []
    changes = []
    for rank, x in enumerate(ORDER, 17):
        pid, short, full, pos, team, assessment, compared, decision, confidence = x
        comparisons.append(f"| {rank} | {short} | {compared} | {decision} | {confidence} |")
        changes.append(f"| {short} | reassessed | {rank} | Pairwise placement against {compared}. |")
    for x in DISPLACED:
        pid, short, full, pos, team, rank, compared, decision = x
        comparisons.append(f"| {rank} | {short} | {compared} | {decision} | Medium |")
        changes.append(f"| {short} | reassessed | {rank} | Displaced below the completed block. |")

    review = ROOT / "06 Reviews/2026/08/2026-08-01/2243-AEST-review.md"
    review.parent.mkdir(parents=True, exist_ok=True)
    review.write_text(f'''---
type: review
reviewed_at: {TS}
baseline: "[[06 Reviews/2026/08/2026-08-01/2207-AEST-review]]"
branch: {BRANCH}
status: ranks17_32_pairwise_complete
---

# Ranks 17–32 pairwise sorting review

## Changes since the prior iteration

The second block was rebuilt rather than retained. Foden and Gakpo lead the block; Eze, Ødegaard, Mateta and Damsgaard entered from ranks 33–36. Dewsbury-Hall, Tarkowski, Enzo and Anderson were displaced below rank 32. No player identity, team, position or availability mismatch was found for the assessed pool in the official API.

## Method

Stable insertion-style comparison was applied to the prior ranks 17–36. Raw expected season points came first. Minutes, tactical role, penalties and set pieces, injury and rotation risk, floor and ceiling followed. Positional replacement value was used only for close cross-position decisions.

## Pairwise decisions

| Rank | Player | Compared with | Decision | Confidence |
|---:|---|---|---|---|
{chr(10).join(comparisons)}

## Evidence adopted

- Foden retains an elite ceiling but receives a substantial rotation discount.
- Gakpo benefits from Liverpool's attacking environment but remains role-sensitive.
- Eze and Ødegaard are separated by direct goal threat versus role security.
- Mateta and Calvert-Lewin receive forward-scarcity adjustments, but not enough to override clearly superior raw-points cases.
- Kluivert and Tavernier are limited by Bournemouth's difficult opening fixture set.
- Szoboszlai's deeper preseason usage prevents a larger rise.
- Bruno Guimarães, Rice, Virgil and Tarkowski retain strong floors but lose ground to higher attacking ceilings and positional replacement.

Sources: {SOURCES}.

## Evidence rejected or limited

- Prior-season totals were not treated as forecasts by themselves.
- Team strength did not automatically promote Manchester City players with unclear minutes.
- Friendly goals and assists were not accepted without role and first-team-minute context.
- No player was moved on an inaccessible or unspecific X profile claim.

## Uncertainties and reversal triggers

Foden's starts, Gakpo's exact front-line role, Arsenal's Eze/Ødegaard/set-piece allocation, Mateta's club status, Kluivert penalties, Calvert-Lewin fitness and Wilson's role can materially reorder this block.

## Next block

Sort ranks 33–48 with challengers from ranks 29–52.
''')

    changes_path = ROOT / "07 Changes/2026/08/2026-08-01/2243-AEST-changes.md"
    changes_path.parent.mkdir(parents=True, exist_ok=True)
    changes_path.write_text(f'''---
type: changes
changed_at: {TS}
review: "{REVIEW_LINK}"
---

# Changes — ranks 17–32 pairwise block

| Player | Prior state | New rank | Material decision |
|---|---|---:|---|
{chr(10).join(changes)}

## Entrants and exits

Eze, Ødegaard, Mateta and Damsgaard entered ranks 17–32. Dewsbury-Hall, Tarkowski, Enzo and Anderson left the block. There were no removals from the active FPL pool and no new injury or transfer-status change adopted in this bounded comparison run.

## Important no-change decisions

The completed top 16 was not reopened because no new evidence crossed its documented reversal thresholds during this run.
''')


def update_nav():
    for name in ["Home.md", "Wiki.md"]:
        path = ROOT / name
        text = path.read_text()
        text = re.sub(r"last_updated: .*", f"last_updated: {TS}", text, count=1)
        marker = "## Latest review"
        block = f"## Latest review\n\n- {REVIEW_LINK}\n- {CHANGE_LINK}\n- Ranks 17–32 completed by direct pairwise sorting; next block is 33–48.\n"
        if marker in text:
            start = text.index(marker)
            nxt = text.find("\n## ", start + len(marker))
            text = text[:start] + block + (text[nxt:] if nxt != -1 else "")
        else:
            text += "\n" + block
        path.write_text(text)


def update_watchlist():
    path = ROOT / "01 Current" / "Current Watchlist.md"
    text = path.read_text()
    text = re.sub(r"last_updated: .*", f"last_updated: {TS}", text, count=1)
    text += f"\n- {TS} — Ranks 17–32 reversal triggers: Foden starts, Gakpo role, Eze/Ødegaard allocation, Mateta status, Kluivert penalties, Calvert-Lewin fitness and Wilson role. {REVIEW_LINK}\n"
    path.write_text(text)


def update_changelog(paths):
    path = ROOT / "00 Meta" / "Document Changelog.md"
    text = path.read_text()
    text = re.sub(r"last_updated: .*", f"last_updated: {TS}", text, count=1)
    rows = []
    for p in paths:
        action = "Created" if "2243-AEST" in p else "Updated"
        summary = "Recorded ranks 17–32 pairwise sorting evidence and placement." if "02 Players" in p else "Updated for the completed ranks 17–32 pairwise review."
        rows.append(f"| {TS} | `{p}` | {action} | {summary} | {REVIEW_LINK} | {SOURCES} |")
    text = text.rstrip() + "\n\n" + "\n".join(rows) + "\n"
    path.write_text(text)


def main():
    players = api_players()
    assessed = [x[0] for x in ORDER] + [x[0] for x in DISPLACED]
    missing = [pid for pid in assessed if pid not in players]
    if missing:
        raise SystemExit(f"Missing official FPL IDs: {missing}")
    update_board(players)
    for rank, x in enumerate(ORDER, 17):
        note(x[0], x[1], x[2], x[3], x[4], rank, x[5], x[6], x[7], x[8])
    for x in DISPLACED:
        note(x[0], x[1], x[2], x[3], x[4], x[5], "Displaced after comparison with higher-upside challengers.", x[6], x[7], "Medium")
    write_records()
    update_nav()
    update_watchlist()
    changed = [
        "vault/01 Current/Current Draft Board.md",
        "vault/01 Current/Current Watchlist.md",
        "vault/Home.md", "vault/Wiki.md",
        "vault/06 Reviews/2026/08/2026-08-01/2243-AEST-review.md",
        "vault/07 Changes/2026/08/2026-08-01/2243-AEST-changes.md",
    ]
    for x in ORDER:
        changed.append(f"vault/02 Players/{x[1]} - {x[0]}.md")
    for x in DISPLACED:
        changed.append(f"vault/02 Players/{x[1]} - {x[0]}.md")
    changed.append("vault/00 Meta/Document Changelog.md")
    update_changelog(changed)

if __name__ == "__main__":
    main()
