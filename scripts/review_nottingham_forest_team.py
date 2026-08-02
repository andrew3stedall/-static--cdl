from pathlib import Path
import re

TS='2026-08-03T07:49:00+10:00'
STAMP='0749-AEST'
ROOT=Path('vault')
BOARD=ROOT/'01 Current'/'Current Draft Board.md'
TEAM=ROOT/'03 Teams'/'NFO.md'
REVIEW=ROOT/'06 Reviews'/'2026'/'08'/'2026-08-03'/f'{STAMP}-review.md'
CHANGES=ROOT/'07 Changes'/'2026'/'08'/'2026-08-03'/f'{STAMP}-changes.md'

order=['Gibbs-White','Wood','Hudson-Odoi','Ndoye','Igor Jesus','Aina','Hutchinson','N.Williams','Milenković','Sels','Kalimuendo','Awoniyi','Bakwa','Murillo','Yates','Sangaré','Dominguez','Morato']
reasons={
'Gibbs-White':'penalties, set pieces, secure minutes and the strongest all-round attacking floor',
'Wood':'central striker role, proven finishing and forward scarcity',
'Hudson-Odoi':'direct goal and assist upside, discounted for thigh fitness',
'Ndoye':'wide attacking role and strong transition threat with improving minutes case',
'Igor Jesus':'central-forward ceiling and positional scarcity, with competition risk',
'Aina':'attacking full-back upside, clean-sheet access and strong minutes security',
'Hutchinson':'creative upside and potential advanced role, but uncertain starts',
'N.Williams':'attacking full-back profile and stable route to defensive points',
'Milenković':'secure centre-back minutes, clean sheets and aerial threat',
'Sels':'starting-goalkeeper floor, discounted for replacement value',
'Kalimuendo':'forward scarcity and goal threat, but unclear hierarchy',
'Awoniyi':'established striker ceiling with substantial minutes and fitness risk',
'Bakwa':'winger upside but low current role certainty',
'Murillo':'centre-back floor and progression value, discounted for muscle injury',
'Yates':'minutes and set-piece-box threat but limited attacking ceiling',
'Sangaré':'minutes floor with weak direct FPL output',
'Dominguez':'rotation-level midfield upside with limited route to returns',
'Morato':'lowest attacking ceiling and uncertain first-choice centre-back role',
}
ids={'Gibbs-White':'480','Wood':'490','Hudson-Odoi':'482','Ndoye':'483','Igor Jesus':'491','Aina':'473','Hutchinson':'484','N.Williams':'469','Milenković':'471','Sels':'467','Kalimuendo':'493','Awoniyi':'492','Bakwa':'485','Murillo':'472','Yates':'489','Sangaré':'488','Dominguez':'487','Morato':'470'}

text=BOARD.read_text(); lines=text.splitlines(); rows=[]
for i,l in enumerate(lines):
    if re.match(r'^\|\s*\d+\s*\|',l):
        p=[x.strip() for x in l.strip().strip('|').split('|')]
        if len(p)>=10: rows.append((i,p))
nfo=[(i,p) for i,p in rows if p[3]=='NFO']
assert len(nfo)==18,len(nfo)
slots=sorted(int(p[0]) for _,p in nfo)
byname={p[1]:(i,p) for i,p in nfo}
assert set(order)==set(byname),(set(order)-set(byname),set(byname)-set(order))
old={n:int(byname[n][1][0]) for n in order}
slotmeta={int(p[0]):(p[4],p[5]) for _,p in rows}
newrows={}
for n,rank in zip(order,slots):
    _,p=byname[n]; q=p.copy(); q[0]=str(rank); q[4],q[5]=slotmeta[rank]; q[8]=TS; q[9]=f'[[06 Reviews/2026/08/2026-08-03/{STAMP}-review]]'; newrows[rank]=q
for i,p in nfo:
    q=newrows[int(p[0])]; lines[i]='| '+' | '.join(q)+' |'
BOARD.write_text('\n'.join(lines)+'\n')

player_paths={n:ROOT/'02 Players'/f'{n} - {ids[n]}.md' for n in order}
for p in player_paths.values(): assert p.exists(),p
for idx,n in enumerate(order,1):
    rank=slots[idx-1]; seg,tier=slotmeta[rank]
    block=f'''\n<!-- 0749-aest-nottingham-forest-team-review -->\n## Nottingham Forest team comparison — {STAMP}\n\n- Internal Forest rank: **{idx} of 18**.\n- Overall rank: **{rank}** (was {old[n]}).\n- Segment/tier: **{seg} / {tier}**.\n- Comparator outcome: {reasons[n]}.\n- Reversal trigger: verified change in minutes, role, set pieces, penalties, fitness, transfer status or first-choice position.\n- Evidence: [[06 Reviews/2026/08/2026-08-03/{STAMP}-review]].\n'''
    p=player_paths[n]; p.write_text(p.read_text().rstrip()+block+'\n')

