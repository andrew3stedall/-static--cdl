from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

TS = "2026-08-08T16:50:00+10:00"
R = "06 Reviews/2026/08/2026-08-08/1650-AEST-review"
C = "07 Changes/2026/08/2026-08-08/1650-AEST-changes"
BOOT = "https://fantasy.premierleague.com/api/bootstrap-static/"
FIX = "https://fantasy.premierleague.com/api/fixtures/"
PI = "https://www.premierinjuries.com/injury-table.php"
SRC = {
    "romero": "https://www.theguardian.com/football/2026/aug/07/tottenham-and-atletico-in-talks-over-romero-with-van-de-ven-set-to-sign-new-deal",
    "rodri": "https://www.theguardian.com/football/2026/aug/07/manchester-city-reject-barcelonas-opening-385m-bid-for-rodri-as-talks-continue",
    "bruno": "https://www.theguardian.com/football/2026/aug/05/arsenal-agree-75m-fee-with-newcastle-for-bruno-guimaraes-as-clubs-reach-compromise",
    "hornicek": "https://www.theguardian.com/football/2026/aug/03/premier-league-transfer-newcastle-reject-first-bid-arsenal-bruno-guimaraes",
    "chelsea_fulham": "https://www.theguardian.com/football/2026/aug/03/transfer-roundup-chelsea-sell-trevoh-chalobah-sign-jordan-henderson",
    "rumours": "https://www.theguardian.com/football/2026/aug/07/football-transfer-rumours-cristian-romero-spurs-arsenal-atletico-inter",
    "rumours2": "https://www.theguardian.com/football/2026/aug/05/football-transfer-rumours-folarin-balogun-tottenham-hotspur-pedro-neto-manchester-city",
    "rumours_gakpo": "https://www.theguardian.com/football/2026/aug/04/football-transfer-rumour-mill-chelsea-mykhailo-mudryk-lampard-coventry",
    "maeda": "https://www.theguardian.com/football/2026/jul/29/premier-league-clubs-strengthen-season-manchester-united-arsenal-midfielders-city-liverpool-chelsea",
    "rushworth": "https://www.theguardian.com/football/2026/aug/04/frank-lampard-coventry-brighton-carl-rushworth-transfer-roundup",
    "spursinj": "https://www.tottenhamhotspur.com/news/1079669/team-news-robertos-latest-on-deki-kudus-and-vicario-from-new-zealand",
}

api = json.loads(Path("/tmp/bootstrap.json").read_text())
fixtures = json.loads(Path("/tmp/fixtures.json").read_text())
elems = api["elements"]
byid = {int(x["id"]): x for x in elems}
teams = {x["id"]: x["short_name"] for x in api["teams"]}
posmap = {1: "GKP", 2: "DEF", 3: "MID", 4: "FWD"}

boardp = Path("vault/01 Current/Current Draft Board.md")
oldtxt = boardp.read_text()
oldrows = [
    [x.strip() for x in line.strip().strip("|").split("|")]
    for line in oldtxt.splitlines()
    if re.match(r"^\| \d+ \|", line)
]
assert len(oldrows) == 350
oldrank = {int(r[6]): int(r[0]) for r in oldrows}
oldname = {int(r[6]): r[1] for r in oldrows}

rows = []
for r in oldrows:
    fid = int(r[6])
    x = byid[fid]
    rr = r[:]
    rr[2] = posmap[x["element_type"]]
    rr[3] = teams[x["team"]]
    news = (x.get("news") or "").strip()
    if x["status"] == "a":
        rr[7] = "Available"
    elif news:
        rr[7] = news
    else:
        rr[7] = {"d": "Doubtful", "i": "Injured", "s": "Suspended", "u": "Unavailable"}.get(x["status"], "Unavailable")
    rows.append(rr)

# Confirmed Premier League departure: Chalobah to Como.
rows = [r for r in rows if int(r[6]) != 143]

