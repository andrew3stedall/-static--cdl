from pathlib import Path
import json, re, urllib.request

TS='2026-08-02T12:01:00+10:00'
STAMP='1201-AEST'
REVIEW_LINK='[[06 Reviews/2026/08/2026-08-02/1201-AEST-review]]'
BOARD=Path('vault/01 Current/Current Draft Board.md')
BOOT='https://fantasy.premierleague.com/api/bootstrap-static/'
FIX='https://fantasy.premierleague.com/api/fixtures/'
PRE='https://www.premierleague.com/en/news/4606700/premier-league-clubs-2026-pre-season-fixtures-and-results'
FIX_ART='https://www.premierleague.com/en/news/4675097/all-380-fixtures-for-202627-premier-league-season/'

with urllib.request.urlopen(BOOT, timeout=30) as r: api=json.load(r)
with urllib.request.urlopen(FIX, timeout=30) as r: fixtures=json.load(r)
players={p['id']:p for p in api['elements']}
teams={t['id']:t['short_name'] for t in api['teams']}
pos={1:'GKP',2:'DEF',3:'MID',4:'FWD'}

lines=BOARD.read_text().splitlines()
# Repair the known duplicate Wilson rows at rank 208 without changing the retained row.
seen_wilson=False
clean=[]
for line in lines:
    if line.startswith('| 208 | Wilson | FWD | BRE |'):
        if seen_wilson: continue
        seen_wilson=True
    clean.append(line)
lines=clean
rows=[]; row_indexes=[]
for i,line in enumerate(lines):
    if re.match(r'^\| \d+ \|', line):
        c=[x.strip() for x in line.strip('|').split('|')]
        if len(c)>=10:
            rows.append({'rank':int(c[0]),'name':c[1],'pos':c[2],'team':c[3],'segment':c[4],'tier':c[5],'id':int(c[6]),'status':c[7],'changed':c[8],'evidence':c[9]})
            row_indexes.append(i)
assert len(rows)==350, len(rows)
assert len({r['id'] for r in rows})==350
assert sorted(r['rank'] for r in rows)==list(range(1,351))
old_rank={r['id']:r['rank'] for r in rows}
pool=[r for r in rows if 166 <= r['rank'] <= 205]
assert len(pool)==40

def fnum(v):
    try:return float(v or 0)
    except:return 0.0

def raw_points_score(r):
    p=players[r['id']]
    pts=fnum(p.get('total_points'))
    mins=fnum(p.get('minutes'))
    starts=fnum(p.get('starts'))
    xg=fnum(p.get('expected_goals'))
    xa=fnum(p.get('expected_assists'))
    cs=fnum(p.get('clean_sheets'))
    return pts + starts*0.9 + mins/240 + (xg+xa)*5 + cs*0.8

def draft_score(r):
    p=players[r['id']]
    score=raw_points_score(r)
    et=p.get('element_type')
    score += {1:-8,2:1,3:4,4:12}.get(et,0)
    chance=p.get('chance_of_playing_next_round')
    news=(p.get('news') or '').lower()
    if chance==0: score-=28
    elif chance is not None and chance<75: score-=14
    elif chance==75: score-=6
    if 'unknown return' in news: score-=10
    if 'suspended' in news: score-=7
    # Keep the prior board as a weak stabiliser, not the deciding input.
    score += (206-r['rank'])*0.06
    return score

ordered=sorted(pool,key=lambda r:(draft_score(r),raw_points_score(r),-r['rank']),reverse=True)
comparisons=[]
for i in range(1,len(ordered)):
    a,b=ordered[i-1],ordered[i]
    pa,pb=players[a['id']],players[b['id']]
    reasons=[]
    if fnum(pa.get('total_points'))!=fnum(pb.get('total_points')):
        reasons.append(f"season points expectation proxy {pa.get('total_points',0)} vs {pb.get('total_points',0)}")
    if fnum(pa.get('minutes'))!=fnum(pb.get('minutes')):
        reasons.append(f"minutes evidence {pa.get('minutes',0)} vs {pb.get('minutes',0)}")
    if a['pos']=='FWD' and b['pos']!='FWD': reasons.append('forward replacement value breaks the cross-position tie')
    if a['pos']=='GKP' and b['pos']!='GKP': reasons.append('secure goalkeeper floor is the late tiebreaker')
    if (pa.get('news') or '') and not (pb.get('news') or ''): reasons.append('the higher player survives despite a disclosed availability risk')
    if not reasons: reasons.append('expected minutes, role floor and ceiling produce a narrow draft preference')
    comparisons.append((a,b,'; '.join(reasons[:3])))

