from pathlib import Path
import re

TS='2026-08-01T23:00:00+10:00'
R='[[06 Reviews/2026/08/2026-08-01/2300-AEST-review]]'
C='[[07 Changes/2026/08/2026-08-01/2300-AEST-changes]]'
root=Path('vault')
players=[
('Sarr',208,'MID','CRY','Available','Evanilson','Sarr has the safer attacking-midfield minutes and multiple return routes.','medium'),
('Evanilson',79,'FWD','BOU','Available','Šeško','Evanilson has the cleaner current starting role; Šeško carries injury and competition risk.','medium'),
('Šeško',439,'FWD','MUN','Shin injury - 75% chance of playing','Welbeck','Šeško has the higher ceiling and forward scarcity despite the current injury flag.','low'),
('Welbeck',136,'FWD','BHA','Available','Minteh','Welbeck wins the close draft call through forward scarcity and a proven central role.','medium'),
('Minteh',122,'MID','BHA','Available','Wood','Minteh has the stronger pace-driven attacking ceiling; Wood has the safer veteran floor.','medium'),
('Wood',490,'FWD','NFO','Available','Woltemade','Wood has the clearer proven Premier League scoring floor.','medium'),
('Woltemade',463,'FWD','NEW','Available','Amad','Woltemade receives a forward-scarcity adjustment, but the comparison remains role-sensitive.','medium'),
('Amad',431,'MID','MUN','Available','Neto','Amad has the clearer route to a high-value attacking role if fit and starting.','medium'),
('Neto',156,'MID','CHE','Available','Kudus','Neto is preferred on current fitness and a slightly cleaner immediate role.','medium'),
('Kudus',512,'MID','TOT','Thigh injury - 75% chance of playing','Barnes','Kudus has the higher all-round ceiling, but the thigh issue keeps confidence low.','low'),
('Barnes',453,'MID','NEW','Available','Maddison','Barnes offers greater direct goal threat; Maddison has the stronger creative floor.','medium'),
('Maddison',515,'MID','TOT','Available','Pedro Porro','Maddison is expected to outscore the defender through set pieces and midfield returns.','medium'),
('Pedro Porro',499,'DEF','TOT','Available','James','Porro has the safer minutes and attacking-defender role.','medium'),
('James',142,'DEF','CHE','Available','Osula','James has the stronger per-start ceiling; Osula gains only a modest forward-scarcity adjustment.','medium'),
('Osula',465,'FWD','NEW','Available','Stach','Osula is drafted first because forward scarcity offsets Stach’s safer midfield floor.','medium'),
('Stach',335,'MID','LEE','Available','Anderson','Stach has the safer expected minutes and role.','medium'),
('Anderson',481,'MID','MCI','Available',"O'Reilly",'Anderson is preferred marginally on attacking upside, but both remain high-rotation risks.','low'),
("O'Reilly",387,'DEF','MCI','Available','Ampadu','O’Reilly has the higher ceiling; Ampadu has the safer floor.','low'),
('Ampadu',338,'MID','LEE','Available','Chalobah','Ampadu has more reliable midfield minutes and a clearer baseline.','medium'),
('Chalobah',143,'DEF','CHE','Available','next challenger','Chalobah remains outside the completed block because defender replacement is deep.','medium')]
rank={p[0]:49+i for i,p in enumerate(players)}
old={}
bp=root/'01 Current/Current Draft Board.md'
text=bp.read_text()
for m in re.finditer(r'^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|',text,re.M): old[m.group(2).strip()]=int(m.group(1))
for name,pid,pos,team,status,comp,decision,conf in players:
    nr=rank[name]; tier='B-' if nr<=64 else 'C+'
    pat=rf'^\|\s*\d+\s*\|\s*{re.escape(name)}\s*\|.*$'
    repl=f'| {nr} | {name} | {pos} | {team} | Core | {tier} | {pid} | {status} | {TS} | {R} |'
    text=re.sub(pat,repl,text,flags=re.M)
text=re.sub(r'last_updated: .*',f'last_updated: {TS}',text,1)
text=re.sub(r'status: .*','status: ranks49_64_pairwise_sorted',text,1)
text=text.replace('The first 48 have now been stable-sorted in three explicit player-versus-player blocks.','The first 64 have now been stable-sorted in four explicit player-versus-player blocks.')
bp.write_text(text)

for name,pid,pos,team,status,comp,decision,conf in players:
    posname={'FWD':'Forward','MID':'Midfielder','DEF':'Defender'}[pos]
    p=root/f'02 Players/{name} - {pid}.md'
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(f'''---
type: player
fpl_id: {pid}
player_name: {name}
team: "[[03 Teams/{team}]]"
position: "[[04 Positions/{posname}]]"
api_status: {status}
current_rank: {rank[name]}
current_segment: Core
last_reviewed: {TS}
---

# {name}

## Current assessment

Ranked {rank[name]} after the ranks 49–64 pairwise review. Expected season points were assessed before scarcity, then minutes, role, set pieces, injury and rotation risk.

## Pairwise placement

- Compared with: **{comp}**.
- Decision: {decision}
- Confidence: {conf}.
- Reversal trigger: confirmed starting role, fitness, penalties or material transfer evidence that changes the direct comparison.

## Evidence timeline

- 2026-08-01 23:00 AEST — Pairwise-reviewed and placed at rank {rank[name]}.
- [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/)
- [Official fixtures](https://fantasy.premierleague.com/api/fixtures/)
- [Premier League fixture difficulty](https://www.premierleague.com/en/news/4675493/get-the-fixture-difficulty-ratings-for-202627-fpl-season)

## Backlinks

- [[01 Current/Current Draft Board]]
- {R}
- {C}
''')

