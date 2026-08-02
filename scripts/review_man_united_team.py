from pathlib import Path
import re

TS='2026-08-03T00:42:00+10:00'
STAMP='0042-AEST'
ROOT=Path('vault')
BOARD=ROOT/'01 Current'/'Current Draft Board.md'
TEAM=ROOT/'03 Teams'/'MUN.md'
REVIEW=ROOT/'06 Reviews'/'2026'/'08'/'2026-08-03'/f'{STAMP}-review.md'
CHANGES=ROOT/'07 Changes'/'2026'/'08'/'2026-08-03'/f'{STAMP}-changes.md'
order=['B.Fernandes','Mbeumo','Cunha','Šeško','Amad','Dorgu','Rashford','Lammens','Maguire','Shaw','Dalot','Martinez','Mount','Mainoo','Zirkzee','Yoro','Mazraoui','Heaven','De Ligt','Tielemans','Darlow','Andrey Santos']
reasons={'B.Fernandes':'penalties, set pieces and the strongest secure raw-points projection','Mbeumo':'elite direct goal involvement and strong minutes outlook','Cunha':'central attacking role and high goal-assist ceiling','Šeško':'forward scarcity and central striker ceiling, discounted for fitness','Amad':'advanced role and chance creation with some rotation risk','Dorgu':'attacking wing-back upside and positional scarcity','Rashford':'proven scoring ceiling, heavily discounted for role uncertainty','Lammens':'starting-goalkeeper floor, discounted for replaceability','Maguire':'secure defensive minutes and aerial threat','Shaw':'attacking full-back upside with durability risk','Dalot':'minutes and attacking contribution, but role competition remains','Martinez':'passing and clean-sheet floor, discounted for injury','Mount':'attacking midfield ceiling but weak minutes certainty','Mainoo':'minutes and progression floor with limited direct FPL output','Zirkzee':'forward scarcity but unclear hierarchy and minutes','Yoro':'long-term centre-back ceiling with modest immediate attacking value','Mazraoui':'versatility and possible attacking role, but uncertain starts','Heaven':'development upside with low first-choice certainty','De Ligt':'centre-back floor heavily discounted by back injury','Tielemans':'current API assignment retained, but injury and role uncertainty dominate','Darlow':'backup-goalkeeper profile and current injury concern','Andrey Santos':'lowest current Manchester United role certainty in the canonical pool'}
text=BOARD.read_text(); lines=text.splitlines(); rows=[]
for i,l in enumerate(lines):
    if re.match(r'^\|\s*\d+\s*\|',l):
        p=[x.strip() for x in l.strip().strip('|').split('|')]
        if len(p)>=10: rows.append((i,p))
mun=[(i,p) for i,p in rows if p[3]=='MUN']; assert len(mun)==22
slots=sorted(int(p[0]) for _,p in mun); byname={p[1]:(i,p) for i,p in mun}; assert set(order)==set(byname)
old={n:int(byname[n][1][0]) for n in order}; slotmeta={int(p[0]):(p[4],p[5]) for _,p in rows}; newrows={}
for n,rank in zip(order,slots):
    _,p=byname[n]; q=p.copy(); q[0]=str(rank); q[4],q[5]=slotmeta[rank]; q[8]=TS; q[9]=f'[[06 Reviews/2026/08/2026-08-03/{STAMP}-review]]'; newrows[rank]=q
for i,p in mun: lines[i]='| '+' | '.join(newrows[int(p[0])])+' |'
BOARD.write_text('\n'.join(lines)+'\n')
player_paths={}
for n in order:
    fpl_id=byname[n][1][6]; p=ROOT/'02 Players'/f'{n} - {fpl_id}.md'; assert p.exists(),p; player_paths[n]=p
for idx,n in enumerate(order,1):
    rank=slots[idx-1]; seg,tier=slotmeta[rank]; p=player_paths[n]
    p.write_text(p.read_text().rstrip()+f'''\n<!-- 0042-aest-man-united-team-review -->\n## Manchester United team comparison — {STAMP}\n\n- Internal Manchester United rank: **{idx} of 22**.\n- Overall rank: **{rank}** (was {old[n]}).\n- Segment/tier: **{seg} / {tier}**.\n- Comparator outcome: {reasons[n]}.\n- Reversal trigger: verified change in minutes, role, penalties, set pieces, fitness, transfer status or first-choice position.\n- Evidence: [[06 Reviews/2026/08/2026-08-03/{STAMP}-review]].\n''')