# Newly registered players that clear the 350-player Draft buffer after manual comparison.
candidate_targets = {
    569: 108,  # Garcia, Fulham striker
    567: 114,  # Hornicek, Newcastle expected No.1
    562: 135,  # Maeda, Ipswich attacker
    148: 150,  # Hato
    183: 160,  # Rudoni
    315: 170,  # Fatawu
    383: 178,  # Elliott
    313: 185,  # Clarke
    245: 190,  # Dibling
    190: 195,  # Tchaouna
    56: 200,   # Abraham
    22: 205,   # Nwaneri
    486: 210,  # McAtee
    348: 215,  # Piroe
    521: 220,  # Kulusevski, injury discounted
    570: 225,  # Palacios
    186: 230,  # Mason-Clark
    164: 235,  # Quenda
    139: 240,  # Ferguson, injury discounted
    110: 245,  # Rushworth
    385: 250,  # Trafford
    318: 255,  # Philogene
    128: 260,  # Buonanotte
    126: 265,  # O'Riley
    100: 270,  # Carvalho
    286: 275,  # Belloumi
    568: 280,  # Barco
    247: 285,  # Hackney
    185: 290,  # Sakamoto
    184: 295,  # Grimes
    298: 300,  # Destan
    161: 305,  # Lavia
    23: 310,   # Fabio Vieira
    44: 315,   # Bailey
    216: 320,  # Esse
    72: 325,   # Gannon-Doak
}
existing_ids = {int(r[6]) for r in rows}
for fid in candidate_targets:
    if fid in existing_ids:
        continue
    x = byid[fid]
    news = (x.get("news") or "").strip()
    status = "Available" if x["status"] == "a" else (news or {"d": "Doubtful", "i": "Injured", "s": "Suspended", "u": "Unavailable"}.get(x["status"], "Unavailable"))
    rows.append(["0", x["web_name"], posmap[x["element_type"]], teams[x["team"]], "Extended watch buffer", "Watch", str(fid), status, TS, f"[[{R}]]"])

# Evidence-based insertion anchors for existing players whose old rank is materially stale.
manual = {
    380: 145,  # Ekitike: dated October return improves indefinite label
    416: 182,  # De Ligt: dated September return
    500: 210,  # Romero: advanced PL-exit risk
    137: 220,  # Tzimas: ACL September return
    440: 235,  # Zirkzee: overseas loan risk
    472: 245,  # Murillo: dated August return
    402: 265,  # Rodri: surgery + Barcelona talks
    459: 270,  # Miley: dated August return
    27: 275,   # Gabriel Jesus: Napoli interest
    43: 286,   # Tielemans: uncertain return
    442: 300,  # Pope: Hornicek expected No.1
    102: 330,  # Yarmoliuk: no return date
    513: 340,  # Xavi Simons: ACL to Feb 2027
    48: 345,   # Onana: ACL rupture
    **candidate_targets,
}
overrides = {
    452: "Transfer agreed to Arsenal; completion/registration watch",
    500: "Advanced Atletico talks; PL-exit risk; knee issue under assessment",
    402: "Barcelona talks; back surgery; major PL-exit risk",
    440: "Juventus loan interest; PL-exit risk",
    27: "Napoli interest; Arsenal open-to-sale reports",
    442: "Hornicek expected Newcastle No.1; Pope exit risk",
    513: "ACL; Premier Injuries potential return 20 Feb 2027",
    48: "ACL rupture; no credible near-term return",
    380: "Post-surgery rehab; Premier Injuries potential return 12 Oct 2026",
    416: "Back surgery; Premier Injuries potential return 6 Sep 2026",
    137: "ACL rehab; Premier Injuries potential return 12 Sep 2026",
    450: "Calf surgery; Premier Injuries potential return 23 Aug 2026",
    459: "Leg/calf rehab; Premier Injuries potential return 23 Aug 2026",
    472: "Thigh rehab; Premier Injuries potential return 22 Aug 2026",
    43: "Thigh injury; return date remains uncertain",
    102: "Undisclosed absence; no return date",
    512: "Thigh issue; manager says very close to training return",
    567: "Newcastle signing; expected first-choice goalkeeper",
    569: "Fulham striker signing; starting-role competition to monitor",
    562: "Ipswich attacking signing; role upside",
    110: "Coventry club-record goalkeeper signing; first-choice pathway",
}
for r in rows:
    fid = int(r[6])
    if fid in overrides:
        r[7] = overrides[fid]


