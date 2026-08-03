from pathlib import Path
import re

TS='2026-08-03T21:23:00+10:00'
STAMP='2123-AEST'
REVIEW='[[06 Reviews/2026/08/2026-08-03/2123-AEST-review]]'
CHANGES='[[07 Changes/2026/08/2026-08-03/2123-AEST-changes]]'
API='https://fantasy.premierleague.com/api/bootstrap-static/'
root=Path('vault')
board=root/'01 Current/Current Draft Board.md'
text=board.read_text()
row_re=re.compile(r'^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|$',re.M)
rows=[]
for m in row_re.finditer(text):
    rows.append({'rank':int(m.group(1)),'player':m.group(2).strip(),'position':m.group(3).strip(),'team':m.group(4).strip(),'segment':m.group(5).strip(),'tier':m.group(6).strip(),'id':int(m.group(7)),'status':m.group(8).strip(),'changed':m.group(9).strip(),'evidence':m.group(10).strip()})
assert len(rows)==350
mids=[r for r in rows if r['position']=='MID']
block=mids[:35]
old_order=[r['player'] for r in block]
new_order=['Palmer','Saka','B.Fernandes','Mbeumo','Cunha','Wirtz','Semenyo','Foden','Gibbs-White','Rogers','Gakpo','Eze','Kluivert','Ødegaard','Tavernier','Szoboszlai','Damsgaard','Bruno G.','Cherki','O.Dango','Rice','Dewsbury-Hall','Ndiaye','Schade','Doku','E.Le Fée','Enzo','Sarr','Minteh','Fernandes','Amad','Neto','Kudus','Barnes','Wilson']
assert set(old_order)==set(new_order),(old_order,set(new_order)-set(old_order),set(old_order)-set(new_order))
by={r['player']:r.copy() for r in block}
slots=sorted(block,key=lambda x:x['rank'])
replacement={}; moves=[]
for slot,name in zip(slots,new_order):
    p=by[name].copy(); old=p['rank']
    p['rank']=slot['rank']; p['segment']=slot['segment']; p['tier']=slot['tier']; p['changed']=TS; p['evidence']=REVIEW
    replacement[slot['rank']]=p
    if old!=p['rank']: moves.append((name,old,p['rank']))
out=[]
for line in text.splitlines():
    m=row_re.match(line)
    if m and int(m.group(1)) in replacement:
        p=replacement[int(m.group(1))]
        out.append(f"| {p['rank']} | {p['player']} | MID | {p['team']} | {p['segment']} | {p['tier']} | {p['id']} | {p['status']} | {TS} | {REVIEW} |")
    else: out.append(line)
newtext='\n'.join(out)+'\n'
newtext=re.sub(r'(?m)^last_updated: .*$',f'last_updated: {TS}',newtext)
newtext=re.sub(r'(?m)^status: .*$', 'status: midfield_position_block_1_reviewed', newtext)
newtext=newtext.replace('This is the **only canonical current overall ordering**. The first 170 have now been manually stable-sorted; this run reviewed ranks 141–170 with challengers from 136–175. Raw expected FPL points are assessed first, followed by minutes, role, set pieces and risk; positional replacement value then determines draft priority in close cross-position comparisons.','This is the **only canonical current overall ordering**. Midfield positional ranks 1–30 have now been insertion-sorted with challengers 31–35. Raw expected FPL points were assessed first, followed by minutes, role, set pieces, injury and rotation risk, floor and ceiling. All non-midfielder global slots were preserved.')
board.write_text(newtext)

for p in replacement.values():
    paths=list((root/'02 Players').glob(f"* - {p['id']}.md")); assert len(paths)==1,(p,paths)
    path=paths[0]; s=path.read_text()
    s=re.sub(r'(?m)^current_rank: .*$',f"current_rank: {p['rank']}",s)
    s=re.sub(r'(?m)^segment: .*$',f"segment: {p['segment']}",s)
    s=re.sub(r'(?m)^tier: .*$',f"tier: {p['tier']}",s)
    s=re.sub(r'(?m)^last_reviewed: .*$',f'last_reviewed: {TS}',s)
    pos=new_order.index(p['player'])+1; old=by[p['player']]['rank']
    s=s.rstrip()+f"\n\n## {STAMP} midfield positional comparison\n\n- Midfield order: **{pos}** after block 1 with challengers 31–35.\n- Overall rank: **{old} → {p['rank']}**.\n- Raw expected points were compared before minutes, role, set pieces, injury/rotation risk, floor and ceiling.\n- Evidence and reversal triggers: {REVIEW}.\n"
    path.write_text(s+'\n')

