from pathlib import Path
import json
import re
import urllib.request

TS = "2026-08-03T22:56:00+10:00"
STAMP = "2256-AEST"
REVIEW = "[[06 Reviews/2026/08/2026-08-03/2256-AEST-review]]"
CHANGES = "[[07 Changes/2026/08/2026-08-03/2256-AEST-changes]]"
API = "https://fantasy.premierleague.com/api/bootstrap-static/"
FIXTURES = "https://fantasy.premierleague.com/api/fixtures/"
root = Path("vault")
board = root / "01 Current/Current Draft Board.md"
text = board.read_text()
row_re = re.compile(r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|$", re.M)
rows = []
for m in row_re.finditer(text):
    rows.append({
        "rank": int(m.group(1)), "player": m.group(2).strip(), "position": m.group(3).strip(),
        "team": m.group(4).strip(), "segment": m.group(5).strip(), "tier": m.group(6).strip(),
        "id": int(m.group(7)), "status": m.group(8).strip(), "changed": m.group(9).strip(),
        "evidence": m.group(10).strip(),
    })
assert len(rows) == 350, len(rows)
mids = [r for r in rows if r["position"] == "MID"]
reviewed = mids[25:65]
old_order = [r["player"] for r in reviewed]
new_order = [
    "E.Le Fée", "Enzo", "Maddison", "Sarr", "Minteh",
    "Kudus", "Martinelli", "Neto", "Barnes", "Amad",
    "McNeil", "Mitoma", "Dorgu", "Iwobi", "Wilson",
    "J.Murphy", "Smith Rowe", "Rayan", "Stach", "Xhaka",
    "Okafor", "Groß", "Reijnders", "Anderson", "Jensen",
    "McGinn", "Aaronson", "Garner", "Gravenberch", "Scott",
    "Zubimendi", "Ampadu", "Caicedo", "Hutchinson", "Yeremy",
    "Ayari", "Hinshelwood", "Sadiki", "Berge", "Tonali",
]
assert len(new_order) == 40
assert set(old_order) == set(new_order), (old_order, set(new_order) - set(old_order), set(old_order) - set(new_order))

with urllib.request.urlopen(API, timeout=30) as response:
    bootstrap = json.load(response)
with urllib.request.urlopen(FIXTURES, timeout=30) as response:
    fixtures = json.load(response)
api_by_id = {int(p["id"]): p for p in bootstrap["elements"]}
for p in reviewed:
    assert p["id"] in api_by_id, p
    assert int(api_by_id[p["id"]]["element_type"]) == 3, (p, api_by_id[p["id"]])

by = {r["player"]: r.copy() for r in reviewed}
slots = sorted(reviewed, key=lambda x: x["rank"])
replacement = {}
moves = []
for slot, name in zip(slots, new_order):
    p = by[name].copy()
    old = p["rank"]
    p["rank"] = slot["rank"]
    p["segment"] = slot["segment"]
    p["tier"] = slot["tier"]
    p["changed"] = TS
    p["evidence"] = REVIEW
    replacement[slot["rank"]] = p
    if old != p["rank"]:
        moves.append((name, old, p["rank"]))

out = []
for line in text.splitlines():
    m = row_re.match(line)
    if m and int(m.group(1)) in replacement:
        p = replacement[int(m.group(1))]
        out.append(f"| {p['rank']} | {p['player']} | MID | {p['team']} | {p['segment']} | {p['tier']} | {p['id']} | {p['status']} | {TS} | {REVIEW} |")
    else:
        out.append(line)
newtext = "\n".join(out) + "\n"
newtext = re.sub(r"(?m)^last_updated: .*?$", f"last_updated: {TS}", newtext)
newtext = re.sub(r"(?m)^status: .*?$", "status: midfield_position_block_2_reviewed", newtext)
board.write_text(newtext)

for p in replacement.values():
    paths = list((root / "02 Players").glob(f"* - {p['id']}.md"))
    assert len(paths) == 1, (p, paths)
    path = paths[0]
    s = path.read_text()
    s = re.sub(r"(?m)^current_rank: .*?$", f"current_rank: {p['rank']}", s)
    s = re.sub(r"(?m)^segment: .*?$", f"segment: {p['segment']}", s)
    s = re.sub(r"(?m)^tier: .*?$", f"tier: {p['tier']}", s)
    s = re.sub(r"(?m)^last_reviewed: .*?$", f"last_reviewed: {TS}", s)
    pos = new_order.index(p["player"]) + 26
    old = by[p["player"]]["rank"]
    note = (
        f"\n\n## {STAMP} midfield positional comparison\n\n"
        f"- Midfield order: **{pos}** after reviewing positional ranks 31–60 with challengers 26–30 and 61–65.\n"
        f"- Overall rank: **{old} → {p['rank']}**.\n"
        f"- Comparator: raw expected season FPL points first, then minutes, role, penalties/set pieces, injury and rotation risk, floor and ceiling.\n"
        f"- Evidence and reversal triggers: {REVIEW}.\n"
    )
    path.write_text(s.rstrip() + note + "\n")

updated = board.read_text()
rows2 = []
for m in row_re.finditer(updated):
    rows2.append({
        "rank": int(m.group(1)), "player": m.group(2).strip(), "position": m.group(3).strip(),
        "team": m.group(4).strip(), "segment": m.group(5).strip(), "tier": m.group(6).strip(),
        "id": int(m.group(7)), "status": m.group(8).strip(),
    })
pos_path = root / "04 Positions/Midfielder.md"
pt = pos_path.read_text()
start = pt.index("<!-- ranked-players:start -->")
end = pt.index("<!-- ranked-players:end -->") + len("<!-- ranked-players:end -->")
section = ["<!-- ranked-players:start -->", "## Players by overall rank", "", "Players are listed in canonical overall draft rank order.", ""]
for r in [x for x in rows2 if x["position"] == "MID"]:
    paths = list((root / "02 Players").glob(f"* - {r['id']}.md"))
    assert len(paths) == 1
    section.append(f"{r['rank']}. [[02 Players/{paths[0].stem}|{r['player']}]] — MID, {r['team']}; {r['segment']} / {r['tier']}; {r['status']}")
section += ["", f"Source: [[01 Current/Current Draft Board]] · generated {TS}", "<!-- ranked-players:end -->"]
pt = pt[:start] + "\n".join(section) + pt[end:]
pt = re.sub(r"(?m)^last_reviewed: .*?$", f"last_reviewed: {TS}", pt)
pt += f"\n\n## {STAMP} block 2 review\n\n- Midfield ranks 31–60 were insertion-sorted with challengers 26–30 and 61–65.\n- Review: {REVIEW}.\n- Changes: {CHANGES}.\n"
pos_path.write_text(pt)

comparisons = [
    ("E.Le Fée", "Enzo", "E.Le Fée", "More advanced role and stronger set-piece route."),
    ("Enzo", "Maddison", "Enzo", "Safer current availability and minutes; Maddison has the higher creative ceiling."),
    ("Maddison", "Sarr", "Maddison", "Set pieces and proven chance creation."),
    ("Sarr", "Minteh", "Sarr", "More established output and role security."),
    ("Minteh", "Kudus", "Minteh", "Current fitness and minutes outlook; a fully fit Kudus can reverse it."),
    ("Kudus", "Martinelli", "Kudus", "Broader attacking role when fit; Martinelli has stronger team context."),
    ("Martinelli", "Neto", "Martinelli", "Higher direct scoring ceiling in an elite attack."),
    ("Neto", "Barnes", "Neto", "Broader creative involvement and slightly safer role."),
    ("Barnes", "Amad", "Barnes", "Higher proven goal-scoring ceiling."),
    ("Amad", "McNeil", "Amad", "More dynamic attacking involvement."),
    ("McNeil", "Mitoma", "McNeil", "Set pieces and current availability outweigh Mitoma's injury uncertainty."),
    ("Mitoma", "Dorgu", "Mitoma", "Higher attacking ceiling if fit; Dorgu has the safer availability floor."),
    ("Dorgu", "Iwobi", "Dorgu", "More advanced deployment and direct return potential."),
    ("Iwobi", "Wilson", "Iwobi", "Safer minutes and established Premier League production."),
    ("Wilson", "J.Murphy", "Wilson", "Set-piece and attacking role narrowly win."),
    ("J.Murphy", "Smith Rowe", "J.Murphy", "Stronger recent direct-return route."),
    ("Smith Rowe", "Rayan", "Smith Rowe", "Higher proven creative ceiling."),
    ("Rayan", "Stach", "Rayan", "More direct attacking role."),
    ("Stach", "Xhaka", "Stach", "Slightly better expected attacking involvement; Xhaka has the safer floor."),
    ("Xhaka", "Okafor", "Xhaka", "Secure minutes and set pieces narrowly beat role uncertainty."),
    ("Okafor", "Groß", "Okafor", "Higher scoring ceiling despite weaker minutes certainty."),
    ("Groß", "Reijnders", "Groß", "Set pieces and proven accumulation floor."),
    ("Reijnders", "Anderson", "Reijnders", "More direct attacking responsibility."),
    ("Anderson", "Jensen", "Anderson", "Stronger minutes outlook and two-way accumulation floor."),
    ("Jensen", "McGinn", "Jensen", "Set-piece access and chance creation."),
    ("McGinn", "Aaronson", "McGinn", "Safer minutes and broader contribution floor."),
    ("Aaronson", "Garner", "Aaronson", "More advanced attacking position."),
    ("Garner", "Gravenberch", "Garner", "Set pieces and direct chance creation."),
    ("Gravenberch", "Scott", "Gravenberch", "Safer elite-team minutes floor."),
    ("Scott", "Zubimendi", "Scott", "More direct attacking role."),
    ("Zubimendi", "Ampadu", "Zubimendi", "Stronger team context and distribution floor."),
    ("Ampadu", "Caicedo", "Ampadu", "Slightly broader accumulation and set-piece route."),
    ("Caicedo", "Hutchinson", "Caicedo", "Minutes security beats Hutchinson's uncertain attacking role."),
    ("Hutchinson", "Yeremy", "Hutchinson", "More credible direct-return ceiling."),
    ("Yeremy", "Ayari", "Yeremy", "More advanced attacking pathway."),
    ("Ayari", "Hinshelwood", "Ayari", "Slightly stronger creative upside."),
    ("Hinshelwood", "Sadiki", "Hinshelwood", "More direct box-arrival route."),
    ("Sadiki", "Berge", "Sadiki", "Higher transition and accumulation upside."),
    ("Berge", "Tonali", "Berge", "Safer minutes floor in the current evidence set."),
]
review_path = root / "06 Reviews/2026/08/2026-08-03/2256-AEST-review.md"
review_path.parent.mkdir(parents=True, exist_ok=True)
rl = [
    "---", "type: review", f"reviewed_at: {TS}", "position: MID", "block: 31-60",
    "challengers: 26-30,61-65", "---", "", "# Midfield positional review — block 2", "",
    "## Scope", "",
    "Insertion-sorted midfield positional ranks 31–60 and tested five challengers on each side. Every non-midfielder retained its global slot.",
    "", "## API reconciliation", "",
    f"- Official player identity, team, position and availability authority: {API}",
    f"- Official fixture endpoint checked: {FIXTURES}",
    f"- Reconciled {len(reviewed)} reviewed midfielders against the current API pool and {len(fixtures)} fixture records.",
    "- Stable FPL IDs were preserved; no reviewed player was absent from the API pool or classified outside midfield.",
    "", "## Sources searched and evidence use", "",
    "- Canonical baseline: [[01 Current/Current Draft Board]].",
    "- Latest team reviews and the prior midfield block supplied role, set-piece, injury and competition context.",
    "- No new external report was strong enough to override the existing canonical evidence in this bounded positional pass.",
    "- No inaccessible source was adopted. Price, ownership and value-for-money were excluded.",
    "", "## Comparator", "",
    "Raw expected season FPL points were assessed first, followed by minutes, role, penalties and set pieces, injury and rotation risk, floor and ceiling.",
    "", "## Decisive comparisons",
]
for a, b, winner, why in comparisons:
    rl.append(f"- **{a} vs {b}: {winner} first.** {why}")
rl += ["", "## Final positional order for reviewed set", ""]
for i, name in enumerate(new_order, 26):
    p = next(v for v in replacement.values() if v["player"] == name)
    rl.append(f"{i}. {name} — overall {p['rank']}")
rl += [
    "", "## Evidence adopted", "",
    "- Official API identity, position and availability metadata.",
    "- Existing immutable team-review conclusions where still consistent with current API metadata.",
    "", "## Evidence rejected", "",
    "- Reputation without a secure minutes path did not justify promotion.",
    "- Injury-flagged upside cases were not ranked as though fully fit.",
    "- Defensive-midfield real-football importance was not treated as equivalent to FPL attacking value.",
    "", "## Close calls and reversal triggers", "",
    "- Minteh/Kudus reverses with confirmed full fitness and a secure Kudus starting role.",
    "- McNeil/Mitoma reverses when Mitoma has a reliable return date and first-team minutes.",
    "- Martinelli/Neto/Barnes remains role-sensitive and should react to repeated competitive starts.",
    "- Wilson/J.Murphy/Smith Rowe is a low-confidence cluster driven by minutes and set-piece evidence.",
    "- Reijnders and Hutchinson can rise quickly with sustained advanced deployment.",
    "", "## Validation", "",
    "- Reviewed midfield ranks 31–60 plus challengers 26–30 and 61–65.",
    "- Preserved all non-midfielder global slots.",
    "- `scripts/validate_draft_board.py` checks complete ranks 1–350 and unique FPL IDs.",
]
review_path.write_text("\n".join(rl) + "\n")

changes_path = root / "07 Changes/2026/08/2026-08-03/2256-AEST-changes.md"
changes_path.parent.mkdir(parents=True, exist_ok=True)
unchanged = [name for name in new_order if by[name]["rank"] == next(v["rank"] for v in replacement.values() if v["player"] == name)]
cl = [
    "---", "type: changes", f"changed_at: {TS}", "position: MID", "block: 31-60", "---", "",
    "# Midfield block 2 changes", "", "## Rank changes", "",
]
for name, old, new in sorted(moves, key=lambda x: x[2]):
    cl.append(f"- {name}: **{old} → {new}**")
cl += [
    "", "## Important no-change decisions", "",
    f"- Unchanged: {', '.join(unchanged) if unchanged else 'None'}.",
    "- Upper challengers E.Le Fée, Enzo, Maddison, Sarr and Minteh all retained places above the block boundary.",
    "- Lower challengers Ayari, Hinshelwood, Sadiki, Berge and Tonali did not enter the top 60 midfielders.",
    "- No non-midfielder changed global rank.",
    "", "## Injury and role treatment", "",
    "- Mitoma remained discounted for an unknown hamstring return date.",
    "- Kudus remained below the top-30 boundary while carrying a current fitness discount.",
    "- Reijnders and Hutchinson moved only within the reviewed set; neither was promoted on reputation alone.",
    "", "## Next block", "",
    "- Midfield ranks 61–90, challenged by ranks 56–60 and 91–95.",
]
changes_path.write_text("\n".join(cl) + "\n")

for rel in ["Home.md", "Wiki.md", "01 Current/Current Watchlist.md"]:
    path = root / rel
    s = path.read_text().rstrip()
    s += f"\n\n<!-- {STAMP.lower()}-midfield-block-2 -->\n- Midfield ranks 31–60 reviewed with challengers 26–30 and 61–65: {REVIEW} · {CHANGES}.\n"
    path.write_text(s + "\n")

changed = [board, pos_path, review_path, changes_path, root / "Home.md", root / "Wiki.md", root / "01 Current/Current Watchlist.md"]
changed += [next((root / "02 Players").glob(f"* - {p['id']}.md")) for p in replacement.values()]
log = root / "00 Meta/Document Changelog.md"
ls = log.read_text().rstrip() + "\n"
for path in changed + [log]:
    action = "created" if path in [review_path, changes_path] else "updated"
    ls += f"| {TS} | `{path.as_posix()}` | {action} | Midfield positional ranks 31–60 with challengers 26–30 and 61–65 | {REVIEW} | {API}; {FIXTURES}; {REVIEW}; {CHANGES} |\n"
log.write_text(ls)