def order_key(r):
    fid = int(r[6])
    anchor = manual.get(fid, oldrank.get(fid, candidate_targets.get(fid, 999)))
    return (float(anchor), oldrank.get(fid, 1000), fid)

rows = sorted(rows, key=order_key)[:350]


def segment_tier(rank: int):
    if rank <= 8:
        return "Franchise", "S" if rank <= 2 else "A+"
    if rank <= 32:
        return "Foundation", "A" if rank <= 16 else "B+"
    if rank <= 80:
        return "Core", "B" if rank <= 48 else ("B-" if rank <= 65 else "C+")
    if rank <= 128:
        return "Depth", "C"
    if rank <= 160:
        return "Endgame", "D+"
    if rank <= 220:
        return "Undrafted buffer", "D"
    return "Extended watch buffer", "Watch"

for rank, r in enumerate(rows, 1):
    r[0] = str(rank)
    r[4], r[5] = segment_tier(rank)
    fid = int(r[6])
    if oldrank.get(fid) != rank or fid in overrides or fid in candidate_targets:
        r[8] = TS
        r[9] = f"[[{R}]]"

newrank = {int(r[6]): int(r[0]) for r in rows}
current_ids = set(newrank)
entrants = [fid for fid in current_ids if fid not in oldrank]
removals = [fid for fid in oldrank if fid not in current_ids]

header = oldtxt.split("## Advised order")[0]
header = re.sub(r"last_updated: .*", f"last_updated: {TS}", header, count=1)
header = re.sub(r"status: .*", "status: final_full_board_sweep_complete", header, count=1)
intro = f'''## Advised order

The full 350-player board was swept top-to-bottom in 20-player blocks with five-player boundary buffers on 8 August 2026. The official FPL pool was reconciled before ranking; transfer-exit risk and injury evidence outside FPL metadata were then applied.

**Draft roster guardrail:** across 20 selections, ensure the final squad contains at least **2 GKP, 5 DEF, 8 MID and 3 FWD**; the remaining two slots are flexible. Once remaining selections equal the number of still-required positional slots, positional need overrides a marginal overall-rank edge.

| Pick order | Player | Position | Team | Segment | Tier | FPL ID | Status | Last changed | Evidence |
|---:|---|---|---|---|---|---:|---|---|---|
'''
body = "\n".join("| " + " | ".join(r) + " |" for r in rows)
cautions = '''
## Method cautions

- Price and ownership are expectation signals only and do not drive Draft ordering.
- Short injuries are discounted lightly on a season-long Draft horizon; multi-month, ACL and surgery cases are discounted materially.
- Confirmed departures leave the active board; advanced talks create material risk; ordinary interest is a watch, not an automatic demotion.
- Position scarcity is applied only after raw season-points expectation.
- Material future movements require dated evidence and a changes record.
'''
boardp.write_text(header + intro + body + cautions)

changed: list[str] = ["vault/01 Current/Current Draft Board.md"]
created_notes: set[str] = set()