updated=board.read_text(); rows2=[]
for m in row_re.finditer(updated):
    rows2.append({'rank':int(m.group(1)),'player':m.group(2).strip(),'position':m.group(3).strip(),'team':m.group(4).strip(),'segment':m.group(5).strip(),'tier':m.group(6).strip(),'id':int(m.group(7)),'status':m.group(8).strip()})
pos=root/'04 Positions/Midfielder.md'; pt=pos.read_text()
start=pt.index('<!-- ranked-players:start -->'); end=pt.index('<!-- ranked-players:end -->')+len('<!-- ranked-players:end -->')
sec=['<!-- ranked-players:start -->','## Players by overall rank','','Players are listed in canonical overall draft rank order.','']
for r in [x for x in rows2 if x['position']=='MID']:
    paths=list((root/'02 Players').glob(f"* - {r['id']}.md")); assert len(paths)==1
    sec.append(f"{r['rank']}. [[02 Players/{paths[0].stem}|{r['player']}]] — MID, {r['team']}; {r['segment']} / {r['tier']}; {r['status']}")
sec += ['',f'Source: [[01 Current/Current Draft Board]] · generated {TS}','<!-- ranked-players:end -->']
pt=pt[:start]+'\n'.join(sec)+pt[end:]
pt=re.sub(r'(?m)^last_reviewed: .*$',f'last_reviewed: {TS}',pt)
leaders='## Current leaders\n\n1. [[02 Players/Palmer - 154]]\n2. [[02 Players/Saka - 12]]\n3. [[02 Players/B.Fernandes - 426]]\n4. [[02 Players/Mbeumo - 427]]\n5. [[02 Players/Cunha - 428]]\n6. [[02 Players/Wirtz - 366]]\n7. [[02 Players/Semenyo - 397]]\n8. [[02 Players/Foden - 398]]'
pt=re.sub(r'## Current leaders\n.*?\n## Current risks',leaders+'\n\n## Current risks',pt,flags=re.S)
pt += f"\n\n## {STAMP} block 1 review\n\n- Midfield ranks 1–30 were insertion-sorted with challengers 31–35.\n- Review: {REVIEW}.\n- Changes: {CHANGES}.\n"
pos.write_text(pt)

comparisons=[('Palmer','Saka','Palmer','Penalties and the broadest secure attacking role narrowly win.'),('Saka','B.Fernandes','Saka','Higher team attacking ceiling; Bruno retains the stronger set-piece monopoly.'),('B.Fernandes','Mbeumo','B.Fernandes','Penalty and chance-creation floor remain superior.'),('Mbeumo','Cunha','Mbeumo','More direct goal involvement and stronger minutes outlook.'),('Wirtz','Semenyo','Wirtz','Creative centrality and elite-team context narrowly win.'),('Semenyo','Foden','Semenyo','Safer expected minutes; Foden has the higher ceiling.'),('Foden','Gibbs-White','Foden','Higher ceiling in the stronger attack despite rotation.'),('Gibbs-White','Rogers','Gibbs-White','Penalties and set pieces provide the safer floor.'),('Rogers','Gakpo','Rogers','Broader minutes route; Gakpo carries more role competition.'),('Gakpo','Eze','Gakpo','Stronger direct scoring ceiling.'),('Eze','Kluivert','Eze','Higher proven creative and scoring ceiling.'),('Kluivert','Ødegaard','Kluivert','Penalties and direct goal threat beat the creative floor.'),('Ødegaard','Tavernier','Ødegaard','Safer elite-team minutes and chance creation.'),('Tavernier','Szoboszlai','Tavernier','Set pieces and wider attacking responsibility narrowly win.'),('Szoboszlai','Damsgaard','Szoboszlai','Higher goal involvement in the stronger attack.'),('Damsgaard','Bruno G.','Damsgaard','More direct chance creation and set-piece access.'),('Bruno G.','Cherki','Bruno G.','Minutes security beats Cherki rotation risk.'),('Cherki','O.Dango','Cherki','Higher per-minute attacking ceiling.'),('O.Dango','Rice','O.Dango','More direct goal threat.'),('Rice','Dewsbury-Hall','Rice','Set pieces and secure elite-team minutes.'),('Dewsbury-Hall','Ndiaye','Dewsbury-Hall','Broader creative role narrowly wins.'),('Ndiaye','Schade','Ndiaye','Safer minutes and more complete attacking involvement.'),('Schade','Doku','Schade','Better expected minutes; Doku has the higher ceiling.'),('Doku','E.Le Fée','Doku','Superior per-minute attacking threat.'),('E.Le Fée','Enzo','E.Le Fée','More advanced role and set-piece access.'),('Enzo','Sarr','Enzo','Safer minutes and accumulation floor.'),('Sarr','Minteh','Sarr','More established production and role security.'),('Minteh','Fernandes','Minteh','Greater direct attacking upside.'),('Fernandes','Amad','Fernandes','Slightly safer current minutes route.'),('Amad','Neto','Amad','More central creative involvement.'),('Neto','Kudus','Neto','Current fitness advantage; fit Kudus can reverse.'),('Kudus','Barnes','Kudus','Broader attacking role when fit.'),('Barnes','Wilson','Barnes','Higher proven top-flight scoring ceiling.')]
review=root/'06 Reviews/2026/08/2026-08-03/2123-AEST-review.md'; review.parent.mkdir(parents=True,exist_ok=True)
rl=['---','type: review',f'reviewed_at: {TS}','position: MID','block: 1-30','challengers: 31-35','---','','# Midfield positional review — block 1','','## Scope','','Insertion-sorted the first 30 midfielders and tested midfielders 31–35 as lower-bound challengers. Every non-midfielder retained its global slot.','','## Sources and reconciliation','',f'- Official identity, team, position and availability authority: {API}','- Canonical baseline: [[01 Current/Current Draft Board]].','- Existing immutable team reviews supplied role, injury and competition context.','- No price, ownership or value-for-money input was used.','','## Comparator','','Raw expected season FPL points were assessed first, then minutes, role, penalties and set pieces, injury and rotation risk, floor and ceiling.','','## Decisive comparisons']
for a,b,w,why in comparisons: rl.append(f'- **{a} vs {b}: {w} first.** {why}')
rl += ['','## Final order for reviewed set','']
for i,n in enumerate(new_order,1):
    p=next(v for v in replacement.values() if v['player']==n); rl.append(f'{i}. {n} — overall {p["rank"]}')
