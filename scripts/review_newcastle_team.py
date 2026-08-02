from pathlib import Path
import re
TS='2026-08-03T07:41:00+10:00'; STAMP='0741-AEST'; ROOT=Path('vault')
BOARD=ROOT/'01 Current'/'Current Draft Board.md'; TEAM=ROOT/'03 Teams'/'NEW.md'
REVIEW=ROOT/'06 Reviews'/'2026'/'08'/'2026-08-03'/f'{STAMP}-review.md'; CHANGES=ROOT/'07 Changes'/'2026'/'08'/'2026-08-03'/f'{STAMP}-changes.md'
order=['Bruno G.','Barnes','Wissa','Woltemade','Elanga','J.Murphy','Hall','Livramento','Pope','Schär','Botman','Thiaw','Osula','Joelinton','J.Ramsey','Burn','L.Miley','Willock','Touré']
reasons={
'Bruno G.':'set pieces, secure minutes and the strongest all-round floor','Barnes':'proven direct goal threat and strong per-minute ceiling','Wissa':'central-forward scoring route and forward scarcity','Woltemade':'central attacking role and forward scarcity, with role uncertainty','Elanga':'pace, chance creation and direct attacking upside','J.Murphy':'established wide role and crossing output','Hall':'attacking full-back upside and defender scarcity','Livramento':'two-way full-back ceiling, discounted for calf fitness','Pope':'starting-goalkeeper floor, discounted for replaceability','Schär':'aerial and long-range threat with secure centre-back value','Botman':'clean-sheet floor and strong minutes when fit','Thiaw':'centre-back floor with modest attacking upside','Osula':'forward scarcity but weak current minutes certainty','Joelinton':'secure physical role but limited direct FPL ceiling and current thigh concern','J.Ramsey':'attacking midfield upside with uncertain starts','Burn':'minutes floor but low attacking ceiling','L.Miley':'development upside, discounted for leg injury','Willock':'attacking bursts but weak role certainty','Touré':'lowest current first-team role certainty in the ranked Newcastle pool'}
text=BOARD.read_text(); lines=text.splitlines(); rows=[]
for i,l in enumerate(lines):
    if re.match(r'^\|\s*\d+\s*\|',l):
        p=[x.strip() for x in l.strip().strip('|').split('|')]
        if len(p)>=10: rows.append((i,p))
teamrows=[(i,p) for i,p in rows if p[3]=='NEW']; assert len(teamrows)==19,len(teamrows)
slots=sorted(int(p[0]) for _,p in teamrows); by={p[1]:(i,p) for i,p in teamrows}; assert set(order)==set(by),(set(order)-set(by),set(by)-set(order))
old={n:int(by[n][1][0]) for n in order}; slotmeta={int(p[0]):(p[4],p[5]) for _,p in rows}; new={}
for n,r in zip(order,slots):
    _,p=by[n]; q=p.copy(); q[0]=str(r); q[4],q[5]=slotmeta[r]; q[8]=TS; q[9]=f'[[06 Reviews/2026/08/2026-08-03/{STAMP}-review]]'; new[r]=q
for i,p in teamrows: lines[i]='| '+' | '.join(new[int(p[0])])+' |'
BOARD.write_text('\n'.join(lines)+'\n')
player_paths={}
for n in order:
    fid=by[n][1][6]; c=list((ROOT/'02 Players').glob(f'* - {fid}.md')); assert len(c)==1,(n,fid,c); player_paths[n]=c[0]
for idx,(n,r) in enumerate(zip(order,slots),1):
    seg,tier=slotmeta[r]; p=player_paths[n]
    p.write_text(p.read_text().rstrip()+f'''\n\n<!-- 0741-aest-newcastle-team-review -->\n## Newcastle team comparison — {STAMP}\n\n- Internal Newcastle rank: **{idx} of 19**.\n- Overall rank: **{r}** (was {old[n]}).\n- Segment/tier: **{seg} / {tier}**.\n- Comparator outcome: {reasons[n]}.\n- Reversal trigger: verified change in minutes, role, set pieces, penalties, fitness, transfer status or first-choice position.\n- Evidence: [[06 Reviews/2026/08/2026-08-03/{STAMP}-review]].\n''')
