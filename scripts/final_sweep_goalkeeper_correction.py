from __future__ import annotations

import json
import re
from pathlib import Path

TS = "2026-08-08T17:12:00+10:00"
R = "06 Reviews/2026/08/2026-08-08/1650-AEST-review"
C = "07 Changes/2026/08/2026-08-08/1650-AEST-changes"
SOURCE = "https://www.brentfordfc.com/en/news/article/first-team-brentford-sign-caoimhin-kelleher-liverpool; https://www.premierleague.com/en/news/4680049/team-news-glasners-first-xi-confirmed; https://www.fulhamfc.com/players/bernd-leno/; https://www.sunderlandafc.news/club/first-team-squad/"

api = json.loads(Path("/tmp/bootstrap.json").read_text())
byid = {int(x["id"]): x for x in api["elements"]}
teams = {x["id"]: x["short_name"] for x in api["teams"]}
posmap = {1: "GKP", 2: "DEF", 3: "MID", 4: "FWD"}

boardp = Path("vault/01 Current/Current Draft Board.md")
txt = boardp.read_text()
rows = [[x.strip() for x in line.strip().strip("|").split("|")] for line in txt.splitlines() if re.match(r"^\| \d+ \|", line)]
assert len(rows) == 350
old = {int(r[6]): int(r[0]) for r in rows}
name_by_id = {int(r[6]): r[1] for r in rows}

# Starting/likely-starting keepers should not be displaced by speculative reserve outfielders.
add_anchors = {
    82: 218,   # Kelleher, Brentford established starter
    412: 230,  # Lammens, Man Utd first-choice pathway
    467: 252,  # Sels, Forest established starter
    109: 254,  # Verbruggen, Brighton incumbent
    250: 258,  # Leno, Fulham established starter
    529: 264,  # Roefs, Sunderland first choice
    28: 270,   # Martinez, Villa starter but transfer uncertainty
}
remove_ids = {362, 92, 561, 255, 119, 93, 396}  # reserve/speculative outfield tail
rows = [r for r in rows if int(r[6]) not in remove_ids]
existing = {int(r[6]) for r in rows}
for fid, anchor in add_anchors.items():
    if fid in existing:
        continue
    x = byid[fid]
    news = (x.get("news") or "").strip()
    status = "Available" if x["status"] == "a" else (news or {"d": "Doubtful", "i": "Injured", "s": "Suspended", "u": "Unavailable"}.get(x["status"], "Unavailable"))
    rows.append(["0", x["web_name"], posmap[x["element_type"]], teams[x["team"]], "Extended watch buffer", "Watch", str(fid), status, TS, f"[[{R}]]"])

def key(r):
    fid = int(r[6])
    return (add_anchors.get(fid, old.get(fid, 999)), old.get(fid, 1000), fid)
rows = sorted(rows, key=key)
assert len(rows) == 350

def segtier(rank):
    if rank <= 8: return "Franchise", "S" if rank <= 2 else "A+"
    if rank <= 32: return "Foundation", "A" if rank <= 16 else "B+"
    if rank <= 80: return "Core", "B" if rank <= 48 else ("B-" if rank <= 65 else "C+")
    if rank <= 128: return "Depth", "C"
    if rank <= 160: return "Endgame", "D+"
    if rank <= 220: return "Undrafted buffer", "D"
    return "Extended watch buffer", "Watch"
for rank, r in enumerate(rows, 1):
    r[0] = str(rank)
    r[4], r[5] = segtier(rank)
    fid = int(r[6])
    if old.get(fid) != rank or fid in add_anchors:
        r[8] = TS
        r[9] = f"[[{R}]]"

header = txt.split("| Pick order | Player | Position | Team | Segment | Tier | FPL ID | Status | Last changed | Evidence |")[0]
body = "| Pick order | Player | Position | Team | Segment | Tier | FPL ID | Status | Last changed | Evidence |\n|---:|---|---|---|---|---|---:|---|---|---|\n" + "\n".join("| " + " | ".join(r) + " |" for r in rows)
cautions = txt.split("## Method cautions", 1)[1]
boardp.write_text(header + body + "\n## Method cautions" + cautions)

