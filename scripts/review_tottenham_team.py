from pathlib import Path
import re

TS='2026-08-03T08:35:00+10:00'
STAMP='0835-AEST'
ROOT=Path('vault')
BOARD=ROOT/'01 Current'/'Current Draft Board.md'
TEAM=ROOT/'03 Teams'/'TOT.md'
REVIEW=ROOT/'06 Reviews'/'2026'/'08'/'2026-08-03'/f'{STAMP}-review.md'
CHANGES=ROOT/'07 Changes'/'2026'/'08'/'2026-08-03'/f'{STAMP}-changes.md'

order=['Solanke','Kudus','Maddison','Pedro Porro','Richarlison','Fernandes','Tel','Romero','Vicario','Van de Ven','Senesi','Van Hecke','Xavi','Udogie','Spence','Gallagher','P.M.Sarr','Bergvall','Bentancur','Odobert','Gray','Danso','Robertson','Tonali','Kinsky','Dubravka']
reasons={
'Solanke':'clearest central-forward role, penalties possibility and strongest raw-points projection',
'Kudus':'elite ball-carrying and direct goal involvement, with a current thigh discount',
'Maddison':'set pieces and chance creation give the strongest midfield floor',
'Pedro Porro':'attacking-defender ceiling and positional scarcity',
'Richarlison':'central-forward scoring ceiling but weaker minutes security than Solanke',
'Fernandes':'creative midfield role and route to assists, while current team assignment needs monitoring',
'Tel':'high attacking ceiling and forward-like usage despite uncertain starts',
'Romero':'secure defensive minutes, clean sheets and aerial threat',
'Vicario':'starting-goalkeeper floor, discounted for replacement value',
'Van de Ven':'minutes and clean-sheet floor with some transition threat',
'Senesi':'aerial and set-piece threat, though current API assignment requires verification',
'Van Hecke':'reliable centre-back floor but limited direct attacking ceiling',
'Xavi':'high creative ceiling, heavily discounted for knee injury and role uncertainty',
'Udogie':'attacking full-back upside but uncertain durability and starts',
'Spence':'two-way full-back upside with rotation risk',
'Gallagher':'strong minutes and box-arrival floor but uncertain attacking responsibility',
'P.M.Sarr':'secure midfield role with moderate attacking upside',
'Bergvall':'development ceiling and progressive role, discounted for minutes uncertainty',
'Bentancur':'minutes floor but limited direct FPL output',
'Odobert':'winger upside, heavily discounted for knee injury',
'Gray':'versatility and minutes potential but low current attacking certainty',
'Danso':'centre-back floor with modest attacking value',
'Robertson':'experience and crossing upside but unclear role and API assignment',
'Tonali':'strong real-football role but limited direct FPL output and questionable assignment',
'Kinsky':'backup-goalkeeper profile',
'Dubravka':'lowest current first-choice certainty in the ranked Tottenham pool',
}

text=BOARD.read_text()
lines=text.splitlines()
rows=[]
for i,l in enumerate(lines):
    if re.match(r'^\|\s*\d+\s*\|',l):
        parts=[p.strip() for p in l.strip().strip('|').split('|')]
        if len(parts)>=10:
            rows.append((i,parts))
tot=[(i,p) for i,p in rows if p[3]=='TOT']
assert len(tot)==26, len(tot)
slots=sorted(int(p[0]) for _,p in tot)
byname={p[1]:(i,p) for i,p in tot}
assert set(order)==set(byname), (set(order)-set(byname),set(byname)-set(order))
old={n:int(byname[n][1][0]) for n in order}
slotmeta={int(p[0]):(p[4],p[5]) for _,p in rows}
newrows={}
for n,rank in zip(order,slots):
    _,p=byname[n]
    q=p.copy(); q[0]=str(rank); q[4],q[5]=slotmeta[rank]; q[8]=TS; q[9]=f'[[06 Reviews/2026/08/2026-08-03/{STAMP}-review]]'
    newrows[rank]=q
for i,p in tot:
    rank=int(p[0]); q=newrows[rank]; lines[i]='| '+' | '.join(q)+' |'
BOARD.write_text('\n'.join(lines)+'\n')

player_paths={}
for n in order:
    candidates=list((ROOT/'02 Players').glob(f'{n} - *.md'))
    assert len(candidates)==1,(n,candidates)
    player_paths[n]=candidates[0]
for idx,n in enumerate(order,1):
    rank=slots[idx-1]; seg,tier=slotmeta[rank]
    block=f'''\n<!-- 0835-aest-tottenham-team-review -->\n## Tottenham team comparison — {STAMP}\n\n- Internal Tottenham rank: **{idx} of 26**.\n- Overall rank: **{rank}** (was {old[n]}).\n- Segment/tier: **{seg} / {tier}**.\n- Comparator outcome: {reasons[n]}.\n- Reversal trigger: verified change in minutes, role, penalties, set pieces, fitness, transfer status or first-choice position.\n- Evidence: [[06 Reviews/2026/08/2026-08-03/{STAMP}-review]].\n'''
    p=player_paths[n]; p.write_text(p.read_text().rstrip()+block+'\n')

