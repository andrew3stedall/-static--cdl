from pathlib import Path
import re

TS='2026-08-01T23:00:00+10:00'
STAMP='2300-AEST'
BRANCH='codex/fpl-review-20260801-2300-ranks49-64'
REVIEW='06 Reviews/2026/08/2026-08-01/2300-AEST-review'
REVIEW_LINK=f'[[{REVIEW}]]'
CHANGE_LINK='[[07 Changes/2026/08/2026-08-01/2300-AEST-changes]]'
root=Path('vault')
board_path=root/'01 Current/Current Draft Board.md'
text=board_path.read_text()
rows=[]
for line in text.splitlines():
    m=re.match(r'\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|',line)
    if m: rows.append({'rank':int(m.group(1)),'name':m.group(2).strip(),'pos':m.group(3).strip(),'team':m.group(4).strip(),'segment':m.group(5).strip(),'tier':m.group(6).strip(),'id':int(m.group(7)),'status':m.group(8).strip(),'line':line})
by_name={r['name']:r for r in rows}
order=['Sarr','Evanilson','Šeško','Welbeck','Minteh','Wood','Woltemade','Amad','Neto','Kudus','Barnes','Maddison','Pedro Porro','James','Osula','Stach','Anderson',"O'Reilly",'Ampadu','Chalobah']
comparators={
'Sarr':('Evanilson','Sarr has the safer attacking-midfield minutes and multiple return routes.'),
'Evanilson':('Šeško','Evanilson has the cleaner current starting role; Šeško carries injury and competition risk.'),
'Šeško':('Welbeck','Šeško has the higher ceiling and forward scarcity despite the current injury flag.'),
'Welbeck':('Minteh','Welbeck wins the close draft call through forward scarcity and a proven central role.'),
'Minteh':('Wood','Minteh has the stronger pace-driven attacking ceiling; Wood has the safer veteran floor.'),
'Wood':('Woltemade','Wood has the clearer proven Premier League scoring floor.'),
'Woltemade':('Amad','Woltemade receives a forward-scarcity adjustment, but the comparison remains role-sensitive.'),
'Amad':('Neto','Amad has the clearer route to a high-value attacking role if fit and starting.'),
'Neto':('Kudus','Neto is preferred on current fitness and a slightly cleaner immediate role.'),
'Kudus':('Barnes','Kudus has the higher all-round ceiling, but the thigh issue keeps confidence low.'),
'Barnes':('Maddison','Barnes offers greater direct goal threat; Maddison has the stronger creative floor.'),
'Maddison':('Pedro Porro','Maddison is expected to outscore the defender through set pieces and midfield returns.'),
'Pedro Porro':('James','Porro has the safer minutes and attacking-defender role.'),
'James':('Osula','James has the stronger per-start ceiling; Osula gains only a modest forward-scarcity adjustment.'),
'Osula':('Stach','Osula is drafted first because forward scarcity offsets Stach’s safer midfield floor.'),
'Stach':('Anderson','Stach has the safer expected minutes and role.'),
'Anderson':("O'Reilly",'Anderson is preferred marginally on attacking upside, but both remain high-rotation risks.'),
"O'Reilly":('Ampadu','O’Reilly has the higher ceiling; Ampadu has the safer floor.'),
'Ampadu':('Chalobah','Ampadu has more reliable midfield minutes and a clearer baseline.'),
'Chalobah':('next challenger','Chalobah remains outside the completed block because defender replacement is deep.')}
newrank={n:49+i for i,n in enumerate(order)}
lines=text.splitlines()
out=[]
for line in lines:
    m=re.match(r'\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|',line)
    if m and m.group(2).strip() in newrank:
        n=m.group(2).strip(); r=by_name[n]; nr=newrank[n]
        tier='B-' if nr<=64 else 'C+'
        seg='Core'
        line=f'| {nr} | {n} | {r["pos"]} | {r["team"]} | {seg} | {tier} | {r["id"]} | {r["status"]} | {TS} | {REVIEW_LINK} |'
    out.append(line)