newrank = {int(r[6]): int(r[0]) for r in rows}
current = set(newrank)
changed = [str(boardp)]

# Synchronise ranked notes, and explicitly mark every player note outside the current 350 as unranked.
for p in Path("vault/02 Players").glob("*.md"):
    m = re.search(r" - (\d+)\.md$", p.name)
    if not m:
        continue
    fid = int(m.group(1))
    s = p.read_text()
    if fid in current:
        rank = newrank[fid]
        x = byid.get(fid)
        s = re.sub(r"(?m)^(current_rank: ).*", rf"\g<1>{rank}", s, count=1)
        if x:
            s = re.sub(r"(?m)^(team: ).*", rf"\g<1>{teams[x['team']]}", s, count=1)
            s = re.sub(r"(?m)^(position: ).*", rf"\g<1>{posmap[x['element_type']]}", s, count=1)
        if fid in add_anchors:
            s += f"\n\n## 1712-AEST goalkeeper-tail correction\n\n- Re-entered the active top 350 at **{rank}** after the final sweep incorrectly let new registrations mechanically displace established/probable starting goalkeepers.\n- Starting-role and two-goalkeeper Draft roster utility outweigh the speculative reserve outfield tail.\n- Evidence: [[{R}]].\n"
    else:
        s = re.sub(r"(?m)^(current_rank: ).*", "current_rank: null", s, count=1)
        if fid in remove_ids:
            s += f"\n\n## 1712-AEST final-tail correction\n\n- Removed from the active top 350 after direct comparison with probable starting goalkeepers.\n- Remains a watchlist/deep-pool player rather than a current ranked selection.\n- Evidence: [[{R}]].\n"
    if fid in add_anchors or fid in remove_ids or (fid not in current and re.search(r"(?m)^last_reviewed:", s)):
        s = re.sub(r"(?m)^(last_reviewed: ).*", rf"\g<1>{TS}", s, count=1)
    p.write_text(s)
    if fid in add_anchors or fid in remove_ids or fid not in current:
        changed.append(str(p))

# Regenerate position pages.
for code, pathstr in {"FWD":"vault/04 Positions/Forward.md","MID":"vault/04 Positions/Midfielder.md","DEF":"vault/04 Positions/Defender.md","GKP":"vault/04 Positions/Goalkeeper.md"}.items():
    p = Path(pathstr); s = p.read_text()
    lines = [f"{r[0]}. [[02 Players/{name_by_id.get(int(r[6]), r[1])} - {r[6]}|{r[1]}]] — {r[3]}; {r[4]} / {r[5]}; {r[7]}" for r in rows if r[2] == code]
    block = "<!-- ranked-players:start -->\n## Players by overall rank\n\n" + "\n".join(lines) + f"\n\nSource: [[01 Current/Current Draft Board]] · generated {TS}\n<!-- ranked-players:end -->"
    s = re.sub(r"<!-- ranked-players:start -->.*?<!-- ranked-players:end -->", block, s, flags=re.S)
    s = re.sub(r"(?m)^last_reviewed: .*", f"last_reviewed: {TS}", s, count=1)
    p.write_text(s); changed.append(pathstr)

# Regenerate team pages that have ranked players.
for team in sorted({r[3] for r in rows}):
    p = Path(f"vault/03 Teams/{team}.md")
    if not p.exists():
        continue
    s = p.read_text()
    lines = [f"{r[0]}. [[02 Players/{name_by_id.get(int(r[6]), r[1])} - {r[6]}|{r[1]}]] — {r[2]}; {r[4]} / {r[5]}; {r[7]}" for r in rows if r[3] == team]
    block = "<!-- ranked-players:start -->\n## Ranked players\n\n" + "\n".join(lines) + f"\n\nSource: [[01 Current/Current Draft Board]] · generated {TS}\n<!-- ranked-players:end -->"
    s = re.sub(r"<!-- ranked-players:start -->.*?<!-- ranked-players:end -->", block, s, flags=re.S)
    s = re.sub(r"(?m)^last_reviewed: .*", f"last_reviewed: {TS}", s, count=1)
    p.write_text(s); changed.append(str(p))