team=TEAM.read_text()
team=re.sub(r'last_reviewed: .*',f'last_reviewed: {TS}',team,1)
entries=[]
for n,rank in zip(order,slots):
    _,p=byname[n]; seg,tier=slotmeta[rank]; status=p[7]
    rel=player_paths[n].relative_to(ROOT).with_suffix('').as_posix()
    entries.append(f'{rank}. [[{rel}|{n}]] — {p[2]}, TOT; {seg} / {tier}; {status}')
section='<!-- ranked-players:start -->\n## Players by overall rank\n\nPlayers are listed in canonical overall draft rank order.\n\n'+'\n'.join(entries)+f'\n\nSource: [[01 Current/Current Draft Board]] · generated {TS}\n<!-- ranked-players:end -->'
team=re.sub(r'<!-- ranked-players:start -->.*?<!-- ranked-players:end -->',section,team,flags=re.S)
team += f'\n\n<!-- 0835-aest-tottenham-team-review -->\n## {STAMP} team review\n\n- All 26 ranked Tottenham players were compared directly.\n- Review: [[06 Reviews/2026/08/2026-08-03/{STAMP}-review]].\n'
TEAM.write_text(team)

comparisons=[]
for a,b in zip(order,order[1:]):
    confidence='medium' if order.index(a)<14 else 'low'
    comparisons.append(f'- **{a} over {b}** — {reasons[a]}; confidence {confidence}. Reverse with verified role, fitness, set-piece, transfer or minutes evidence.')
REVIEW.parent.mkdir(parents=True,exist_ok=True)
REVIEW.write_text(f'''---\ntype: review\nreviewed_at: {TS}\nteam: TOT\n---\n\n# Tottenham Hotspur internal FPL Draft review — {STAMP}\n\n## Scope\nAll 26 ranked Tottenham players were compared directly. Raw expected points were assessed first, then minutes, role, penalties and set pieces, injury and rotation risk, floor and ceiling; positional replacement value was applied afterward.\n\n## Evidence\n- [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/) for identity, team, position and availability.\n- Current canonical board and Tottenham team note.\n\n## Decisive comparison chain\n'''+'\n'.join(comparisons)+'''\n\n## Final internal order\n'''+ '\n'.join(f'{i}. {n} — overall {r} — {slotmeta[r][0]} / {slotmeta[r][1]}' for i,(n,r) in enumerate(zip(order,slots),1))+'''\n\n## Uncertainties\nThe Solanke/Richarlison striker split, Kudus fitness, Maddison and Xavi roles, full-back rotation, and current API assignments for Fernandes, Senesi, Van Hecke, Tonali and Dubravka are the main reversal triggers.\n''')
CHANGES.parent.mkdir(parents=True,exist_ok=True)
CHANGES.write_text(f'''---\ntype: changes\nchanged_at: {TS}\nteam: TOT\n---\n\n# Tottenham Hotspur ordering changes — {STAMP}\n\n'''+ '\n'.join(f'- {n}: **{old[n]}'+(f' → {r}**' if old[n]!=r else ', unchanged**') for n,r in zip(order,slots))+'''\n\nNo non-Tottenham player rank changed. The board remains 350 unique, physically ordered ranks.\n''')

for path in [ROOT/'01 Current'/'Current Watchlist.md',ROOT/'Home.md',ROOT/'Wiki.md']:
    path.write_text(path.read_text().rstrip()+f'\n\n<!-- 0835-aest-tottenham-team-review -->\n- Tottenham internal ordering reviewed: [[06 Reviews/2026/08/2026-08-03/{STAMP}-review]] · [[07 Changes/2026/08/2026-08-03/{STAMP}-changes]].\n')

changed=[BOARD,*player_paths.values(),TEAM,REVIEW,CHANGES,ROOT/'01 Current'/'Current Watchlist.md',ROOT/'Home.md',ROOT/'Wiki.md',ROOT/'00 Meta'/'Document Changelog.md']
cl=ROOT/'00 Meta'/'Document Changelog.md'
base=cl.read_text().rstrip()
rows=[]
for p in changed:
    action='created' if p in (REVIEW,CHANGES) else 'updated'
    rows.append(f'| {TS} | `{p.as_posix()}` | {action} | Tottenham internal team ordering review | [[06 Reviews/2026/08/2026-08-03/{STAMP}-review]] | https://fantasy.premierleague.com/api/bootstrap-static/ |')
cl.write_text(base+'\n'+'\n'.join(rows)+'\n')
print('updated',len(changed),'markdown files')