# Synchronise/create every ranked player note.
for r in rows:
    rank, name, position, team, _, _, fid_s, status, _, _ = r
    fid = int(fid_s)
    filename_name = oldname.get(fid, name)
    p = Path(f"vault/02 Players/{filename_name} - {fid}.md")
    existed = p.exists()
    if existed:
        s = p.read_text()
        s = re.sub(r"(?m)^(current_rank: )\d+", rf"\g<1>{rank}", s, count=1)
        s = re.sub(r"(?m)^(team: ).*", rf"\g<1>{team}", s, count=1)
        s = re.sub(r"(?m)^(position: ).*", rf"\g<1>{position}", s, count=1)
        s = re.sub(r"(?m)^(last_reviewed: ).*", rf"\g<1>{TS}", s, count=1)
    else:
        s = f"""---\ntype: player\nfpl_id: {fid}\nplayer: {name}\nteam: {team}\nposition: {position}\ncurrent_rank: {rank}\nlast_reviewed: {TS}\n---\n\n# {name}\n"""
        created_notes.add(str(p))
    if oldrank.get(fid) != int(rank) or fid in overrides or fid in entrants:
        s += f"""\n\n## 1650-AEST final full-board sweep\n\n- Overall rank: **{oldrank.get(fid, 'new')} -> {rank}**.\n- Current status: **{status}**.\n- Reconciled against the current FPL API and season-long Draft injury/transfer framework.\n- Evidence and reversal triggers: [[{R}]].\n"""
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s)
    changed.append(str(p))

# Build canonical player-note targets and repair shorthand links in mutable/current documents.
player_targets: dict[str, str] = {}
for p in Path("vault/02 Players").glob("*.md"):
    m = re.match(r"(.+) - (\d+)\.md$", p.name)
    if m:
        player_targets[m.group(1)] = str(p.relative_to("vault")).removesuffix(".md")

mutable_link_roots = [Path("vault/02 Players"), Path("vault/03 Teams"), Path("vault/04 Positions")]
mutable_files = [p for root in mutable_link_roots for p in root.glob("*.md")]
mutable_files += [Path("vault/Home.md"), Path("vault/Wiki.md"), Path("vault/01 Current/Current Draft Board.md"), Path("vault/01 Current/Current Watchlist.md")]
for p in mutable_files:
    if not p.exists():
        continue
    text = p.read_text()
    def repair(match):
        raw = match.group(1)
        target = raw.split("|", 1)[0].split("#", 1)[0].strip()
        if not target.startswith("02 Players/"):
            return match.group(0)
        exact = Path("vault") / (target + ".md")
        if exact.exists():
            return match.group(0)
        name = target.split("/", 1)[1]
        resolved = player_targets.get(name)
        if not resolved:
            return match.group(0)
        alias = raw.split("|", 1)[1] if "|" in raw else name
        return f"[[{resolved}|{alias}]]"
    fixed = re.sub(r"\[\[([^\]]+)\]\]", repair, text)
    if fixed != text:
        p.write_text(fixed)
        changed.append(str(p))

# Regenerate position pages.
for code, pathstr in {"FWD": "vault/04 Positions/Forward.md", "MID": "vault/04 Positions/Midfielder.md", "DEF": "vault/04 Positions/Defender.md", "GKP": "vault/04 Positions/Goalkeeper.md"}.items():
    p = Path(pathstr)
    s = p.read_text() if p.exists() else f"---\ntype: position\nposition: {code}\n---\n\n# {code}\n"
    lines = [f"{r[0]}. [[02 Players/{oldname.get(int(r[6]), r[1])} - {r[6]}|{r[1]}]] — {r[3]}; {r[4]} / {r[5]}; {r[7]}" for r in rows if r[2] == code]
    block = "<!-- ranked-players:start -->\n## Players by overall rank\n\n" + "\n".join(lines) + f"\n\nSource: [[01 Current/Current Draft Board]] · generated {TS}\n<!-- ranked-players:end -->"
    if "<!-- ranked-players:start -->" in s:
        s = re.sub(r"<!-- ranked-players:start -->.*?<!-- ranked-players:end -->", block, s, flags=re.S)
    else:
        s += "\n\n" + block + "\n"
    s = re.sub(r"(?m)^last_reviewed: .*", f"last_reviewed: {TS}", s, count=1)
    p.write_text(s)
    changed.append(pathstr)

