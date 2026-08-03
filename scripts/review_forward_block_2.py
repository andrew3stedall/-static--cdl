from pathlib import Path
import re

TS='2026-08-03T18:23:00+10:00'
STAMP='1823-AEST'
REVIEW='[[06 Reviews/2026/08/2026-08-03/1823-AEST-review]]'
CHANGES='[[07 Changes/2026/08/2026-08-03/1823-AEST-changes]]'
API='https://fantasy.premierleague.com/api/bootstrap-static/'
root=Path('vault')
board=root/'01 Current/Current Draft Board.md'
text=board.read_text()
row_re=re.compile(r'^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|$',re.M)
rows=[]
for m in row_re.finditer(text):
    rows.append({'rank':int(m.group(1)),'player':m.group(2).strip(),'position':m.group(3).strip(),'team':m.group(4).strip(),'segment':m.group(5).strip(),'tier':m.group(6).strip(),'id':int(m.group(7)),'status':m.group(8).strip(),'changed':m.group(9).strip(),'evidence':m.group(10).strip()})
assert len(rows)==350
fwds=[r for r in rows if r['position']=='FWD']
assert len(fwds)==52, len(fwds)
window=fwds[25:]
old_order=[r['player'] for r in window]
new_order=['Barry','Ekitiké','N.Jackson','Awoniyi','Kalimuendo','Emegha','Osula','Zirkzee','Georginio','Nmecha','Simms','Hirst','Wilson','Wright','Isidor','Akpom','McBurnie','Tzimas','Thomas-Asante','Kostoulas','Kusi-Asare','Enes Ünal','Al-Hamadi','Rodríguez','G.Jesus','Markelo','Emersonn']
assert set(old_order)==set(new_order),(old_order,set(new_order)-set(old_order),set(old_order)-set(new_order))
by_name={r['player']:r.copy() for r in window}
slots=sorted(window,key=lambda r:r['rank'])
replacement={}
changes=[]
for slot,name in zip(slots,new_order):
    p=by_name[name]
    old=p['rank']
    p['rank']=slot['rank']; p['segment']=slot['segment']; p['tier']=slot['tier']; p['changed']=TS; p['evidence']=REVIEW
    replacement[slot['rank']]=p
    if old!=p['rank']: changes.append((name,old,p['rank']))
lines=[]
for line in text.splitlines():
    m=row_re.match(line)
    if m and int(m.group(1)) in replacement:
        p=replacement[int(m.group(1))]
        lines.append(f"| {p['rank']} | {p['player']} | FWD | {p['team']} | {p['segment']} | {p['tier']} | {p['id']} | {p['status']} | {TS} | {REVIEW} |")
    else: lines.append(line)
newtext='\n'.join(lines)+'\n'
newtext=re.sub(r'(?m)^last_updated: .*$',f'last_updated: {TS}',newtext)
newtext=re.sub(r'(?m)^status: .*$', 'status: forward_position_blocks_1_2_reviewed', newtext)
board.write_text(newtext)

# player notes
for p in replacement.values():
    matches=list((root/'02 Players').glob(f"* - {p['id']}.md")); assert len(matches)==1,(p,matches)
    path=matches[0]; s=path.read_text()
    s=re.sub(r'(?m)^current_rank: .*$',f"current_rank: {p['rank']}",s)
    s=re.sub(r'(?m)^segment: .*$',f"segment: {p['segment']}",s)
    s=re.sub(r'(?m)^tier: .*$',f"tier: {p['tier']}",s)
    s=re.sub(r'(?m)^last_reviewed: .*$',f'last_reviewed: {TS}',s)
    old=by_name[p['player']]['rank']; pos=new_order.index(p['player'])+26
    s += f"\n\n## {STAMP} forward positional comparison\n\n- Forward order: **{pos} of {len(fwds)}** after reviewing ranks 31–52 with upper challengers 26–30.\n- Overall rank: **{old} → {p['rank']}**.\n- Comparator: raw expected points, then minutes, role, set pieces, injury/rotation risk, floor and ceiling.\n- Evidence and reversal triggers: {REVIEW}.\n"
    path.write_text(s)