team=TEAM.read_text(); team=re.sub(r'last_reviewed: .*',f'last_reviewed: {TS}',team,1)
entries=[]
for n,r in zip(order,slots):
    p=by[n][1]; seg,tier=slotmeta[r]; rel=player_paths[n].relative_to(ROOT).with_suffix('').as_posix(); entries.append(f'{r}. [[{rel}|{n}]] — {p[2]}, NEW; {seg} / {tier}; {p[7]}')
section='<!-- ranked-players:start -->\n## Players by overall rank\n\nPlayers are listed in canonical overall draft rank order.\n\n'+'\n'.join(entries)+f'\n\nSource: [[01 Current/Current Draft Board]] · generated {TS}\n<!-- ranked-players:end -->'
team=re.sub(r'<!-- ranked-players:start -->.*?<!-- ranked-players:end -->',section,team,flags=re.S)
team += f'\n\n<!-- 0741-aest-newcastle-team-review -->\n## {STAMP} team review\n\n- All 19 ranked Newcastle players were compared directly.\n- Review: [[06 Reviews/2026/08/2026-08-03/{STAMP}-review]].\n'; TEAM.write_text(team)
REVIEW.parent.mkdir(parents=True,exist_ok=True); CHANGES.parent.mkdir(parents=True,exist_ok=True)
comparisons='\n'.join(f'- **{a} over {b}** — {reasons[a]}; confidence {"medium" if i<11 else "low"}. Reverse with verified role, fitness, set-piece, transfer or minutes evidence.' for i,(a,b) in enumerate(zip(order,order[1:])))
REVIEW.write_text(f'''---\ntype: review\nreviewed_at: {TS}\nteam: NEW\n---\n\n# Newcastle United internal FPL Draft review — {STAMP}\n\n## Scope\nAll 19 ranked Newcastle players were compared directly. Raw expected points were assessed first, then minutes, role, set pieces, injury and rotation risk, floor and ceiling; positional replacement value was applied afterward.\n\n## Evidence\n- [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/) for identity, team, position and availability.\n- Current canonical board and Newcastle team note.\n\n## Decisive comparison chain\n{comparisons}\n\n## Final internal order\n'''+ '\n'.join(f'{i}. {n} — overall {r} — {slotmeta[r][0]} / {slotmeta[r][1]}' for i,(n,r) in enumerate(zip(order,slots),1))+'''\n\n## Uncertainties\nThe Wissa/Woltemade striker hierarchy, Elanga and Murphy wing minutes, Hall/Livramento fitness, and centre-back selection are the main reversal triggers.\n''')
CHANGES.write_text(f'''---\ntype: changes\nchanged_at: {TS}\nteam: NEW\n---\n\n# Newcastle United ordering changes — {STAMP}\n\n'''+ '\n'.join(f'- {n}: **{old[n]}'+(f' → {r}**' if old[n]!=r else ', unchanged**') for n,r in zip(order,slots))+'''\n\nNo non-Newcastle player rank changed. The board remains 350 unique, physically ordered ranks.\n''')
for path in [ROOT/'01 Current'/'Current Watchlist.md',ROOT/'Home.md',ROOT/'Wiki.md']:
    path.write_text(path.read_text().rstrip()+f'\n\n<!-- 0741-aest-newcastle-team-review -->\n- Newcastle United internal ordering reviewed: [[06 Reviews/2026/08/2026-08-03/{STAMP}-review]] · [[07 Changes/2026/08/2026-08-03/{STAMP}-changes]].\n')
changed=[BOARD,*player_paths.values(),TEAM,REVIEW,CHANGES,ROOT/'01 Current'/'Current Watchlist.md',ROOT/'Home.md',ROOT/'Wiki.md',ROOT/'00 Meta'/'Document Changelog.md']
cl=ROOT/'00 Meta'/'Document Changelog.md'; base=cl.read_text().rstrip(); out=[]
for p in changed:
    action='created' if p in (REVIEW,CHANGES) else 'updated'; out.append(f'| {TS} | `{p.as_posix()}` | {action} | Newcastle United internal team ordering review | [[06 Reviews/2026/08/2026-08-03/{STAMP}-review]] | https://fantasy.premierleague.com/api/bootstrap-static/ |')
cl.write_text(base+'\n'+'\n'.join(out)+'\n'); print('updated',len(changed),'markdown files')