# Regenerate every team page represented by the board.
for team in sorted({r[3] for r in rows}):
    p = Path(f"vault/03 Teams/{team}.md")
    s = p.read_text() if p.exists() else f"---\ntype: team\nteam: {team}\nlast_reviewed: {TS}\n---\n\n# {team}\n"
    lines = [f"{r[0]}. [[02 Players/{oldname.get(int(r[6]), r[1])} - {r[6]}|{r[1]}]] — {r[2]}; {r[4]} / {r[5]}; {r[7]}" for r in rows if r[3] == team]
    block = "<!-- ranked-players:start -->\n## Ranked players\n\n" + "\n".join(lines) + f"\n\nSource: [[01 Current/Current Draft Board]] · generated {TS}\n<!-- ranked-players:end -->"
    if "<!-- ranked-players:start -->" in s:
        s = re.sub(r"<!-- ranked-players:start -->.*?<!-- ranked-players:end -->", block, s, flags=re.S)
    else:
        s += "\n\n" + block + "\n"
    s = re.sub(r"(?m)^last_reviewed: .*", f"last_reviewed: {TS}", s, count=1)
    p.write_text(s)
    changed.append(str(p))

# Persist roster guardrail in ranking methodology.
skill = Path(".agents/skills/rank-draft-board/SKILL.md")
ss = skill.read_text()
guard = '''
## Draft roster guardrail

For a 20-player squad, maintain at least **2 goalkeepers, 5 defenders, 8 midfielders and 3 forwards**. The final two selections may be any position permitted by the league. During a live draft, once remaining selections equal the number of still-required positional slots, positional need overrides a marginal overall-rank edge.
'''
if "## Draft roster guardrail" not in ss:
    ss = ss.replace("## Core factors", guard + "\n## Core factors")
skill.write_text(ss)
changed.append(str(skill))

# Current watchlist: material transfer and injury triggers.
wp = Path("vault/01 Current/Current Watchlist.md")
ws = wp.read_text()
watch_block = f'''<!-- final-sweep-20260808:start -->
## 8 Aug final-sweep priority watches

- **Cristian Romero** — advanced Atletico negotiations and reported agreed personal terms; large PL-exit risk. {SRC['romero']}
- **Rodri / Rodrigo** — Barcelona negotiations after rejected opening bid, personal terms reported, plus back surgery. {SRC['rodri']}
- **Bruno Guimaraes** — Arsenal/Newcastle fee agreement reported; expected destination remains Premier League, so this is primarily a role/team-change watch. {SRC['bruno']}
- **Nick Pope / Lukas Hornicek** — Hornicek signed and is expected to become Newcastle No.1; Pope likely to leave. {SRC['hornicek']}
- **Trevoh Chalobah** — confirmed sold by Chelsea to Como; removed from active ranked board. {SRC['chelsea_fulham']}
- **Gabriel Jesus / Joshua Zirkzee / Ethan Nwaneri** — current overseas exit-interest reports; ordinary interest remains lower confidence than advanced talks. {SRC['rumours']}
- **Pedro Neto / Savinho / Tijjani Reijnders / Nicolas Jackson** — intra-Premier-League or role-changing transfer watch. {SRC['rumours2']}
- **Xavi Simons / Wilson Odobert / Amadou Onana** — major knee/ACL timelines; substantial Draft-horizon discounts. {PI}
- **Ekitike / De Ligt / Tzimas / Livramento / Lewis Miley / Murillo** — dated return information improves the hold case versus an unknown return date. {PI}
<!-- final-sweep-20260808:end -->'''
if "<!-- final-sweep-20260808:start -->" in ws:
    ws = re.sub(r"<!-- final-sweep-20260808:start -->.*?<!-- final-sweep-20260808:end -->", watch_block, ws, flags=re.S)
else:
    ws += "\n\n" + watch_block + "\n"
wp.write_text(ws)
changed.append(str(wp))

# Full 20-player block audit with five-player buffers.
blocks = []
for start in range(1, 351, 20):
    end = min(350, start + 19)
    lo = max(1, start - 5)
    hi = min(350, end + 5)
    material = []
    for r in rows:
        nr = int(r[0]); fid = int(r[6])
        if start <= nr <= end and (fid in entrants or oldrank.get(fid) != nr or fid in overrides):
            material.append(r[1])
    blocks.append((start, end, lo, hi, material))