# rebuild Forward.md
updated=board.read_text(); rows2=[]
for m in row_re.finditer(updated):
    rows2.append({'rank':int(m.group(1)),'player':m.group(2).strip(),'position':m.group(3).strip(),'team':m.group(4).strip(),'segment':m.group(5).strip(),'tier':m.group(6).strip(),'id':int(m.group(7)),'status':m.group(8).strip()})
fwd=[r for r in rows2 if r['position']=='FWD']
pos=root/'04 Positions/Forward.md'; s=pos.read_text(); a=s.index('<!-- ranked-players:start -->'); b=s.index('<!-- ranked-players:end -->')+len('<!-- ranked-players:end -->')
section=['<!-- ranked-players:start -->','## Players by overall rank','','Players are listed in canonical overall draft rank order.','']
for r in fwd:
    matches=list((root/'02 Players').glob(f"* - {r['id']}.md")); assert len(matches)==1
    section.append(f"{r['rank']}. [[02 Players/{matches[0].stem}|{r['player']}]] — FWD, {r['team']}; {r['segment']} / {r['tier']}; {r['status']}")
section += ['',f'Source: [[01 Current/Current Draft Board]] · generated {TS}','<!-- ranked-players:end -->']
s=s[:a]+'\n'.join(section)+s[b:]
s=re.sub(r'(?m)^last_reviewed: .*$',f'last_reviewed: {TS}',s)
s += f"\n\n## {STAMP} block 2 review\n\n- Positional ranks 31–52 were insertion-sorted with upper challengers 26–30; there were no lower challengers because only 52 forwards are in the canonical pool.\n- Review: {REVIEW}.\n- Changes: {CHANGES}.\n"
pos.write_text(s)

comparisons=[
('Barry','Ekitiké','Barry','Availability and a clearer immediate role beat the injured higher ceiling.'),
('Ekitiké','N.Jackson','Ekitiké','Higher ceiling if fit; Jackson has the safer current availability.'),
('N.Jackson','Awoniyi','N.Jackson','Stronger recent top-flight production and broader route to starts.'),
('Awoniyi','Kalimuendo','Awoniyi','Proven Premier League scoring, narrowly, with durability risk.'),
('Kalimuendo','Emegha','Kalimuendo','Clearer current hierarchy and availability.'),
('Emegha','Osula','Emegha','Higher scoring ceiling despite hamstring risk.'),
('Osula','Zirkzee','Osula','Slightly cleaner direct-striker role; both have weak minutes certainty.'),
('Zirkzee','Georginio','Zirkzee','More direct central-forward route.'),
('Georginio','Nmecha','Georginio','Better creative and attacking floor.'),
('Nmecha','Simms','Nmecha','Top-flight role and broader link-play route narrowly win.'),
('Simms','Hirst','Simms','Higher proven scoring ceiling.'),
('Hirst','Wilson','Hirst','Clearer starting-centre-forward pathway.'),
('Wilson','Wright','Wilson','Higher upside if fit; Wright has the safer floor.'),
('Wright','Isidor','Wright','Penalty potential and broader scoring route.'),
('Isidor','Akpom','Isidor','Stronger current top-flight role case.'),
('Akpom','McBurnie','Akpom','Better recent scoring record and mobility.'),
('McBurnie','Tzimas','McBurnie','Availability beats Tzimas knee uncertainty.'),
('Tzimas','Thomas-Asante','Tzimas','Higher long-term ceiling if fit.'),
('Thomas-Asante','Kostoulas','Thomas-Asante','More established senior scoring record.'),
('Kostoulas','Kusi-Asare','Kostoulas','Slightly clearer first-team pathway.'),
('Kusi-Asare','Enes Ünal','Kusi-Asare','Availability wins; Ünal remains a major return-to-fitness watch.'),
('Enes Ünal','Al-Hamadi','Enes Ünal','Much stronger proven scoring profile when fit.'),
('Al-Hamadi','Rodríguez','Al-Hamadi','Slightly clearer current hierarchy.'),
('Rodríguez','G.Jesus','Rodríguez','Availability and role path beat long-term injury uncertainty.'),
('G.Jesus','Markelo','G.Jesus','Far higher ceiling even with severe availability risk.'),
('Markelo','Emersonn','Markelo','Marginally clearer senior pathway; low confidence.')]
review=root/'06 Reviews/2026/08/2026-08-03/1823-AEST-review.md'; review.parent.mkdir(parents=True,exist_ok=True)
rl=['---','type: review',f'reviewed_at: {TS}','position: FWD','block: 31-52','challengers: 26-30','---','','# Forward positional review — block 2','','## Scope','','Reviewed positional ranks 31–52 with upper-bound challengers 26–30. The canonical pool contains 52 forwards, so no lower challengers existed. Non-forward global slots were preserved.','','## Sources and reconciliation','',f'- Official player identity, team, position and availability authority: {API}','- Canonical baseline: [[01 Current/Current Draft Board]].','- Latest immutable team and block-1 reviews supplied role and injury context.','- No price, ownership or value-for-money evidence was used.','','## Decisive comparisons']
for a,b,w,why in comparisons: rl.append(f'- **{a} vs {b}: {w} first.** {why}')
rl += ['','## Final positional order from rank 26','']
for i,n in enumerate(new_order,26):
    p=next(v for v in replacement.values() if v['player']==n); rl.append(f'{i}. {n} — overall {p["rank"]}')
