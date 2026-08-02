from pathlib import Path
import re

TS='2026-08-03T08:30:00+10:00'
STAMP='0830-AEST'
ROOT=Path('vault')
BOARD=ROOT/'01 Current'/'Current Draft Board.md'
TEAM=ROOT/'03 Teams'/'SUN.md'
REVIEW=ROOT/'06 Reviews'/'2026'/'08'/'2026-08-03'/f'{STAMP}-review.md'
CHANGES=ROOT/'07 Changes'/'2026'/'08'/'2026-08-03'/f'{STAMP}-changes.md'

order=[
('E.Le Fée','542'),('Xhaka','544'),('Brobbey','552'),('Mukiele','533'),
('Roefs','529'),('Ballard','532'),('Adingra','546'),('Sadiki','545'),
('Hume','534'),('Alderete','535'),('Isidor','553'),('Talbi','549'),
('Diarra','543'),('Reinildo','536'),('Rigg','548'),("O'Nien",'539')]
reasons={
'E.Le Fée':'set pieces, advanced creation and the strongest attacking floor in the squad',
'Xhaka':'elite minutes security, set pieces and bonus-friendly involvement',
'Brobbey':'central-forward ceiling and forward scarcity, with adaptation risk',
'Mukiele':'attacking defender upside, clean-sheet route and strong minutes case',
'Roefs':'starting-goalkeeper floor, discounted for positional replaceability',
'Ballard':'secure centre-back minutes and aerial threat',
'Adingra':'direct winger ceiling, discounted for role and minutes uncertainty',
'Sadiki':'progressive midfield role and accumulation floor',
'Hume':'attacking full-back route but weaker team-level clean-sheet certainty',
'Alderete':'centre-back minutes and aerial floor with modest attacking ceiling',
'Isidor':'forward scarcity and scoring route, heavily discounted for hierarchy uncertainty',
'Talbi':'wide attacking upside but limited proven Premier League role security',
'Diarra':'minutes and progression value with limited direct FPL returns',
'Reinildo':'defensive minutes potential but minimal attacking ceiling',
'Rigg':'development upside with uncertain starts',
"O'Nien":'lowest attacking ceiling among the ranked Sunderland options',
}

text=BOARD.read_text()
lines=text.splitlines()
rows=[]
for i,l in enumerate(lines):
    if re.match(r'^\|\s*\d+\s*\|',l):
        parts=[p.strip() for p in l.strip().strip('|').split('|')]
        if len(parts)>=10: rows.append((i,parts))
sun=[(i,p) for i,p in rows if p[3]=='SUN']
assert len(sun)==16, len(sun)
slots=sorted(int(p[0]) for _,p in sun)
byid={p[6]:(i,p) for i,p in sun}
assert set(pid for _,pid in order)==set(byid), (set(pid for _,pid in order)-set(byid),set(byid)-set(pid for _,pid in order))
old={n:int(byid[pid][1][0]) for n,pid in order}
slotmeta={int(p[0]):(p[4],p[5]) for _,p in rows}
newrows={}
for (n,pid),rank in zip(order,slots):
    _,p=byid[pid]
    q=p.copy(); q[0]=str(rank); q[4],q[5]=slotmeta[rank]; q[8]=TS; q[9]=f'[[06 Reviews/2026/08/2026-08-03/{STAMP}-review]]'
    newrows[rank]=q
for i,p in sun:
    rank=int(p[0]); lines[i]='| '+' | '.join(newrows[rank])+' |'
BOARD.write_text('\n'.join(lines)+'\n')

player_paths={}
for n,pid in order:
    candidates=list((ROOT/'02 Players').glob(f'* - {pid}.md'))
    assert len(candidates)==1,(n,pid,candidates)
    player_paths[n]=candidates[0]
for idx,(n,pid) in enumerate(order,1):
    rank=slots[idx-1]; seg,tier=slotmeta[rank]
    block=f'''\n<!-- 0830-aest-sunderland-team-review -->\n## Sunderland team comparison — {STAMP}\n\n- Internal Sunderland rank: **{idx} of 16**.\n- Overall rank: **{rank}** (was {old[n]}).\n- Segment/tier: **{seg} / {tier}**.\n- Comparator outcome: {reasons[n]}.\n- Reversal trigger: verified change in minutes, role, set pieces, penalties, fitness, transfer status or first-choice position.\n- Evidence: [[06 Reviews/2026/08/2026-08-03/{STAMP}-review]].\n'''
    p=player_paths[n]; p.write_text(p.read_text().rstrip()+block+'\n')