top160 = Counter(r[2] for r in rows if int(r[0]) <= 160)
assert top160["GKP"] >= 2 and top160["DEF"] >= 5 and top160["FWD"] >= 3 and top160["MID"] >= 8

entrant_lines = []
for fid in sorted(entrants, key=lambda x: newrank[x]):
    x = byid[fid]
    entrant_lines.append(f"- **{x['web_name']}** ({posmap[x['element_type']]}, {teams[x['team']]}) entered at **{newrank[fid]}**; FPL ID {fid}.")
removal_lines = []
for fid in removals:
    reason = "confirmed Chelsea-to-Como transfer" if fid == 143 else "fell below the 350-player buffer after new-player insertion"
    removal_lines.append(f"- **{oldname[fid]}** (old rank {oldrank[fid]}) — {reason}.")
moves = sorted([(fid, oldrank[fid], newrank[fid]) for fid in oldrank.keys() & newrank.keys() if oldrank[fid] != newrank[fid]], key=lambda z: abs(z[2] - z[1]), reverse=True)
move_lines = [f"- **{oldname[fid]}:** {old} -> {new}" for fid, old, new in moves[:80]]
blocklines = ["| Block | Buffer checked | Material names |", "|---|---|---|"] + [f"| {a}–{b} | {lo}–{hi} | {', '.join(names) if names else 'No material movement'} |" for a, b, lo, hi, names in blocks]

rp = Path("vault") / f"{R}.md"
rp.parent.mkdir(parents=True, exist_ok=True)
rp.write_text(f'''---
type: review
reviewed_at: {TS}
scope: final full-board 1-350 sweep
block_size: 20
buffer: 5
---

# Final full-board FPL Draft sweep — 8 August 2026

## Changes since prior iteration

All 350 ranks were rechecked in 20-player blocks with five-player boundary challengers. The current FPL player pool, transfer/exit risk, injury evidence beyond FPL metadata, newly registered players, roster coverage and current Obsidian links were reconciled.

## Sources searched

- Official FPL player pool: {BOOT}
- Official FPL fixtures: {FIX}
- Premier Injuries: {PI}
- Bruno Guimaraes agreement: {SRC['bruno']}
- Romero Atletico talks: {SRC['romero']}
- Rodri Barcelona talks: {SRC['rodri']}
- Newcastle Hornicek/Pope context: {SRC['hornicek']}
- Chelsea/Fulham transfer roundup: {SRC['chelsea_fulham']}
- Current transfer-rumour sweeps: {SRC['rumours']}; {SRC['rumours2']}; {SRC['rumours_gakpo']}
- Ipswich/Maeda context: {SRC['maeda']}
- Coventry/Rushworth confirmation: {SRC['rushworth']}
- Tottenham injury update: {SRC['spursinj']}

## API reconciliation

The current FPL API contains **{len(elems)}** players. All retained board IDs are present in the API. The prior board had no API-missing IDs but omitted many newly registered players; those players were screened rather than blindly imported. Trevoh Chalobah was removed because his Como transfer is confirmed even though the FPL pool may lag the real-world move.

## New entrants accepted

{chr(10).join(entrant_lines)}

## Removals

{chr(10).join(removal_lines)}

## Injury findings beyond the old FPL labels

- **Xavi Simons:** ACL rehabilitation with a 20 Feb 2027 potential return — severe season-value hit.
- **Amadou Onana:** ACL rupture — substantial downgrade.
- **Wilson Odobert:** ACL recovery with a late-November potential return — long but holdable, still well below healthy peers.
- **Ekitike:** dated 12 Oct potential return is materially better than an indefinite label, so season-long value improves despite surgery/rehab risk.
- **De Ligt:** 6 Sep potential return after back surgery converts an indefinite absence into a medium-term one.
- **Tzimas, Livramento, Lewis Miley and Murillo:** dated August/September targets reduce uncertainty and therefore reduce their injury penalties.
- **Kudus:** Tottenham's manager described him as very close to returning to training, supporting only a small season-long penalty.

## Transfer findings adopted

- **Trevoh Chalobah:** confirmed Como sale -> removed.
- **Cristian Romero:** advanced Atletico negotiations and preferred exit -> major PL-exit discount.
- **Rodri:** Barcelona negotiations/personal terms plus back surgery -> heavy risk discount.
- **Nick Pope:** Hornicek expected to become Newcastle first choice and Pope likely to leave -> major downgrade; Hornicek added.
- **Bruno Guimaraes:** Arsenal fee agreement is a team/role-change watch, not a Premier-League-exit risk -> no punitive season-value downgrade.
- **Gabriel Jesus and Zirkzee:** credible overseas interest recorded, but not treated as completed transfers.
- **Gakpo:** Spurs interest retained as a watch only because Liverpool reportedly have no intention to sell without an exceptional offer.

## Evidence rejected / kept low weight

- Ordinary transfer interest without agreement did not trigger large moves when the likely destination remained in the Premier League.
- Price and ownership were used only to identify new API candidates worth manual attention; they did not determine rank.
- Raw preseason goals or assists without first-team role evidence were not decisive.

## 20-player blocks and five-player buffers

{chr(10).join(blocklines)}

## Largest movements

{chr(10).join(move_lines)}

## Roster coverage guardrail

Top-160 positional availability after the sweep: **{top160['GKP']} GKP, {top160['DEF']} DEF, {top160['MID']} MID, {top160['FWD']} FWD**. This supports the required final squad minimum of **2 GKP / 5 DEF / 8 MID / 3 FWD**; the final two roster slots are flexible.

## Major uncertainties / reversal triggers

- Completion or collapse of Romero, Rodri, Bruno Guimaraes, Gabriel Jesus and Zirkzee moves.
- Newcastle explicitly naming Hornicek or Pope as No.1, or Pope completing a transfer.
- New medical timelines for Saliba, Tielemans and other no-return-date cases.
- New FPL registrations between this sweep and draft day.
''')
changed.append(str(rp))