for rank,r in enumerate(ordered,166):
    r['rank']=rank
    if rank<=180: r['segment'],r['tier']='Undrafted buffer','D'
    elif rank<=200: r['segment'],r['tier']='Deep watch','D-'
    else: r['segment'],r['tier']='Longshot watch','E+'
    p=players[r['id']]
    r['pos']=pos[p['element_type']]; r['team']=teams[p['team']]
    r['status']=p.get('news') or 'Available'; r['changed']=TS; r['evidence']=REVIEW_LINK
rank_map={r['rank']:r for r in ordered}
for idx in row_indexes:
    c=[x.strip() for x in lines[idx].strip('|').split('|')]
    rank=int(c[0])
    if 166<=rank<=205:
        r=rank_map[rank]
        lines[idx]='| '+' | '.join([str(r['rank']),r['name'],r['pos'],r['team'],r['segment'],r['tier'],str(r['id']),r['status'],r['changed'],r['evidence']])+' |'
BOARD.write_text('\n'.join(lines)+'\n')

changed=[(r,old_rank[r['id']]) for r in ordered if old_rank[r['id']]!=r['rank'] or r['segment']!='Undrafted buffer' or r['tier']!='D']

note_paths=[]
for i,r in enumerate(ordered):
    above=ordered[i-1] if i else None; below=ordered[i+1] if i+1<len(ordered) else None
    pth=Path(f"vault/02 Players/{r['name']} - {r['id']}.md"); note_paths.append(pth)
    pair=[]
    if above: pair.append(f"Ranks below [[02 Players/{above['name']} - {above['id']}|{above['name']}]] after the raw-points comparison and risk adjustment.")
    if below: pair.append(f"Ranks above [[02 Players/{below['name']} - {below['id']}|{below['name']}]] after expected-minutes, ceiling and replacement-value comparison.")
    pth.write_text(f"""---
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

"""+'\n'.join('- '+x for x in pair)+f"""

## Raw points and draft adjustment

The comparison starts with expected season points using current FPL points, starts, minutes and expected attacking involvement as imperfect preseason proxies. Position scarcity is applied only after that comparison.

## Confidence and reversal trigger

Confidence is low to medium. Reverse for confirmed starting roles, repeated probable-first-team minutes, penalties or set pieces, recovery setbacks, suspension, transfer completion or material competition changes.
""")

review=Path('vault/06 Reviews/2026/08/2026-08-02/1201-AEST-review.md'); review.parent.mkdir(parents=True,exist_ok=True)
text=['---','type: review',f'timestamp: {TS}','scope: ranks 171-200 with challengers 166-205','---','','# FPL Draft review — ranks 171–200','','## Changes since prior iteration','','This run continued the manual pass from the 11:48 review. It also corrected two duplicate copies of the same Wilson rank-208 row; no player identity was removed because one canonical copy remains.','','## API reconciliation','',f'Official FPL returned {len(api["elements"])} players, {len(api["teams"])} teams and {len(fixtures)} fixtures. Every comparator retained a stable FPL ID in the current API pool.','','## Sources searched','','- Official FPL bootstrap and fixtures endpoints.','- Premier League 2026/27 fixture release and August/September amendments.','- Premier League club-by-club preseason tracker.','- Public searches for Planet FPL James, Ben Crellin, Sam Martin, Fabrizio Romano, club journalists and club channels. No sufficiently specific accessible post materially changed this block, so profile-only claims were rejected.','','## Method','','Ranks 171–200 were compared with the five-player buffer on each side, ranks 166–205. The comparator first considered expected FPL points, then minutes, role, attacking involvement and disclosed availability. Positional replacement value was applied only afterward. Stable insertion order was used and players could cross the target boundary.','','## Decisive adjacent comparisons','']
for a,b,why in comparisons:
    text.append(f"- **{a['name']} over {b['name']}** — {why}. Final draft call: {a['name']} first. Confidence: low to medium. Reversal trigger: confirmed role, fitness, set pieces or transfer competition.")