# Amend the in-run immutable records before publication.
rp = Path("vault") / f"{R}.md"
review = rp.read_text() + f'''\n\n## 17:12 AEST goalkeeper-tail quality correction\n\nA post-generation sanity check found that mass insertion of new registrations had pushed established/probable starting goalkeepers out of the 350 while leaving speculative reserve outfielders at the tail. That was rejected as a mechanical artefact rather than a valid Draft comparison.\n\nRe-entered: **Kelleher ({newrank[82]}), Lammens ({newrank[412]}), Sels ({newrank[467]}), Verbruggen ({newrank[109]}), Leno ({newrank[250]}), Roefs ({newrank[529]}), Martinez ({newrank[28]})**. Kelleher is Brentford's established replacement for Flekken; Sels started Forest's preseason opener; Leno remains Fulham's senior goalkeeper; Roefs is Sunderland's established first choice; current reporting also supports Lammens as Manchester United's lead goalkeeper.\n\nRemoved instead from the ranked tail: **Jacquet, Ji-soo, Anselmino, J.Cuenca, Costinha, Schuster and Vitor Reis**. Their uncertain/reserve minutes do not beat the season-long floor of a starting goalkeeper when every Draft manager needs two.\n\nSources: {SOURCE}\n'''
rp.write_text(review); changed.append(str(rp))
cp = Path("vault") / f"{C}.md"
changes = cp.read_text() + f'''\n\n## Goalkeeper-tail correction\n\n- Kelleher: outside 350 -> **{newrank[82]}**\n- Lammens: outside 350 -> **{newrank[412]}**\n- Sels: outside 350 -> **{newrank[467]}**\n- Verbruggen: outside 350 -> **{newrank[109]}**\n- Leno: outside 350 -> **{newrank[250]}**\n- Roefs: outside 350 -> **{newrank[529]}**\n- Martinez (GKP): outside 350 -> **{newrank[28]}**\n- Jacquet, Ji-soo, Anselmino, J.Cuenca, Costinha, Schuster and Vitor Reis moved outside the active 350.\n\nReason: starting-goalkeeper season floor and mandatory two-GK roster utility beat speculative reserve outfield minutes.\n'''
cp.write_text(changes); changed.append(str(cp))

# Changelog the correction files.
log = Path("vault/00 Meta/Document Changelog.md")
ls = log.read_text()
for f in list(dict.fromkeys(changed)) + [str(log)]:
    ls += f"\n| {TS} | `{f}` | corrected | Final-sweep goalkeeper-tail sanity correction and current-rank synchronization | [[{R}]] | {SOURCE}; [[{R}]]; [[{C}]] |"
log.write_text(ls + "\n")

# Validate current mutable links exactly.
broken = []
for p in [*Path("vault/02 Players").glob("*.md"), *Path("vault/03 Teams").glob("*.md"), *Path("vault/04 Positions").glob("*.md"), Path("vault/Home.md"), Path("vault/Wiki.md"), boardp, Path("vault/01 Current/Current Watchlist.md")]:
    if not p.exists(): continue
    for raw in re.findall(r"\[\[([^\]]+)\]\]", p.read_text(errors="ignore")):
        target = raw.split("|",1)[0].split("#",1)[0].strip()
        if "/" not in target: continue
        q = Path("vault") / (target + ".md" if not target.endswith(".md") else target)
        if not q.exists(): broken.append((str(p), target))
assert not broken, broken[:20]
finalrows = [[x.strip() for x in line.strip().strip("|").split("|")] for line in boardp.read_text().splitlines() if re.match(r"^\| \d+ \|", line)]
assert len(finalrows) == 350 and [int(r[0]) for r in finalrows] == list(range(1,351))
assert len({int(r[6]) for r in finalrows}) == 350
print("Goalkeeper-tail correction complete")
print([(r[0], r[1]) for r in finalrows if r[2] == "GKP"])
