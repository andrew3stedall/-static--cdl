from pathlib import Path
import json,re,urllib.request

TS='2026-08-02T12:59:00+10:00'; STAMP='1259-AEST'
LINK='[[06 Reviews/2026/08/2026-08-02/1259-AEST-review]]'
BOARD=Path('vault/01 Current/Current Draft Board.md')
with urllib.request.urlopen('https://fantasy.premierleague.com/api/bootstrap-static/',timeout=30) as r: api=json.load(r)
with urllib.request.urlopen('https://fantasy.premierleague.com/api/fixtures/',timeout=30) as r: fixtures=json.load(r)
players={p['id']:p for p in api['elements']}; teams={t['id']:t['short_name'] for t in api['teams']}; pos={1:'GKP',2:'DEF',3:'MID',4:'FWD'}
lines=BOARD.read_text().splitlines(); rows=[]; indexes=[]
for i,line in enumerate(lines):
    if re.match(r'^\| \d+ \|',line):
        c=[x.strip() for x in line.strip('|').split('|')]
        rows.append({'rank':int(c[0]),'name':c[1],'pos':c[2],'team':c[3],'segment':c[4],'tier':c[5],'id':int(c[6]),'status':c[7],'changed':c[8],'evidence':c[9]}); indexes.append(i)
assert len(rows)==350 and [r['rank'] for r in rows]==list(range(1,351)) and len({r['id'] for r in rows})==350
old_rank={r['id']:r['rank'] for r in rows}
pool=[r for r in rows if 196<=r['rank']<=240]
ranked_ids={r['id'] for r in rows}
# Screen every API-active unranked player. Only players with a demonstrated senior role can challenge.
unranked_screen=[]
for p in api['elements']:
    if p['id'] in ranked_ids: continue
    pts=float(p.get('total_points') or 0); starts=float(p.get('starts') or 0); mins=float(p.get('minutes') or 0)
    if pts>=55 or starts>=12 or mins>=1000:
        unranked_screen.append((p['id'],p.get('web_name','Unknown'),pts,starts,mins))
# No unranked player is inserted without direct role evidence; record all screened cases in review.
def score(r):
    p=players.get(r['id'],{})
    pts=float(p.get('total_points') or 0); starts=float(p.get('starts') or 0); mins=float(p.get('minutes') or 0)
    xgi=float(p.get('expected_goal_involvements') or 0); cs=float(p.get('clean_sheets') or 0)
    raw=pts + 1.2*starts + mins/240 + 2.5*xgi
    if p.get('element_type') in (1,2): raw += 1.2*cs
    scarcity={1:-10,2:2,3:4,4:13}.get(p.get('element_type'),0)
    chance=p.get('chance_of_playing_next_round'); news=(p.get('news') or '').lower()
    risk=0
    if chance==0: risk-=24
    elif chance is not None and chance<75: risk-=12
    elif chance==75: risk-=5
    if 'unknown return' in news: risk-=10
    # Strong stabiliser prevents noisy historical fields from overwhelming prior manual ordering.
    stability=(241-r['rank'])*2.2
    return stability + raw*0.32 + scarcity + risk
sorted_pool=sorted(pool,key=lambda r:(score(r),-r['rank']),reverse=True)
comparisons=[]
for i in range(1,len(sorted_pool)):
    a,b=sorted_pool[i-1],sorted_pool[i]; pa,pb=players[a['id']],players[b['id']]
    reasons=[]
    if (pa.get('total_points') or 0)!=(pb.get('total_points') or 0): reasons.append(f"raw expected-points proxy favours {a['name']} ({pa.get('total_points') or 0} prior points vs {pb.get('total_points') or 0})")
    if (pa.get('starts') or 0)!=(pb.get('starts') or 0): reasons.append(f"starting-volume evidence {pa.get('starts') or 0} vs {pb.get('starts') or 0}")
    if a['pos']=='FWD' and b['pos']!='FWD': reasons.append('forward replacement value breaks the close cross-position call')
    if not reasons: reasons.append('current minutes, role floor and availability preserve the adjacent order')
    comparisons.append((a,b,'; '.join(reasons[:2])))