rl += ['','## Close calls and reversal triggers','','- Ekitiké rises rapidly with a reliable Achilles return and starting role.','- Wilson rises with sustained fitness and starts.','- Tzimas rises once knee availability and first-team minutes are confirmed.','- Enes Ünal rises materially once fully fit.','- G.Jesus remains a ceiling-only stash until a dependable return and role exist.','','## Validation','','- Reviewed all remaining forwards, with positional ranks 26–30 retained as upper-bound challengers.','- Preserved every non-forward global slot.','- `scripts/validate_draft_board.py` checks complete ranks 1–350 and unique FPL IDs.']
review.write_text('\n'.join(rl)+'\n')

changes_path=root/'07 Changes/2026/08/2026-08-03/1823-AEST-changes.md'; changes_path.parent.mkdir(parents=True,exist_ok=True)
cl=['---','type: changes',f'changed_at: {TS}','position: FWD','block: 31-52','---','','# Forward block 2 changes','','## Rank changes','']
for n,o,nr in sorted(changes,key=lambda x:x[2]): cl.append(f'- {n}: **{o} → {nr}**')
unch=[n for n in new_order if by_name[n]['rank']==next(v['rank'] for v in replacement.values() if v['player']==n)]
cl += ['','## Important no-change decisions','',f"- Unchanged: {', '.join(unch) if unch else 'none'}.",'- Barry and Ekitiké remained above the block boundary challengers below them.','- No non-forward player changed global rank.','','## Next step','','- Forward position is now fully reviewed; proceed to midfield positional block 1.']
changes_path.write_text('\n'.join(cl)+'\n')

for rel in ['Home.md','Wiki.md','01 Current/Current Watchlist.md']:
    p=root/rel; q=p.read_text(); q += f"\n\n<!-- {STAMP.lower()}-forward-block-2 -->\n- Forward ranks 31–52 reviewed with upper challengers 26–30: {REVIEW} · {CHANGES}.\n"; p.write_text(q)

changed=[board,pos,review,changes_path,root/'Home.md',root/'Wiki.md',root/'01 Current/Current Watchlist.md']+[next((root/'02 Players').glob(f"* - {p['id']}.md")) for p in replacement.values()]
log=root/'00 Meta/Document Changelog.md'; ls=log.read_text().rstrip()+'\n'
for p in changed+[log]:
    action='created' if p in (review,changes_path) else 'updated'
    ls += f"| {TS} | `{p.as_posix()}` | {action} | Forward positional ranks 31–52 with challengers 26–30 | {REVIEW} | {API}; {REVIEW}; {CHANGES} |\n"
log.write_text(ls)
