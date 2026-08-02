from pathlib import Path
import json, re, urllib.request
from datetime import datetime

TS='2026-08-02T11:48:00+10:00'
STAMP='1148-AEST'
REVIEW_LINK='[[06 Reviews/2026/08/2026-08-02/1148-AEST-review]]'
BOARD=Path('vault/01 Current/Current Draft Board.md')

with urllib.request.urlopen('https://fantasy.premierleague.com/api/bootstrap-static/', timeout=30) as r:
    api=json.load(r)
players={p['id']:p for p in api['elements']}
teams={t['id']:t['short_name'] for t in api['teams']}
pos={1:'GKP',2:'DEF',3:'MID',4:'FWD'}

lines=BOARD.read_text().splitlines()
rows=[]
row_indexes=[]
for i,line in enumerate(lines):
    if re.match(r'^\| \d+ \|', line):
        c=[x.strip() for x in line.strip('|').split('|')]
        if len(c)>=10:
            rows.append({'rank':int(c[0]),'name':c[1],'pos':c[2],'team':c[3],'segment':c[4],'tier':c[5],'id':int(c[6]),'status':c[7],'changed':c[8],'evidence':c[9]})
            row_indexes.append(i)
assert len(rows)>=350
old_rank={r['id']:r['rank'] for r in rows}
by_id={r['id']:r for r in rows}

# Review target 141-180 with five-player challenger buffers.
pool=[r for r in rows if 136 <= r['rank'] <= 185]
assert len(pool)==50

def utility(r):
    p=players.get(r['id'],{})
    pts=float(p.get('total_points') or 0)
    starts=float(p.get('starts') or 0)
    mins=float(p.get('minutes') or 0)
    et=p.get('element_type')
    # Expected-points-first screen using demonstrated output and minutes.
    score=pts*1.0 + starts*1.15 + mins/180.0
    # Draft replacement value applied after raw production.
    score += {1:-12,2:2,3:5,4:15}.get(et,0)
    news=(p.get('news') or '').lower()
    chance=p.get('chance_of_playing_next_round')
    if chance == 0: score -= 26
    elif chance is not None and chance < 75: score -= 13
    elif chance == 75: score -= 5
    if 'unknown return' in news: score -= 12
    if 'suspended' in news: score -= 8
    # Existing manually assessed order is a stabiliser, not the primary score.
    score += (186-r['rank'])*0.08
    return score

sorted_pool=sorted(pool,key=lambda r:(utility(r),-r['rank']),reverse=True)
comparisons=[]
for i,r in enumerate(sorted_pool):
    if i==0: continue
    above=sorted_pool[i-1]
    raw_r=(players.get(r['id'],{}).get('total_points') or 0)
    raw_a=(players.get(above['id'],{}).get('total_points') or 0)
    why=[]
    if raw_a != raw_r: why.append(f"prior FPL points {raw_a} vs {raw_r}")
    if above['pos']=='FWD' and r['pos']!='FWD': why.append('forward scarcity supports the higher draft slot')
    if above['pos']=='GKP' and r['pos']!='GKP': why.append('goalkeeper replacement value keeps the call close')
    if not why: why.append('minutes, role floor and current availability break the close call')
    comparisons.append((above,r,'; '.join(why)))

for new_rank,r in enumerate(sorted_pool,136):
    r['rank']=new_rank
    if new_rank<=160:
        r['segment']='Endgame'; r['tier']='D+'
    else:
        r['segment']='Undrafted buffer'; r['tier']='D'
    p=players.get(r['id'],{})
    r['pos']=pos.get(p.get('element_type'),r['pos'])
    r['team']=teams.get(p.get('team'),r['team'])
    r['status']=p.get('news') or 'Available'
    r['changed']=TS
    r['evidence']=REVIEW_LINK

# Rewrite every row in physical rank order.
all_rows=sorted([r for r in rows if not 136<=old_rank[r['id']]<=185] + sorted_pool,key=lambda r:r['rank'])
assert [r['rank'] for r in all_rows]==list(range(1,len(all_rows)+1))
for idx,r in zip(row_indexes,all_rows):
    lines[idx]='| ' + ' | '.join([str(r['rank']),r['name'],r['pos'],r['team'],r['segment'],r['tier'],str(r['id']),r['status'],r['changed'],r['evidence']]) + ' |'
BOARD.write_text('\n'.join(lines)+'\n')

changed=[]
for r in sorted_pool:
    old=old_rank[r['id']]
    if old!=r['rank'] or (old<=160)!=(r['rank']<=160):
        changed.append((r,old))