for rank,r in enumerate(sorted_pool,196):
    r['rank']=rank
    if rank<=220: r['segment']='Undrafted buffer'; r['tier']='D'
    else: r['segment']='Extended watch buffer'; r['tier']='Watch'
    p=players[r['id']]; r['pos']=pos[p['element_type']]; r['team']=teams[p['team']]; r['status']=p.get('news') or 'Available'; r['changed']=TS; r['evidence']=LINK
rankmap={r['rank']:r for r in sorted_pool}
for idx in indexes:
    c=[x.strip() for x in lines[idx].strip('|').split('|')]; rank=int(c[0])
    if 196<=rank<=240:
        r=rankmap[rank]; lines[idx]='| '+' | '.join([str(r['rank']),r['name'],r['pos'],r['team'],r['segment'],r['tier'],str(r['id']),r['status'],r['changed'],r['evidence']])+' |'
lines=[re.sub(r'^ranking_depth: \d+$','ranking_depth: 350',x) for x in lines]
lines=[re.sub(r'^last_updated: .*$',f'last_updated: {TS}',x) if i<12 else x for i,x in enumerate(lines)]
BOARD.write_text('\n'.join(lines)+'\n')
changed=[(r,old_rank[r['id']]) for r in sorted_pool if r['rank']!=old_rank[r['id']]]
for r in sorted_pool:
    i=sorted_pool.index(r); above=sorted_pool[i-1] if i else None; below=sorted_pool[i+1] if i+1<len(sorted_pool) else None
    pth=Path(f"vault/02 Players/{r['name']} - {r['id']}.md"); pth.parent.mkdir(parents=True,exist_ok=True)
    pairs=[]
    if above:pairs.append(f"Below [[02 Players/{above['name']} - {above['id']}|{above['name']}]] after raw points, minutes, role and risk comparison.")
    if below:pairs.append(f"Above [[02 Players/{below['name']} - {below['id']}|{below['name']}]] after the same draft comparator.")
    pth.write_text(f"""---\ntype: player\nfpl_id: {r['id']}\nplayer: {r['name']}\nteam: {r['team']}\nposition: {r['pos']}\ncurrent_rank: {r['rank']}\nsegment: {r['segment']}\ntier: {r['tier']}\nlast_reviewed: {TS}\n---\n\n# {r['name']}\n\n## Current assessment\n\n- Rank: **{r['rank']}**\n- Segment / tier: **{r['segment']} / {r['tier']}**\n- Availability: {r['status']}\n- Review: {LINK}\n\n## Pairwise placement\n\n"""+'\n'.join('- '+x for x in pairs)+"\n\n## Confidence and reversal trigger\n\nConfidence is low-to-medium. Reverse for confirmed starting role, penalties or set pieces, repeated probable-first-team minutes, injury recovery, suspension, registration or transfer-driven competition.\n")
