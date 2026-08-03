from pathlib import Path
import re

TS = "2026-08-03T16:48:00+10:00"
STAMP = "1648-AEST"
REVIEW_LINK = "[[06 Reviews/2026/08/2026-08-03/1648-AEST-review]]"
CHANGE_LINK = "[[07 Changes/2026/08/2026-08-03/1648-AEST-changes]]"
API = "https://fantasy.premierleague.com/api/bootstrap-static/"
root = Path("vault")
board_path = root / "01 Current/Current Draft Board.md"
text = board_path.read_text()

row_re = re.compile(r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|$", re.M)
rows=[]
for m in row_re.finditer(text):
    rows.append({"rank":int(m.group(1)),"player":m.group(2).strip(),"position":m.group(3).strip(),"team":m.group(4).strip(),"segment":m.group(5).strip(),"tier":m.group(6).strip(),"id":int(m.group(7)),"status":m.group(8).strip(),"changed":m.group(9).strip(),"evidence":m.group(10).strip(),"span":m.span()})
assert len(rows)==350, len(rows)
forwards=[r for r in rows if r["position"]=="FWD"]
block=forwards[:35]
old_order=[r["player"] for r in block]
new_order=[
"Haaland","Isak","Watkins","Thiago","Gyökeres","João Pedro","Mateta","Solanke","Calvert-Lewin","Marmoush",
"Evanilson","Šeško","Wood","Wissa","Woltemade","Richarlison","Delap","Havertz","Brobbey","Muniz",
"Strand Larsen","Beto","Nketiah","Welbeck","Igor Jesus","Barry","Ekitiké","Osula","Kalimuendo","N.Jackson",
"Emegha","Isidor","Wright","Hirst","Nmecha"]
assert set(old_order)==set(new_order), (old_order, sorted(set(new_order)-set(old_order)), sorted(set(old_order)-set(new_order)))
by_name={r["player"]:r.copy() for r in block}
slots=sorted(block,key=lambda r:r["rank"])
changes=[]
replacement={}
for slot,name in zip(slots,new_order):
    p=by_name[name]
    old=p["rank"]
    p["rank"]=slot["rank"]
    p["segment"]=slot["segment"]
    p["tier"]=slot["tier"]
    p["changed"]=TS
    p["evidence"]=REVIEW_LINK
    replacement[slot["rank"]]=p
    if old!=p["rank"]: changes.append((name,old,p["rank"]))

lines=text.splitlines()
out=[]
for line in lines:
    m=row_re.match(line)
    if m and int(m.group(1)) in replacement:
        p=replacement[int(m.group(1))]
        out.append(f'| {p["rank"]} | {p["player"]} | FWD | {p["team"]} | {p["segment"]} | {p["tier"]} | {p["id"]} | {p["status"]} | {TS} | {REVIEW_LINK} |')
    else: out.append(line)
board_path.write_text("\n".join(out)+"\n")

# Update affected player notes by stable FPL ID.
for p in replacement.values():
    matches=list((root/"02 Players").glob(f"* - {p['id']}.md"))
    assert len(matches)==1,(p,matches)
    path=matches[0]
    s=path.read_text()
    s=re.sub(r"(?m)^current_rank: .*?$",f"current_rank: {p['rank']}",s)
    s=re.sub(r"(?m)^segment: .*?$",f"segment: {p['segment']}",s)
    s=re.sub(r"(?m)^tier: .*?$",f"tier: {p['tier']}",s)
    s=re.sub(r"(?m)^last_reviewed: .*?$",f"last_reviewed: {TS}",s)
    pos=new_order.index(p['player'])+1
    old=by_name[p['player']]['rank']
    note=(f"\n\n## {STAMP} forward positional comparison\n\n"
          f"- Forward order: **{pos} of {len(forwards)}** after the first 30-player block with challengers 31–35.\n"
          f"- Overall rank: **{old} → {p['rank']}**.\n"
          f"- Comparator: raw expected FPL points first, then minutes, role, penalties/set pieces, injury/rotation risk, floor and ceiling; forward scarcity was applied only after that comparison.\n"
          f"- Evidence and reversal triggers: {REVIEW_LINK}.\n")
    path.write_text(s.rstrip()+note)

# Rebuild ranked forward section from updated board.
updated=board_path.read_text()
rows2=[]
for m in row_re.finditer(updated):
    rows2.append({"rank":int(m.group(1)),"player":m.group(2).strip(),"position":m.group(3).strip(),"team":m.group(4).strip(),"segment":m.group(5).strip(),"tier":m.group(6).strip(),"id":int(m.group(7)),"status":m.group(8).strip()})
fwd=[r for r in rows2 if r['position']=='FWD']
position_path=root/"04 Positions/Forward.md"
pos_text=position_path.read_text()
start=pos_text.index("<!-- ranked-players:start -->")
end=pos_text.index("<!-- ranked-players:end -->")+len("<!-- ranked-players:end -->")
section=["<!-- ranked-players:start -->","## Players by overall rank","","Players are listed in canonical overall draft rank order.",""]
for r in fwd:
    matches=list((root/"02 Players").glob(f"* - {r['id']}.md")); assert len(matches)==1
    stem=matches[0].stem
    section.append(f"{r['rank']}. [[02 Players/{stem}|{r['player']}]] — FWD, {r['team']}; {r['segment']} / {r['tier']}; {r['status']}")
section += ["",f"Source: [[01 Current/Current Draft Board]] · generated {TS}","<!-- ranked-players:end -->"]
pos_text=pos_text[:start]+"\n".join(section)+pos_text[end:]
pos_text=re.sub(r"(?m)^last_reviewed: .*?$",f"last_reviewed: {TS}",pos_text)
pos_text += f"\n\n## {STAMP} block 1 review\n\n- Positional ranks 1–30 were insertion-sorted with challengers 31–35.\n- Review: {REVIEW_LINK}.\n- Changes: {CHANGE_LINK}.\n"
position_path.write_text(pos_text)

comparisons=[
("Haaland","Isak","Haaland","Higher penalty-backed goal ceiling and the strongest secure central role."),
("Isak","Watkins","Isak","Liverpool attack and elite scoring ceiling narrowly outweigh Watkins' safer continuity."),
("Watkins","Thiago","Watkins","Higher raw points expectation in a stronger attack; Thiago's penalties keep it close."),
("Thiago","Gyökeres","Thiago","Premier League role and penalty certainty currently beat adaptation uncertainty."),
("Gyökeres","João Pedro","Gyökeres","Clearer elite-team number-nine ceiling; João Pedro has the broader creative floor."),
("Mateta","Solanke","Mateta","Penalty and focal-point role narrowly beat Solanke's stronger team context."),
("Solanke","Calvert-Lewin","Solanke","Higher expected minutes and stronger attacking environment."),
("Marmoush","Evanilson","Marmoush","Higher ceiling; rotation risk prevents a larger gap."),
("Evanilson","Šeško","Evanilson","Safer current availability and established minutes; Šeško reverses with full fitness and a locked role."),
("Wood","Wissa","Wood","Penalty/focal role and proven floor narrowly win; age and minutes are reversal triggers."),
("Wissa","Woltemade","Wissa","More proven Premier League scoring route."),
("Woltemade","Richarlison","Woltemade","Clearer season-long central role; Richarlison carries heavier competition risk."),
("Richarlison","Delap","Richarlison","Proven per-minute output narrowly wins, but Delap rises above him with confirmed starts."),
("Delap","Havertz","Delap","Clearer direct striker route; Havertz's role remains tactically variable."),
("Brobbey","Muniz","Brobbey","Slightly clearer first-choice route; Muniz has the stronger proven league production."),
("Muniz","Strand Larsen","Muniz","Better combination of raw points ceiling and established Premier League output."),
("Strand Larsen","Beto","Strand Larsen","More complete scoring profile; Beto's penalty/starting role could reverse it."),
("Beto","Nketiah","Beto","Clearer central-forward minutes and aerial route."),
("Nketiah","Welbeck","Nketiah","Higher season-long ceiling; Welbeck has the safer veteran floor when fit."),
("Igor Jesus","Barry","Igor Jesus","Stronger immediate senior-role case."),
("Barry","Ekitiké","Barry","Availability wins while Ekitiké carries an Achilles return-date risk."),
("Ekitiké","Osula","Ekitiké","Much higher ceiling if fit; Osula has a weak minutes path."),
("Kalimuendo","N.Jackson","Kalimuendo","Slightly clearer hierarchy; Jackson's transfer and minutes uncertainty cap him."),
("N.Jackson","Emegha","N.Jackson","More established Premier League production."),
("Emegha","Isidor","Emegha","Higher attacking ceiling despite fitness uncertainty."),
("Isidor","Wright","Isidor","Stronger current top-flight role case."),
("Wright","Hirst","Wright","Penalty potential and broader scoring route."),
("Hirst","Nmecha","Hirst","Clearer established central-forward pathway.")]
review_path=root/"06 Reviews/2026/08/2026-08-03/1648-AEST-review.md"
review_path.parent.mkdir(parents=True,exist_ok=True)
review_lines=["---","type: review",f"reviewed_at: {TS}","position: FWD","block: 1-30","challengers: 31-35","---","","# Forward positional review — block 1","","## Scope","","Insertion-sorted the first 30 forwards and tested the five forwards immediately below the block. Non-forward global slots were preserved; forwards were reassigned only across the existing forward-occupied global slots.","","## Sources and reconciliation","",f"- Official player identity, team, position and availability authority: {API}","- Canonical baseline: [[01 Current/Current Draft Board]].","- Team-level conclusions from the latest immutable club reviews were retained unless a direct forward-versus-forward comparison justified movement.","- No inaccessible source was used as evidence. No price, ownership or value-for-money input was used.","","## Comparator","","For every pair, raw expected season FPL points were assessed first. Expected minutes, tactical role, penalties/set pieces, injury and rotation risk, floor and ceiling followed. Positional scarcity did not distinguish these same-position comparisons.","","## Decisive comparisons"]
for a,b,w,why in comparisons: review_lines.append(f"- **{a} vs {b}: {w} first.** {why}")
review_lines += ["","## Final positional order for reviewed set",""]
for i,n in enumerate(new_order,1):
    p=replacement[by_name[n]['rank'] if False else next(s['rank'] for s in replacement.values() if s['player']==n)]
    review_lines.append(f"{i}. {n} — overall {p['rank']}")
review_lines += ["","## Evidence adopted","","- Current official API classification and availability metadata.","- Previously documented club-role, injury and competition conclusions where still consistent with the current canonical board.","","## Evidence rejected","","- Team-order rank alone was not treated as proof of cross-team superiority.","- Reputation without a credible minutes path did not justify promotion.","- No movement was manufactured for challengers 31–35 where the comparator did not beat the block boundary.","","## Close calls and reversal triggers","","- Watkins/Thiago reverses if Thiago retains penalties and Watkins loses meaningful minutes or penalty share.","- Evanilson/Šeško reverses when Šeško is fully fit and confirmed as the regular starter.","- Richarlison/Delap reverses with a sustained Delap starting role or continued Richarlison rotation.","- Brobbey/Muniz is low confidence and should react to competitive starting line-ups and penalty ownership.","- Ekitiké should rise materially once a reliable Achilles return and first-team role are confirmed.","","## Validation","","- Reviewed positional ranks 1–30 plus challengers 31–35.","- Preserved all non-forward global slots.","- Required complete ranks 1–350 and unique FPL IDs are checked by `scripts/validate_draft_board.py`."]
review_path.write_text("\n".join(review_lines)+"\n")

changes_path=root/"07 Changes/2026/08/2026-08-03/1648-AEST-changes.md"
changes_path.parent.mkdir(parents=True,exist_ok=True)
cl=["---","type: changes",f"changed_at: {TS}","position: FWD","block: 1-30","---","","# Forward block 1 changes","","## Rank changes",""]
for name,old,new in sorted(changes,key=lambda x:x[2]): cl.append(f"- {name}: **{old} → {new}**")
unchanged=[n for n in new_order if by_name[n]['rank']==next(p['rank'] for p in replacement.values() if p['player']==n)]
cl += ["","## Important no-change decisions","",f"- Unchanged within the reviewed set: {', '.join(unchanged)}.","- Challengers Isidor, Wright, Hirst and Nmecha did not enter the top 30 forwards.","- No non-forward player changed global rank.","","## Status and role changes","","- No new API position or team change was introduced by this positional pass.","- Existing injury and role discounts were retained, including Šeško and Ekitiké.","","## Next block","","- Forward positional ranks 31–60, challenged by ranks 26–30 and 61–65."]
changes_path.write_text("\n".join(cl)+"\n")

# Append latest links to Home, Wiki and watchlist without changing risk rows.
for rel in ["Home.md","Wiki.md","01 Current/Current Watchlist.md"]:
    path=root/rel
    s=path.read_text()
    s += f"\n\n<!-- {STAMP.lower()}-forward-block-1 -->\n- Forward ranks 1–30 reviewed with challengers 31–35: {REVIEW_LINK} · {CHANGE_LINK}.\n"
    path.write_text(s)

# Changelog one row per changed markdown file.
changed=[board_path,position_path,review_path,changes_path,root/"Home.md",root/"Wiki.md",root/"01 Current/Current Watchlist.md"]
changed += [next((root/"02 Players").glob(f"* - {p['id']}.md")) for p in replacement.values()]
log=root/"00 Meta/Document Changelog.md"
ls=log.read_text().rstrip()+"\n"
for path in changed+[log]:
    rel=path.as_posix()
    action="created" if path in [review_path,changes_path] else "updated"
    ls += f"| {TS} | `{rel}` | {action} | Forward positional ranks 1–30 with challengers 31–35 | {REVIEW_LINK} | {API}; {REVIEW_LINK}; {CHANGE_LINK} |\n"
log.write_text(ls)