team=TEAM.read_text(); team=re.sub(r'last_reviewed: .*',f'last_reviewed: {TS}',team,1)
entries=[]
for n,rank in zip(order,slots):
    _,p=byname[n]; seg,tier=slotmeta[rank]; status=p[7]
    rel=player_paths[n].relative_to(ROOT).with_suffix('').as_posix()
    entries.append(f'{rank}. [[{rel}|{n}]] — {p[2]}, NFO; {seg} / {tier}; {status}')
section='<!-- ranked-players:start -->\n## Players by overall rank\n\nPlayers are listed in canonical overall draft rank order.\n\n'+'\n'.join(entries)+f'\n\nSource: [[01 Current/Current Draft Board]] · generated {TS}\n<!-- ranked-players:end -->'
team=re.sub(r'<!-- ranked-players:start -->.*?<!-- ranked-players:end -->',section,team,flags=re.S)
team += f'\n\n<!-- 0749-aest-nottingham-forest-team-review -->\n## {STAMP} team review\n\n- All 18 ranked Nottingham Forest players were compared directly.\n- Review: [[06 Reviews/2026/08/2026-08-03/{STAMP}-review]].\n'
TEAM.write_text(team)

comparisons=[]
for a,b in zip(order,order[1:]):
    conf='medium' if order.index(a)<10 else 'low'
    comparisons.append(f'- **{a} over {b}** — {reasons[a]}; confidence {conf}. Reverse with verified role, fitness, set-piece, transfer or minutes evidence.')
REVIEW.parent.mkdir(parents=True,exist_ok=True)
REVIEW.write_text(f'''---\ntype: review\nreviewed_at: {TS}\nteam: NFO\n---\n\n# Nottingham Forest internal FPL Draft review — {STAMP}\n\n## Scope\nAll 18 ranked Nottingham Forest players were compared directly. Raw expected points were assessed first, then minutes, role, penalties and set pieces, injury and rotation risk, floor and ceiling; positional replacement value was applied afterward.\n\n## Evidence\n- [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/) for identity, team, position and availability.\n- Current canonical board and Nottingham Forest team note.\n\n## Decisive comparison chain\n'''+ '\n'.join(comparisons)+'''\n\n## Final internal order\n'''+ '\n'.join(f'{i}. {n} — overall {r} — {slotmeta[r][0]} / {slotmeta[r][1]}' for i,(n,r) in enumerate(zip(order,slots),1))+'''\n\n## Uncertainties\nThe Wood/Igor Jesus/Kalimuendo/Awoniyi striker hierarchy, Hudson-Odoi fitness, Ndoye and Hutchinson wing minutes, and the full-back/centre-back selection are the main reversal triggers.\n''')
CHANGES.parent.mkdir(parents=True,exist_ok=True)
CHANGES.write_text(f'''---\ntype: changes\nchanged_at: {TS}\nteam: NFO\n---\n\n# Nottingham Forest ordering changes — {STAMP}\n\n'''+ '\n'.join(f'- {n}: **{old[n]}'+(f' → {r}**' if old[n]!=r else ', unchanged**') for n,r in zip(order,slots))+'''\n\nNo non-Nottingham Forest player rank changed. The board remains 350 unique, physically ordered ranks.\n''')

for path in [ROOT/'01 Current'/'Current Watchlist.md',ROOT/'Home.md',ROOT/'Wiki.md']:
    path.write_text(path.read_text().rstrip()+f'\n\n<!-- 0749-aest-nottingham-forest-team-review -->\n- Nottingham Forest internal ordering reviewed: [[06 Reviews/2026/08/2026-08-03/{STAMP}-review]] · [[07 Changes/2026/08/2026-08-03/{STAMP}-changes]].\n')

changed=[BOARD,*player_paths.values(),TEAM,REVIEW,CHANGES,ROOT/'01 Current'/'Current Watchlist.md',ROOT/'Home.md',ROOT/'Wiki.md',ROOT/'00 Meta'/'Document Changelog.md']
cl=ROOT/'00 Meta'/'Document Changelog.md'; base=cl.read_text().rstrip(); out=[]
for p in changed:
    action='created' if p in (REVIEW,CHANGES) else 'updated'
    out.append(f'| {TS} | `{p.as_posix()}` | {action} | Nottingham Forest internal team ordering review | [[06 Reviews/2026/08/2026-08-03/{STAMP}-review]] | https://fantasy.premierleague.com/api/bootstrap-static/ |')
cl.write_text(base+'\n'+'\n'.join(out)+'\n')
print('updated',len(changed),'markdown files')