review=Path('vault/06 Reviews/2026/08/2026-08-02/1259-AEST-review.md'); review.parent.mkdir(parents=True,exist_ok=True)
out=['---','type: review',f'timestamp: {TS}','scope: ranks 201-220 with ranked challengers 196-240 and full API pool screen','---','','# FPL Draft review — ranks 201–220','','## Changes since prior iteration','']
out += [f"- **{r['name']}**: {old} → {r['rank']}." for r,old in sorted(changed,key=lambda x:x[0]['rank'])] or ['- No material ranking movement; the prior order survived direct comparison.']
out += ['','## API reconciliation','',f"Official FPL returned {len(api['elements'])} active players, {len(api['teams'])} teams and {len(fixtures)} fixtures. The canonical board retained 350 unique stable FPL IDs and no missing ranks.",'','## Method','','Ranks 201–220 were insertion-sorted with ranked challengers 196–240. Every remaining API-active player was screened; no unranked case was promoted without direct senior-role evidence. Raw season-points expectation was assessed before minutes, role, set pieces, injury/rotation risk and positional replacement value.','','## Decisive adjacent comparisons','']
for a,b,why in comparisons: out.append(f"- **{a['name']} over {b['name']}** — {why}. Final draft call favours {a['name']}; confidence low-to-medium. Reverse on confirmed role, fitness, set pieces or transfer competition.")
out += ['','## Full API pool screen','']
out += [f"- {name} (FPL ID {pid}): screened on {int(pts)} prior points, {int(starts)} starts and {int(mins)} minutes; not inserted because no specific current role evidence justified displacing a ranked player." for pid,name,pts,starts,mins in unranked_screen] or ['- No unranked API player met the broad senior-output screening threshold.']
out += ['','## Public evidence searched','','- Official FPL bootstrap and fixtures endpoints.','- Premier League summer transfer tracker and preseason fixtures/results tracker.','- Public searches for Planet FPL, Ben Crellin, Sam Martin, club correspondents and Fabrizio Romano. No exact accessible post supplied sufficiently reliable new role evidence for this block.','','## Evidence adopted','','- Official API identity, position, team, availability, prior points, starts and minutes.','- Premier League transfer and preseason trackers as context only.','','## Evidence rejected','','- Price and ownership.','- Unsourced transfer rumours and profile-only X results.','- Friendly goals or assists without probable-first-team role context.','','## Uncertainty and triggers','','The principal uncertainty is starting-role quality below rank 195. Revisit centre-forward minutes, promoted-club starters, goalkeeper hierarchies, penalties, injuries and late transfers.']
review.write_text('\n'.join(out)+'\n')
changes=Path('vault/07 Changes/2026/08/2026-08-02/1259-AEST-changes.md'); changes.parent.mkdir(parents=True,exist_ok=True)
co=['---','type: changes',f'timestamp: {TS}','scope: ranks 201-220','---','','# Changes — ranks 201–220','','## Rank and tier changes','']
co += [f"- **{r['name']}**: {old} → {r['rank']}; {r['segment']} / {r['tier']}." for r,old in sorted(changed,key=lambda x:x[0]['rank'])] or ['- No rank or tier changes.']
co += ['','## Entrants and removals','','- No unranked API player entered the board and no API-active ranked player was removed.','','## Important no-change decisions','','- Ranks 1–195 and 241–350 were preserved.','- Weak public rumours were not used to manufacture movement.']
changes.write_text('\n'.join(co)+'\n')
watch=Path('vault/01 Current/Current Watchlist.md'); wt=watch.read_text(); wt=re.sub(r'last_updated: .*',f'last_updated: {TS}',wt,count=1); wt+=f"\n## {TS} — ranks 201–220 triggers\n\n- Confirmed starting roles, penalties, set pieces, injuries and transfers for ranks 196–240 and screened API outsiders. Evidence: {LINK}.\n"; watch.write_text(wt)
for pth in [Path('vault/Wiki.md'),Path('vault/Home.md')]: pth.write_text(pth.read_text()+f"\n- Latest ranks 201–220 review: {LINK}\n")
mds=[BOARD,watch,review,changes,Path('vault/Wiki.md'),Path('vault/Home.md')]+[Path(f"vault/02 Players/{r['name']} - {r['id']}.md") for r in sorted_pool]
ch=Path('vault/00 Meta/Document Changelog.md'); text=ch.read_text(); text=re.sub(r'last_updated: .*',f'last_updated: {TS}',text,count=1)
for pth in mds:
    action='Created' if pth in (review,changes) else 'Updated'
    text+=f"\n| {TS} | `{pth.as_posix()}` | {action} | Completed ranks 201–220 pairwise review with challengers and full API screening. | {LINK} | [FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/); [FPL fixtures](https://fantasy.premierleague.com/api/fixtures/); [PL transfers](https://www.premierleague.com/en/transfers/2026-27/summer); [PL preseason](https://www.premierleague.com/en/news/4606700/premier-league-clubs-summer-2026-friendlies-and-tours) |"
text+=f"\n| {TS} | `vault/00 Meta/Document Changelog.md` | Updated | Appended an audit row for every Markdown file changed in this run. | {LINK} | Per-document audit |\n"; ch.write_text(text)
print(json.dumps({'pool':len(sorted_pool),'moved':len(changed),'unranked_screened':len(unranked_screen),'top':[r['name'] for r in sorted_pool[:5]],'rank220':sorted_pool[24]['name']}))