cp = Path("vault") / f"{C}.md"
cp.parent.mkdir(parents=True, exist_ok=True)
cp.write_text(f'''---
type: changes
changed_at: {TS}
scope: final full-board 1-350 sweep
---

# Final sweep changes

## Entrants
{chr(10).join(entrant_lines)}

## Removals
{chr(10).join(removal_lines)}

## Material rank changes
{chr(10).join(move_lines)}

## Transfer-status changes
- Chalobah: confirmed out of the Premier League; removed.
- Romero: advanced Atletico exit risk materially increased.
- Rodri: Barcelona talks/personal terms materially increased exit risk.
- Pope: Hornicek first-choice expectation materially reduced value.
- Bruno Guimaraes: Arsenal agreement recorded without a Premier-League-exit discount.
- Gabriel Jesus and Zirkzee: credible overseas interest recorded as watch risk.

## Injury-status changes
- Xavi Simons and Onana: ACL context converts generic uncertainty into severe long-horizon discounts.
- Ekitike and De Ligt: dated return evidence reduces uncertainty and improves rank.
- Tzimas, Livramento, Lewis Miley and Murillo: dated return windows reduce the penalty versus unknown return dates.

## Important no-change decisions
- Gakpo remains high: Spurs interest exists, but Liverpool reluctance makes an exit insufficiently likely to override role/ceiling.
- Neto/Reijnders intra-league gossip did not justify large moves.
- Kudus retains high value because the manager described a near return.
''')
changed.append(str(cp))