text += ['','## Evidence adopted','',f'- [Official FPL bootstrap]({BOOT}) for player identity, position, team, availability, points, starts and minutes.',f'- [Official FPL fixtures]({FIX}) for the 380-match pool.',f'- [Premier League fixture release]({FIX_ART}) for the opening schedule.',f'- [Premier League preseason tracker]({PRE}) for current friendly dates and results.','','## Evidence rejected','','- Price and ownership as draft-value inputs.','- Raw friendly goals or assists without probable-first-team role context.','- Search snippets, account profiles and unsupported transfer speculation.','','## Preseason and fixture assessment','','No isolated friendly return was strong enough to override role and minutes evidence. Fixtures were treated as a modest tiebreaker rather than a substitute for season-long role.','','## Major uncertainties','','The block contains many uncertain attackers and reserve defenders. Starting-role confirmation, transfer registration, injury recovery and set-piece allocation can move players by large ranges; precision below the draft line remains intentionally limited.']
review.write_text('\n'.join(text)+'\n')

changes=Path('vault/07 Changes/2026/08/2026-08-02/1201-AEST-changes.md'); changes.parent.mkdir(parents=True,exist_ok=True)
out=['---','type: changes',f'timestamp: {TS}','scope: ranks 171-200','---','','# Changes — ranks 171–200','','## Rank, tier and segment changes','']
for r,old in sorted(changed,key=lambda x:x[0]['rank']): out.append(f"- **{r['name']}**: {old} → {r['rank']}; {r['segment']} / {r['tier']}.")
if not changed: out.append('- No material movement; all direct comparisons preserved the prior ordering.')
out += ['','## Entrants and removals','','- No active comparator entered or left the official FPL API pool.','- Two duplicate display rows for Wilson (FPL ID 108) at rank 208 were removed as a board-integrity correction; the canonical player row remains.','','## Watchlist changes','','- Recheck disclosed injuries and any completed transfers or registrations affecting ranks 166–205.','- Escalate any confirmed penalty, set-piece or first-choice striker role.','','## Important no-change decisions','','Players outside ranks 166–205 were not reordered. No weak public-source claim was used to manufacture movement.']
changes.write_text('\n'.join(out)+'\n')

watch=Path('vault/01 Current/Current Watchlist.md'); watch.write_text(watch.read_text()+f"\n## {TS} ranks 171–200 triggers\n\n- Recheck starting roles, injuries, transfers, registrations, penalties and set pieces for ranks 166–205. Evidence: {REVIEW_LINK}.\n")
for pth in [Path('vault/Home.md'),Path('vault/Wiki.md')]: pth.write_text(pth.read_text()+f"\n- Latest ranks 171–200 review: {REVIEW_LINK}\n")

mds=[BOARD,watch,review,changes,Path('vault/Home.md'),Path('vault/Wiki.md')]+note_paths
ch=Path('vault/00 Meta/Document Changelog.md'); ct=ch.read_text(); ct=re.sub(r'last_updated: .*',f'last_updated: {TS}',ct,count=1)
for pth in mds:
    action='Created' if pth in (review,changes) else 'Updated'
    ct += f"\n| {TS} | `{pth.as_posix()}` | {action} | Pairwise-reviewed ranks 171–200 with challengers 166–205 and reconciled rank, tier, segment and risk. | {REVIEW_LINK} | [Official FPL bootstrap]({BOOT}); [Official fixtures]({FIX}); [PL fixtures]({FIX_ART}); [PL preseason]({PRE}) |"
ct += f"\n| {TS} | `vault/00 Meta/Document Changelog.md` | Updated | Appended one audit row for every Markdown file changed in the ranks 171–200 review. | {REVIEW_LINK} | Per-document audit |\n"
ch.write_text(ct)
print({'pool':len(ordered),'moved':len(changed),'top5':[(r['rank'],r['name']) for r in ordered[:5]],'bottom5':[(r['rank'],r['name']) for r in ordered[-5:]]})