text='\n'.join(out)+'\n'
text=re.sub(r'last_updated: .*',f'last_updated: {TS}',text,1)
text=re.sub(r'status: .*','status: ranks49_64_pairwise_sorted',text,1)
text=text.replace('The first 48 have now been stable-sorted in three explicit player-versus-player blocks.','The first 64 have now been stable-sorted in four explicit player-versus-player blocks.')
board_path.write_text(text)

# player notes
for n in order:
    r=by_name[n]; rank=newrank[n]; comp,decision=comparators[n]
    safe=n.replace('/','-')
    p=root/f'02 Players/{safe} - {r["id"]}.md'
    content=f'''---
type: player
fpl_id: {r['id']}
player_name: {n}
team: "[[03 Teams/{r['team']}]]"
position: "[[04 Positions/{'Forward' if r['pos']=='FWD' else 'Midfielder' if r['pos']=='MID' else 'Defender'}]]"
api_status: {r['status']}
current_rank: {rank}
current_segment: Core
last_reviewed: {TS}
---

# {n}

## Current assessment

Ranked {rank} after the ranks 49–64 pairwise review. Expected season points were assessed before scarcity, then minutes, role, set pieces, injury and rotation risk.

## Pairwise placement

- Compared with: **{comp}**.
- Decision: {decision}
- Confidence: {'low' if n in ['Šeško','Kudus','Anderson',"O'Reilly"] else 'medium'}.
- Reversal trigger: confirmed starting role, fitness, penalties or material transfer evidence that changes the direct comparison.

## Evidence timeline

- 2026-08-01 23:00 AEST — Pairwise-reviewed and placed at rank {rank}.
- [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/)
- [Official fixtures](https://fantasy.premierleague.com/api/fixtures/)
- [Premier League fixture difficulty](https://www.premierleague.com/en/news/4675493/get-the-fixture-difficulty-ratings-for-202627-fpl-season)

## Backlinks

- [[01 Current/Current Draft Board]]
- {REVIEW_LINK}
- {CHANGE_LINK}
'''
    p.parent.mkdir(parents=True,exist_ok=True); p.write_text(content)