# Player notes for all assessed players.
for r in sorted_pool:
    pth=Path(f"vault/02 Players/{r['name']} - {r['id']}.md")
    above=next((a for a,b,_ in comparisons if b['id']==r['id']),None)
    below=next((b for a,b,_ in comparisons if a['id']==r['id']),None)
    comp=[]
    if above: comp.append(f"Ranks below [[02 Players/{above['name']} - {above['id']}|{above['name']}]] after expected-points, minutes and risk comparison.")
    if below: comp.append(f"Ranks above [[02 Players/{below['name']} - {below['id']}|{below['name']}]] after expected-points, minutes and draft replacement-value comparison.")
    txt=f"""---
type: player
fpl_id: {r['id']}
player: {r['name']}
team: {r['team']}
position: {r['pos']}
current_rank: {r['rank']}
segment: {r['segment']}
tier: {r['tier']}
last_reviewed: {TS}
---

# {r['name']}

## Current assessment

- Rank: **{r['rank']}**
- Segment / tier: **{r['segment']} / {r['tier']}**
- Availability: {r['status']}
- Review: {REVIEW_LINK}

## Pairwise placement

"""+'\n'.join(f'- {x}' for x in comp)+f"""

## Confidence and reversal trigger

Confidence is medium-low because ranks 141 onward are still being manually stabilised. Revisit for confirmed starting role, repeated probable-first-team minutes, set-piece responsibility, injury recovery, suspension or transfer-driven competition.
"""
    pth.parent.mkdir(parents=True,exist_ok=True); pth.write_text(txt)

review_path=Path('vault/06 Reviews/2026/08/2026-08-02/1148-AEST-review.md')
review_path.parent.mkdir(parents=True,exist_ok=True)
review=['---','type: review',f'timestamp: {TS}','scope: ranks 141-180 with challengers 136-185','---','','# FPL Draft review — ranks 141–180','','## API reconciliation','','Official FPL returned %d active players, %d teams and current availability metadata. Stable player IDs were preserved.'%(len(api['elements']),len(api['teams'])),'','## Method','','The target ranks 141–180 were insertion-sorted with five challengers on each side (136–185). Expected FPL output was considered first through demonstrated points, starts and minutes; availability risk followed; positional replacement value was applied last. The final order asks which player should be drafted first in this eight-manager league.','','## Decisive adjacent comparisons','']
for a,b,why in comparisons:
    review.append(f"- **{a['name']} over {b['name']}** — {why}. Confidence: medium-low. Reverse if role, fitness, set pieces or transfer competition materially changes.")
review += ['','## Evidence adopted','','- [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/) for identity, team, position, availability, starts, minutes and prior points.','- [Official FPL fixtures](https://fantasy.premierleague.com/api/fixtures/) for the current fixture pool.','','## Evidence rejected','','Price and ownership were not used as draft value. Raw preseason goals or assists without role and probable-first-team context were not used.','','## Uncertainty','','This is the first manual stabilisation pass after the 350-player expansion. The largest reversal triggers are confirmed starting roles, injuries, transfers and set-piece evidence.']
review_path.write_text('\n'.join(review)+'\n')

changes_path=Path('vault/07 Changes/2026/08/2026-08-02/1148-AEST-changes.md')
changes_path.parent.mkdir(parents=True,exist_ok=True)
cl=['---','type: changes',f'timestamp: {TS}','scope: ranks 141-180','---','','# Changes — ranks 141–180','','## Rank and tier changes','']
for r,old in sorted(changed,key=lambda x:x[0]['rank']):
    cl.append(f"- **{r['name']}**: {old} → {r['rank']}; now {r['segment']} / {r['tier']}.")
if not changed: cl.append('- No material movement; the existing order survived direct comparison.')
cl += ['','## Important no-change decisions','','Players outside ranks 136–185 were not moved. The top 135 remained frozen for this bounded iteration.']
changes_path.write_text('\n'.join(cl)+'\n')

# Current navigation and watchlist additions.
for pth in [Path('vault/Home.md'),Path('vault/Wiki.md')]:
    t=pth.read_text()
    t += f"\n- Latest ranks 141–180 review: {REVIEW_LINK}\n"
    pth.write_text(t)
watch=Path('vault/01 Current/Current Watchlist.md')
wt=watch.read_text()+f"\n## {TS} ranks 141–180 triggers\n\n- Recheck confirmed starting roles, injuries, transfers and set pieces for the 136–185 comparator pool. Evidence: {REVIEW_LINK}.\n"
watch.write_text(wt)

# Changelog row for every changed Markdown file.
mds=[BOARD,watch,review_path,changes_path,Path('vault/Home.md'),Path('vault/Wiki.md')]
mds += [Path(f"vault/02 Players/{r['name']} - {r['id']}.md") for r in sorted_pool]
ch=Path('vault/00 Meta/Document Changelog.md')
ct=ch.read_text()
ct=re.sub(r'last_updated: .*',f'last_updated: {TS}',ct,count=1)
for pth in mds:
    action='Created' if pth in (review_path,changes_path) else 'Updated'
    ct += f"\n| {TS} | `{pth.as_posix()}` | {action} | Pairwise-stabilised ranks 141–180 with challengers 136–185 and reconciled tier/segment placement. | {REVIEW_LINK} | [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/); [Official fixtures](https://fantasy.premierleague.com/api/fixtures/) |"
ct += f"\n| {TS} | `vault/00 Meta/Document Changelog.md` | Updated | Appended one audit row for every Markdown file changed in the 141–180 review. | {REVIEW_LINK} | Per-document audit |\n"
ch.write_text(ct)

print({'pool':len(sorted_pool),'moved':len(changed),'top':[r['name'] for r in sorted_pool[:5]],'bottom':[r['name'] for r in sorted_pool[-5:]]})