rows=''.join(f'| {rank[n]} | {n} | {comp} | {decision} | {conf} |\n' for n,pid,pos,team,status,comp,decision,conf in players)
review=root/'06 Reviews/2026/08/2026-08-01/2300-AEST-review.md'; review.parent.mkdir(parents=True,exist_ok=True)
review.write_text(f'''---
type: review
reviewed_at: {TS}
baseline: "[[06 Reviews/2026/08/2026-08-01/2254-AEST-review]]"
branch: codex/fpl-review-20260801-2300-ranks49-64
status: ranks49_64_pairwise_complete
---

# Ranks 49–64 pairwise sorting review

## Changes since the prior iteration

Sarr entered the block lead at 49. Evanilson, Šeško, Welbeck, Minteh and Wood were promoted ahead of lower-floor midfield and defender options. Stach, Anderson, O'Reilly and Ampadu were pushed below rank 64. No confirmed API removal was found in the assessed pool.

## Method

Stable insertion-style comparison was applied to prior ranks 45–68. Raw expected season points came first, followed by minutes, role, penalties and set pieces, injury and rotation risk, floor and ceiling. Positional replacement value was used only for close cross-position decisions.

## Pairwise decisions

| Rank | Player | Compared with | Decision | Confidence |
|---:|---|---|---|---|
{rows}
## Evidence adopted

- Sarr, Minteh, Amad and Barnes were favoured for direct attacking routes.
- Evanilson, Šeško, Welbeck, Wood, Woltemade and Osula received forward-scarcity adjustments only after raw-points assessment.
- Šeško and Kudus retain explicit injury discounts.
- Neto and James retain ceiling but carry Chelsea competition and availability risk.
- Pedro Porro remains the leading defender in this block because his attacking role and minutes are clearer.

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
move=''.join(f'| {n} | {old.get(n,"—")} | {rank[n]} | {rank[n]-old[n]:+d} |\n' for n,*_ in players)
changes.write_text(f'''---
type: changes
changed_at: {TS}
baseline: "[[07 Changes/2026/08/2026-08-01/2254-AEST-changes]]"
review: "{R}"
---

# Changes — ranks 49–64

| Player | Old rank | New rank | Change |
|---|---:|---:|---|
{move}
## Important no-change decisions

- No assessed player was removed from the active pool.
- Šeško and Kudus remain ranked but retain injury-risk labels.
- Manchester City and Chelsea squad membership did not override unresolved minutes risk.
''')

wp=root/'01 Current/Current Watchlist.md'
wp.write_text(wp.read_text()+f'''\n## 2026-08-01 23:00 AEST block triggers\n\n- Šeško — shin fitness and Manchester United striker hierarchy. {R}\n- Kudus — thigh fitness and Tottenham role. {R}\n- Neto / James — Chelsea starting and substitution patterns. {R}\n- Anderson / O'Reilly — Manchester City first-team minutes. {R}\n''')
for fn in ['Home.md','Wiki.md']:
    p=root/fn; t=p.read_text(); t=re.sub(r'latest_review: .*',f'latest_review: "{R}"',t,1); t=re.sub(r'latest_changes: .*',f'latest_changes: "{C}"',t,1); p.write_text(t+f'\n- 2026-08-01 23:00 AEST — ranks 49–64 pairwise review completed. {R}\n')
cp=root/'00 Meta/Document Changelog.md'; ct=cp.read_text(); ct=re.sub(r'last_updated: .*',f'last_updated: {TS}',ct,1)
paths=['vault/01 Current/Current Draft Board.md','vault/01 Current/Current Watchlist.md','vault/Home.md','vault/Wiki.md','vault/06 Reviews/2026/08/2026-08-01/2300-AEST-review.md','vault/07 Changes/2026/08/2026-08-01/2300-AEST-changes.md']+[f'vault/02 Players/{n} - {pid}.md' for n,pid,*_ in players]+['vault/00 Meta/Document Changelog.md']
for path in paths:
    action='Created' if '2300-AEST' in path else 'Updated'
    ct+=f'\n| {TS} | `{path}` | {action} | Recorded ranks 49–64 pairwise review evidence and placement. | {R} | [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/); [Official fixtures](https://fantasy.premierleague.com/api/fixtures/); [PL FDR](https://www.premierleague.com/en/news/4675493/get-the-fixture-difficulty-ratings-for-202627-fpl-season) |'
cp.write_text(ct+'\n')
Path('scripts/fpl_block_49_64.py').unlink(missing_ok=True)
Path('.github/workflows/fpl-block-49-64.yml').unlink(missing_ok=True)