rl += ['','## Close calls and reversal triggers','','- Palmer/Saka/Bruno remains a close elite tier; penalty changes or material role shifts can reorder them.','- Semenyo/Foden reverses if Foden becomes a secure starter.','- Kluivert/Ødegaard depends heavily on penalty ownership and role continuity.','- Cherki rises rapidly with repeated starts.','- Neto/Kudus reverses when Kudus is fully fit and secure.','','## Validation','','- Reviewed midfield ranks 1–30 plus challengers 31–35.','- Preserved all non-midfielder global slots.','- `scripts/validate_draft_board.py` checks complete ranks 1–350 and unique FPL IDs.']
review.write_text('\n'.join(rl)+'\n')

changes=root/'07 Changes/2026/08/2026-08-03/2123-AEST-changes.md'; changes.parent.mkdir(parents=True,exist_ok=True)
unchanged=[n for n in new_order if by[n]['rank']==next(v['rank'] for v in replacement.values() if v['player']==n)]
cl=['---','type: changes',f'changed_at: {TS}','position: MID','block: 1-30','---','','# Midfield block 1 changes','','## Rank changes','']
for n,o,r in sorted(moves,key=lambda x:x[2]): cl.append(f'- {n}: **{o} → {r}**')
cl += ['','## Important no-change decisions','',f"- Unchanged: {', '.join(unchanged) if unchanged else 'None'}.",'- Challengers Amad, Neto, Kudus, Barnes and Wilson did not enter the top 30 midfielders.','- No non-midfielder changed global rank.','','## Next block','','- Midfield ranks 31–60, challenged by ranks 26–30 and 61–65.']
changes.write_text('\n'.join(cl)+'\n')

for rel in ['Home.md','Wiki.md','01 Current/Current Watchlist.md']:
    path=root/rel; s=path.read_text().rstrip()+f"\n\n<!-- {STAMP.lower()}-midfield-block-1 -->\n- Midfield ranks 1–30 reviewed with challengers 31–35: {REVIEW} · {CHANGES}.\n"; path.write_text(s)
changed=[board,pos,review,changes,root/'Home.md',root/'Wiki.md',root/'01 Current/Current Watchlist.md']+[next((root/'02 Players').glob(f"* - {p['id']}.md")) for p in replacement.values()]
log=root/'00 Meta/Document Changelog.md'; ls=log.read_text().rstrip()+'\n'
for path in changed+[log]:
    action='created' if path in [review,changes] else 'updated'
    ls += f"| {TS} | `{path.as_posix()}` | {action} | Midfield positional ranks 1–30 with challengers 31–35 | {REVIEW} | {API}; {REVIEW}; {CHANGES} |\n"
log.write_text(ls)