team=TEAM.read_text()
team=re.sub(r'last_reviewed: .*',f'last_reviewed: {TS}',team,1)
entries=[]
for (n,pid),rank in zip(order,slots):
    _,p=byid[pid]; seg,tier=slotmeta[rank]; status=p[7]
    rel=player_paths[n].relative_to(ROOT).with_suffix('').as_posix()
    entries.append(f'{rank}. [[{rel}|{n}]] — {p[2]}, SUN; {seg} / {tier}; {status}')
section='<!-- ranked-players:start -->\n## Players by overall rank\n\nPlayers are listed in canonical overall draft rank order.\n\n'+'\n'.join(entries)+f'\n\nSource: [[01 Current/Current Draft Board]] · generated {TS}\n<!-- ranked-players:end -->'
team=re.sub(r'<!-- ranked-players:start -->.*?<!-- ranked-players:end -->',section,team,flags=re.S)
team += f'\n\n<!-- 0830-aest-sunderland-team-review -->\n## {STAMP} team review\n\n- All 16 ranked Sunderland players were compared directly.\n- Review: [[06 Reviews/2026/08/2026-08-03/{STAMP}-review]].\n'
TEAM.write_text(team)

comparisons=[]
for (a,_),(b,_) in zip(order,order[1:]):
    confidence='medium' if order.index((a,next(pid for n,pid in order if n==a)))<9 else 'low'
    comparisons.append(f'- **{a} over {b}** — {reasons[a]}; confidence {confidence}. Reverse with verified role, fitness, set-piece, transfer or minutes evidence.')
REVIEW.parent.mkdir(parents=True,exist_ok=True)
REVIEW.write_text(f'''---\ntype: review\nreviewed_at: {TS}\nteam: SUN\n---\n\n# Sunderland internal FPL Draft review — {STAMP}\n\n## Scope\nAll 16 ranked Sunderland players were compared directly. Raw expected points were assessed first, then minutes, role, penalties and set pieces, injury and rotation risk, floor and ceiling; positional replacement value was applied afterward.\n\n## Evidence\n- [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/) for identity, team, position and availability.\n- Current canonical board and Sunderland team note.\n\n## Decisive comparison chain\n'''+'\n'.join(comparisons)+'''\n\n## Final internal order\n'''+ '\n'.join(f'{i}. {n} — overall {r} — {slotmeta[r][0]} / {slotmeta[r][1]}' for i,((n,_),r) in enumerate(zip(order,slots),1))+'''\n\n## Uncertainties\nBrobbey and Isidor striker hierarchy, Adingra and Talbi wing minutes, and the full-back/centre-back selection pattern are the main reversal triggers.\n''')
CHANGES.parent.mkdir(parents=True,exist_ok=True)
CHANGES.write_text(f'''---\ntype: changes\nchanged_at: {TS}\nteam: SUN\n---\n\n# Sunderland ordering changes — {STAMP}\n\n'''+ '\n'.join(f'- {n}: **{old[n]}'+(f' → {r}**' if old[n]!=r else ', unchanged**') for (n,_),r in zip(order,slots))+'''\n\nNo non-Sunderland player rank changed. The board remains 350 unique, physically ordered ranks.\n''')

for path in [ROOT/'01 Current'/'Current Watchlist.md',ROOT/'Home.md',ROOT/'Wiki.md']:
    path.write_text(path.read_text().rstrip()+f'\n\n<!-- 0830-aest-sunderland-team-review -->\n- Sunderland internal ordering reviewed: [[06 Reviews/2026/08/2026-08-03/{STAMP}-review]] · [[07 Changes/2026/08/2026-08-03/{STAMP}-changes]].\n')

changed=[BOARD,*player_paths.values(),TEAM,REVIEW,CHANGES,ROOT/'01 Current'/'Current Watchlist.md',ROOT/'Home.md',ROOT/'Wiki.md',ROOT/'00 Meta'/'Document Changelog.md']
cl=ROOT/'00 Meta'/'Document Changelog.md'
base=cl.read_text().rstrip(); out=[]
for p in changed:
    action='created' if p in (REVIEW,CHANGES) else 'updated'
    out.append(f'| {TS} | `{p.as_posix()}` | {action} | Sunderland internal team ordering review | [[06 Reviews/2026/08/2026-08-03/{STAMP}-review]] | https://fantasy.premierleague.com/api/bootstrap-static/ |')
cl.write_text(base+'\n'+'\n'.join(out)+'\n')
print('updated',len(changed),'markdown files')
