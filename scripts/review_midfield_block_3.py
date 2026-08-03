from pathlib import Path
import re
TS='2026-08-03T23:16:00+10:00'
STAMP='2316-AEST'
REVIEW='[[06 Reviews/2026/08/2026-08-03/2316-AEST-review]]'
CHANGES='[[07 Changes/2026/08/2026-08-03/2316-AEST-changes]]'
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
block=mids[55:95]
old_order=[r['player'] for r in block]
new_order=['Reijnders','Garnacho','Mac Allister','Anderson','Jensen','McGinn','Aaronson','Ndoye','Lewis-Potter','Scott','Adingra','Brooks','Garner','Zubimendi','Bobb','King','Hutchinson','Gravenberch','Sadiki','Ayari','Hinshelwood','Ampadu','Grealish','Xavi','Caicedo','Yeremy','Merino','Gallagher','Rodrigo','Mount','Mainoo','C.Jones','Ngumoha','Adli','Kamada','Anthony','Kevin','Wharton','P.M.Sarr','Tzolis']
assert set(old_order)==set(new_order),(old_order,set(new_order)-set(old_order),set(old_order)-set(new_order))
by={r['player']:r.copy() for r in block}; slots=sorted(block,key=lambda x:x['rank']); replacement={}; moves=[]
for slot,name in zip(slots,new_order):
    p=by[name].copy(); old=p['rank']; p['rank']=slot['rank']; p['segment']=slot['segment']; p['tier']=slot['tier']; p['changed']=TS; p['evidence']=REVIEW; replacement[slot['rank']]=p
    if old!=p['rank']: moves.append((name,old,p['rank']))
out=[]
for line in text.splitlines():
    m=row_re.match(line)
    if m and int(m.group(1)) in replacement:
        p=replacement[int(m.group(1))]; out.append(f"| {p['rank']} | {p['player']} | MID | {p['team']} | {p['segment']} | {p['tier']} | {p['id']} | {p['status']} | {TS} | {REVIEW} |")
    else: out.append(line)
newtext='\n'.join(out)+'\n'; newtext=re.sub(r'(?m)^last_updated: .*$',f'last_updated: {TS}',newtext); newtext=re.sub(r'(?m)^status: .*$', 'status: midfield_position_block_3_reviewed',newtext); board.write_text(newtext)
for p in replacement.values():
    paths=list((root/'02 Players').glob(f"* - {p['id']}.md")); assert len(paths)==1,(p,paths)
    path=paths[0]; s=path.read_text(); s=re.sub(r'(?m)^current_rank: .*$',f"current_rank: {p['rank']}",s); s=re.sub(r'(?m)^segment: .*$',f"segment: {p['segment']}",s); s=re.sub(r'(?m)^tier: .*$',f"tier: {p['tier']}",s); s=re.sub(r'(?m)^last_reviewed: .*$',f'last_reviewed: {TS}',s)
    pos=new_order.index(p['player'])+56; old=by[p['player']]['rank']; s=s.rstrip()+f"\n\n## {STAMP} midfield positional comparison\n\n- Midfield order: **{pos}** after block 3 with challengers 56–60 and 91–95.\n- Overall rank: **{old} → {p['rank']}**.\n- Raw expected points were compared before minutes, role, set pieces, injury/rotation risk, floor and ceiling.\n- Evidence and reversal triggers: {REVIEW}.\n"; path.write_text(s+'\n')
updated=board.read_text(); rows2=[]
for m in row_re.finditer(updated): rows2.append({'rank':int(m.group(1)),'player':m.group(2).strip(),'position':m.group(3).strip(),'team':m.group(4).strip(),'segment':m.group(5).strip(),'tier':m.group(6).strip(),'id':int(m.group(7)),'status':m.group(8).strip()})
pos=root/'04 Positions/Midfielder.md'; pt=pos.read_text(); start=pt.index('<!-- ranked-players:start -->'); end=pt.index('<!-- ranked-players:end -->')+len('<!-- ranked-players:end -->'); sec=['<!-- ranked-players:start -->','## Players by overall rank','','Players are listed in canonical overall draft rank order.','']
for r in [x for x in rows2 if x['position']=='MID']:
    path=next((root/'02 Players').glob(f"* - {r['id']}.md")); sec.append(f"{r['rank']}. [[02 Players/{path.stem}|{r['player']}]] — MID, {r['team']}; {r['segment']} / {r['tier']}; {r['status']}")