review=root/'06 Reviews/2026/08/2026-08-01/2300-AEST-review.md'; review.parent.mkdir(parents=True,exist_ok=True)
review.write_text(f'''---
type: review
reviewed_at: {TS}
baseline: "[[06 Reviews/2026/08/2026-08-01/2254-AEST-review]]"
branch: {BRANCH}
status: ranks49_64_pairwise_complete
---

# Ranks 49–64 pairwise sorting review

## Changes since the prior iteration

Sarr entered the block lead at 49. Evanilson, Šeško, Welbeck, Minteh and Wood were promoted ahead of the prior lower-floor midfield and defender options. Stach, Anderson, O'Reilly and Ampadu were pushed below rank 64. No confirmed API removal was found in the assessed pool.

## Method

Stable insertion-style comparison was applied to prior ranks 45–68. Raw expected season points came first, followed by minutes, role, penalties and set pieces, injury and rotation risk, floor and ceiling. Positional replacement value was used only for close cross-position decisions.

## Pairwise decisions

| Rank | Player | Compared with | Decision | Confidence |
|---:|---|---|---|---|
'''+''.join(f'| {newrank[n]} | {n} | {comparators[n][0]} | {comparators[n][1]} | {'low' if n in ['Šeško','Kudus','Anderson',"O'Reilly"] else 'medium'} |\n' for n in order)+'''
## Evidence adopted

- Sarr, Minteh, Amad and Barnes were favoured for direct attacking routes.
- Evanilson, Šeško, Welbeck, Wood, Woltemade and Osula received forward-scarcity adjustments, but only after raw-points assessment.
- Šeško and Kudus retain explicit injury discounts.
- Neto and James retain ceiling but carry Chelsea competition and availability risk.
- Pedro Porro remains the leading defender in this block because attacking role and minutes are clearer than the alternatives.

Sources: [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/); [Official fixtures](https://fantasy.premierleague.com/api/fixtures/); [PL FDR](https://www.premierleague.com/en/news/4675493/get-the-fixture-difficulty-ratings-for-202627-fpl-season).

## Evidence rejected or limited

- Price and ownership were not used.
- Team strength was not accepted as proof of starts.
- Friendly output without probable-first-team role context was not used to force movement.
- No inaccessible X profile claim was treated as evidence.

## Uncertainties and reversal triggers

Šeško fitness, Tottenham's Kudus/Maddison roles, Chelsea's Neto/James minutes, Newcastle's forward hierarchy and Manchester City's Anderson/O'Reilly rotation can materially reorder this block.

## Next block

Sort ranks 65–80 with challengers from ranks 61–84.
''')
changes=root/'07 Changes/2026/08/2026-08-01/2300-AEST-changes.md'; changes.parent.mkdir(parents=True,exist_ok=True)
old={r['name']:r['rank'] for r in rows}
changes.write_text(f'''---
type: changes
changed_at: {TS}
baseline: "[[07 Changes/2026/08/2026-08-01/2254-AEST-changes]]"
review: "{REVIEW_LINK}"
---

# Changes — ranks 49–64

| Player | Old rank | New rank | Change |
|---|---:|---:|---|
'''+''.join(f'| {n} | {old[n]} | {newrank[n]} | {newrank[n]-old[n]:+d} |\n' for n in order)+'''
## Important no-change decisions

- No assessed player was removed from the active pool.
- Šeško and Kudus remain ranked but retain injury-risk labels.
- Manchester City and Chelsea squad membership did not override unresolved minutes risk.
''')

# Watchlist append
wp=root/'01 Current/Current Watchlist.md'; wt=wp.read_text();
wt += f'''\n## 2026-08-01 23:00 AEST block triggers\n\n- Šeško — shin fitness and Manchester United striker hierarchy. {REVIEW_LINK}\n- Kudus — thigh fitness and Tottenham role. {REVIEW_LINK}\n- Neto / James — Chelsea starting and substitution patterns. {REVIEW_LINK}\n- Anderson / O'Reilly — Manchester City first-team minutes. {REVIEW_LINK}\n'''; wp.write_text(wt)
# Home and Wiki latest links
for fn in ['Home.md','Wiki.md']:
    p=root/fn; t=p.read_text(); t=re.sub(r'latest_review: .*',f'latest_review: "{REVIEW_LINK}"',t,1); t=re.sub(r'latest_changes: .*',f'latest_changes: "{CHANGE_LINK}"',t,1)
    t += f'\n- 2026-08-01 23:00 AEST — ranks 49–64 pairwise review completed. {REVIEW_LINK}\n'; p.write_text(t)
# changelog
cp=root/'00 Meta/Document Changelog.md'; ct=cp.read_text(); ct=re.sub(r'last_updated: .*',f'last_updated: {TS}',ct,1)
paths=['vault/01 Current/Current Draft Board.md','vault/01 Current/Current Watchlist.md','vault/Home.md','vault/Wiki.md','vault/06 Reviews/2026/08/2026-08-01/2300-AEST-review.md','vault/07 Changes/2026/08/2026-08-01/2300-AEST-changes.md']+[f'vault/02 Players/{n} - {by_name[n]["id"]}.md' for n in order]
for path in paths+['vault/00 Meta/Document Changelog.md']:
    action='Created' if ('2300-AEST' in path or '02 Players' in path and not (root/path.removeprefix('vault/')).exists()) else 'Updated'
    ct += f'\n| {TS} | `{path}` | {action} | Recorded ranks 49–64 pairwise review evidence and placement. | {REVIEW_LINK} | [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/); [Official fixtures](https://fantasy.premierleague.com/api/fixtures/); [PL FDR](https://www.premierleague.com/en/news/4675493/get-the-fixture-difficulty-ratings-for-202627-fpl-season) |'
cp.write_text(ct+'\n')

# remove temporary files from net diff
Path('scripts/fpl_block_49_64.py').unlink(missing_ok=True)
Path('.github/workflows/fpl-block-49-64.yml').unlink(missing_ok=True)