team=TEAM.read_text(); team=re.sub(r'last_reviewed: .*',f'last_reviewed: {TS}',team,1); entries=[]
for n,rank in zip(order,slots):
    _,p=byname[n]; seg,tier=slotmeta[rank]; rel=player_paths[n].relative_to(ROOT).with_suffix('').as_posix(); entries.append(f'{rank}. [[{rel}|{n}]] — {p[2]}, MUN; {seg} / {tier}; {p[7]}')
section='<!-- ranked-players:start -->\n## Players by overall rank\n\nPlayers are listed in canonical overall draft rank order.\n\n'+'\n'.join(entries)+f'\n\nSource: [[01 Current/Current Draft Board]] · generated {TS}\n<!-- ranked-players:end -->'
team=re.sub(r'<!-- ranked-players:start -->.*?<!-- ranked-players:end -->',section,team,flags=re.S)+f'\n\n<!-- 0042-aest-man-united-team-review -->\n## {STAMP} team review\n\n- All 22 ranked Manchester United players were compared directly.\n- Review: [[06 Reviews/2026/08/2026-08-03/{STAMP}-review]].\n'; TEAM.write_text(team)
comparisons=[f'- **{a} over {b}** — {reasons[a]}; confidence {"medium" if order.index(a)<12 else "low"}. Reverse with verified role, fitness, set-piece, transfer or minutes evidence.' for a,b in zip(order,order[1:])]
REVIEW.parent.mkdir(parents=True,exist_ok=True); REVIEW.write_text(f'''---\ntype: review\nreviewed_at: {TS}\nteam: MUN\n---\n\n# Manchester United internal FPL Draft review — {STAMP}\n\n## Scope\nAll 22 ranked Manchester United players were compared directly. Raw expected points were assessed first, then minutes, role, penalties and set pieces, injury and rotation risk, floor and ceiling; positional replacement value was applied afterward.\n\n## Evidence\n- [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/) for identity, team, position and availability.\n- [Premier League fixture difficulty ratings](https://www.premierleague.com/en/news/4675493/get-the-fixture-difficulty-ratings-for-202627-fpl-season).\n- Current canonical board and Manchester United team note.\n\n## Decisive comparison chain\n'''+ '\n'.join(comparisons)+'\n\n## Final internal order\n'+ '\n'.join(f'{i}. {n} — overall {r} — {slotmeta[r][0]} / {slotmeta[r][1]}' for i,(n,r) in enumerate(zip(order,slots),1))+'\n\n## Uncertainties\nThe Šeško fitness assessment, Rashford role, first-choice wing-back pairing, goalkeeper hierarchy and the API team assignments for Tielemans, Darlow and Andrey Santos are the main reversal triggers.\n')
CHANGES.parent.mkdir(parents=True,exist_ok=True); CHANGES.write_text(f'''---\ntype: changes\nchanged_at: {TS}\nteam: MUN\n---\n\n# Manchester United ordering changes — {STAMP}\n\n'''+ '\n'.join(f'- {n}: **{old[n]}'+(f' → {r}**' if old[n]!=r else ', unchanged**') for n,r in zip(order,slots))+'\n\nNo non-Manchester United player rank changed. The board remains 350 unique, physically ordered ranks.\n')
for p in [ROOT/'01 Current'/'Current Watchlist.md',ROOT/'Home.md',ROOT/'Wiki.md']: p.write_text(p.read_text().rstrip()+f'\n\n<!-- 0042-aest-man-united-team-review -->\n- Manchester United internal ordering reviewed: [[06 Reviews/2026/08/2026-08-03/{STAMP}-review]] · [[07 Changes/2026/08/2026-08-03/{STAMP}-changes]].\n')
changed=[BOARD,*player_paths.values(),TEAM,REVIEW,CHANGES,ROOT/'01 Current'/'Current Watchlist.md',ROOT/'Home.md',ROOT/'Wiki.md',ROOT/'00 Meta'/'Document Changelog.md']; cl=ROOT/'00 Meta'/'Document Changelog.md'; base=cl.read_text().rstrip(); rows=[]
for p in changed:
    rows.append(f'| {TS} | `{p.as_posix()}` | {"created" if p in (REVIEW,CHANGES) else "updated"} | Manchester United internal team ordering review | [[06 Reviews/2026/08/2026-08-03/{STAMP}-review]] | https://fantasy.premierleague.com/api/bootstrap-static/ |')
cl.write_text(base+'\n'+'\n'.join(rows)+'\n'); print('updated',len(changed),'markdown files')