sec += ['',f'Source: [[01 Current/Current Draft Board]] · generated {TS}','<!-- ranked-players:end -->']; pt=pt[:start]+'\n'.join(sec)+pt[end:]; pt=re.sub(r'(?m)^last_reviewed: .*$',f'last_reviewed: {TS}',pt); pt += f"\n\n## {STAMP} block 3 review\n\n- Midfield ranks 61–90 were insertion-sorted with challengers 56–60 and 91–95.\n- Review: {REVIEW}.\n- Changes: {CHANGES}.\n"; pos.write_text(pt)
comparisons=[('Reijnders','Garnacho','Reijnders','Safer current role and stronger accumulation floor.'),('Garnacho','Mac Allister','Garnacho','Higher direct attacking ceiling despite role uncertainty.'),('Mac Allister','Anderson','Mac Allister','Set pieces and elite-team minutes.'),('Anderson','Jensen','Anderson','Stronger minutes outlook and broader contribution floor.'),('Jensen','McGinn','Jensen','Set-piece access and chance creation.'),('McGinn','Aaronson','McGinn','Safer minutes and stronger floor.'),('Aaronson','Ndoye','Aaronson','More secure current role.'),('Ndoye','Lewis-Potter','Ndoye','Stronger direct scoring route.'),('Lewis-Potter','Scott','Lewis-Potter','More advanced role.'),('Scott','Adingra','Scott','Safer current minutes; Adingra has the higher ceiling.'),('Adingra','Brooks','Adingra','Greater direct goal threat.'),('Brooks','Garner','Brooks','More attacking deployment.'),('Garner','Zubimendi','Garner','Set pieces and slightly greater direct-return route.'),('Zubimendi','Bobb','Zubimendi','Minutes security beats rotation risk.'),('Bobb','King','Bobb','Higher per-minute attacking ceiling.'),('King','Hutchinson','King','More advanced attacking upside.'),('Hutchinson','Gravenberch','Hutchinson','Greater direct-return ceiling.'),('Gravenberch','Sadiki','Gravenberch','Elite-team minutes and floor.'),('Sadiki','Ayari','Sadiki','Slightly stronger minutes case.'),('Ayari','Hinshelwood','Ayari','More advanced role.'),('Hinshelwood','Ampadu','Hinshelwood','Higher attacking involvement.'),('Ampadu','Grealish','Ampadu','Availability and minutes floor.'),('Grealish','Xavi','Grealish','Current availability narrowly wins.'),('Xavi','Caicedo','Xavi','Higher attacking ceiling despite injury uncertainty.'),('Caicedo','Yeremy','Caicedo','Much safer minutes floor.'),('Yeremy','Merino','Yeremy','More direct attacking upside.'),('Merino','Gallagher','Merino','Better scoring route in an elite attack.'),('Gallagher','Rodrigo','Gallagher','More direct box involvement.'),('Rodrigo','Mount','Rodrigo','Safer role when fit.'),('Mount','Mainoo','Mount','More advanced attacking role.'),('Mainoo','C.Jones','Mainoo','Slightly clearer path to central starts.'),('C.Jones','Ngumoha','C.Jones','Safer senior minutes.'),('Ngumoha','Adli','Ngumoha','Higher breakout ceiling.'),('Adli','Kamada','Adli','More advanced attacking role.'),('Kamada','Anthony','Kamada','Better proven creative output.'),('Anthony','Kevin','Anthony','Clearer senior minutes route.'),('Kevin','Wharton','Kevin','Higher attacking ceiling.'),('Wharton','P.M.Sarr','Wharton','Safer minutes and set-piece route when fit.'),('P.M.Sarr','Tzolis','P.M.Sarr','Stronger current minutes certainty.')]
review=root/'06 Reviews/2026/08/2026-08-03/2316-AEST-review.md'; review.parent.mkdir(parents=True,exist_ok=True); rl=['---','type: review',f'reviewed_at: {TS}','position: MID','block: 61-90','challengers: 56-60,91-95','---','','# Midfield positional review — block 3','','## Scope','','Insertion-sorted midfield positional ranks 61–90 and tested ranks 56–60 and 91–95 as boundary challengers. Every non-midfielder retained its global slot.','','## Sources and reconciliation','',f'- Official identity, team, position and availability authority: {API}','- Canonical baseline: [[01 Current/Current Draft Board]].','- Existing immutable team and prior positional reviews supplied role, injury and competition context.','','## Decisive comparisons']
for a,b,w,why in comparisons: rl.append(f'- **{a} vs {b}: {w} first.** {why}')
rl += ['','## Final reviewed order','']
for i,n in enumerate(new_order,56): p=next(v for v in replacement.values() if v['player']==n); rl.append(f'{i}. {n} — overall {p["rank"]}')
rl += ['','## Close calls and reversal triggers','','- Garnacho can rise sharply with a secure starting role.','- Adingra can pass Scott with repeated starts.','- Bobb and King remain high-variance minutes bets.','- Xavi rises when healthy and starting.','- Wharton rises when fully fit and retaining set pieces.','','## Validation','','- Preserved all non-midfielder global slots.','- `scripts/validate_draft_board.py` checks complete ranks 1–350 and unique FPL IDs.']; review.write_text('\n'.join(rl)+'\n')
changes=root/'07 Changes/2026/08/2026-08-03/2316-AEST-changes.md'; changes.parent.mkdir(parents=True,exist_ok=True); unchanged=[n for n in new_order if by[n]['rank']==next(v['rank'] for v in replacement.values() if v['player']==n)]; cl=['---','type: changes',f'changed_at: {TS}','position: MID','block: 61-90','---','','# Midfield block 3 changes','','## Rank changes','']
for n,o,r in sorted(moves,key=lambda x:x[2]): cl.append(f'- {n}: **{o} → {r}**')
cl += ['','## Important no-change decisions','',f"- Unchanged: {', '.join(unchanged) if unchanged else 'None'}.",'- Upper challengers Reijnders, Anderson, Jensen, McGinn and Aaronson were tested.','- Lower challengers Anthony, Kevin, Wharton, P.M.Sarr and Tzolis were tested.','- No non-midfielder changed global rank.','','## Next block','','- Midfield ranks 91–120, challenged by ranks 86–90 and 121–125.']; changes.write_text('\n'.join(cl)+'\n')
for rel in ['Home.md','Wiki.md','01 Current/Current Watchlist.md']:
    path=root/rel; path.write_text(path.read_text().rstrip()+f"\n\n<!-- {STAMP.lower()}-midfield-block-3 -->\n- Midfield ranks 61–90 reviewed with challengers 56–60 and 91–95: {REVIEW} · {CHANGES}.\n")
changed=[board,pos,review,changes,root/'Home.md',root/'Wiki.md',root/'01 Current/Current Watchlist.md']+[next((root/'02 Players').glob(f"* - {p['id']}.md")) for p in replacement.values()]; log=root/'00 Meta/Document Changelog.md'; ls=log.read_text().rstrip()+'\n'
for path in changed+[log]:
    action='created' if path in [review,changes] else 'updated'; ls += f"| {TS} | `{path.as_posix()}` | {action} | Midfield positional ranks 61–90 with challengers 56–60 and 91–95 | {REVIEW} | {API}; {REVIEW}; {CHANGES} |\n"
log.write_text(ls)