# Latest-run navigation.
for f in ["vault/Home.md", "vault/Wiki.md"]:
    p = Path(f)
    s = p.read_text()
    marker = f'''<!-- latest-final-sweep:start -->
## Latest final sweep

- [[{R}|8 Aug 2026 final full-board review]]
- [[{C}|8 Aug 2026 changes]]
- Canonical board: [[01 Current/Current Draft Board]]
- Current watchlist: [[01 Current/Current Watchlist]]
<!-- latest-final-sweep:end -->'''
    if "<!-- latest-final-sweep:start -->" in s:
        s = re.sub(r"<!-- latest-final-sweep:start -->.*?<!-- latest-final-sweep:end -->", marker, s, flags=re.S)
    else:
        s += "\n\n" + marker + "\n"
    p.write_text(s)
    changed.append(f)

# Second link-normalisation pass now that all current pages have been regenerated.
for p in mutable_files:
    if not p.exists():
        continue
    text = p.read_text()
    def repair2(match):
        raw = match.group(1)
        target = raw.split("|", 1)[0].split("#", 1)[0].strip()
        if not target.startswith("02 Players/"):
            return match.group(0)
        exact = Path("vault") / (target + ".md")
        if exact.exists():
            return match.group(0)
        name = target.split("/", 1)[1]
        resolved = player_targets.get(name)
        if not resolved:
            return match.group(0)
        alias = raw.split("|", 1)[1] if "|" in raw else name
        return f"[[{resolved}|{alias}]]"
    fixed = re.sub(r"\[\[([^\]]+)\]\]", repair2, text)
    if fixed != text:
        p.write_text(fixed)
        changed.append(str(p))

# Audit links in every mutable/current document, without mutating immutable historical reviews.
broken = []
checked = 0
for p in mutable_files:
    if not p.exists():
        continue
    text = p.read_text(errors="ignore")
    for raw in re.findall(r"\[\[([^\]]+)\]\]", text):
        target = raw.split("|", 1)[0].split("#", 1)[0].strip()
        if "/" not in target:
            continue
        checked += 1
        q = Path("vault") / (target + ".md" if not target.endswith(".md") else target)
        if not q.exists():
            broken.append((str(p), target))
if broken:
    raise SystemExit("Broken current/mutable wikilinks: " + repr(broken[:30]))
with rp.open("a") as fh:
    fh.write(f"\n## Link audit result\n\nChecked **{checked}** structured wikilinks across current/player/team/position navigation documents; **0 broken links remain**. Immutable historical review/change records were not rewritten.\n")

# Temporary discovery files are not canonical deliverables.
for f in ["vault/00 Meta/Final Sweep API Reconciliation.md", "vault/00 Meta/Final Sweep New Candidate Shortlist.md"]:
    p = Path(f)
    if p.exists():
        p.unlink()

# Changelog every changed Markdown file once.
changed = list(dict.fromkeys(changed))
log = Path("vault/00 Meta/Document Changelog.md")
ls = log.read_text()
ev = "; ".join([BOOT, FIX, PI, SRC["bruno"], SRC["romero"], SRC["rodri"], SRC["hornicek"], SRC["chelsea_fulham"], f"[[{R}]]", f"[[{C}]]"])
for f in changed + ["vault/00 Meta/Document Changelog.md"]:
    action = "created" if f in created_notes or f in [str(rp), str(cp)] else "updated"
    ls += f"\n| {TS} | `{f}` | {action} | Final 1–350 sweep in 20-player blocks with five-player buffers; API, transfers, injuries, roster guardrail and links reconciled | [[{R}]] | {ev} |"
log.write_text(ls + "\n")

# Final invariants.
finalrows = [
    [x.strip() for x in line.strip().strip("|").split("|")]
    for line in boardp.read_text().splitlines()
    if re.match(r"^\| \d+ \|", line)
]
assert [int(r[0]) for r in finalrows] == list(range(1, 351))
assert len({int(r[6]) for r in finalrows}) == 350
assert all(int(r[6]) in byid for r in finalrows)
assert fixtures
print("Final sweep complete")
print("Top160:", dict(top160))
print("Entrants:", len(entrants), "Removals:", len(removals), "Link checks:", checked)
