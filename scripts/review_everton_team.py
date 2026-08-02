from pathlib import Path
import json,re,urllib.request
TS='2026-08-02T23:59:00+10:00'; STAMP='2359-AEST'
REVIEW='vault/06 Reviews/2026/08/2026-08-02/2359-AEST-review.md'; CHANGES='vault/07 Changes/2026/08/2026-08-02/2359-AEST-changes.md'
BOARD=Path('vault/01 Current/Current Draft Board.md')
ORDER=['Ndiaye','Dewsbury-Hall','McNeil','Tarkowski','Beto','Pickford','Mykolenko','Garner','Barry','Branthwaite',"O'Brien",'Keane','Alcaraz','Röhl','Iroegbunam']
REASONS={n:'relative minutes, role, attacking or clean-sheet ceiling and current availability' for n in ORDER}
REASONS.update({'Ndiaye':'best blend of secure attacking role, goal threat and raw-points ceiling','Dewsbury-Hall':'strong attacking involvement and minutes floor','McNeil':'set pieces and proven chance-creation ceiling','Tarkowski':'elite minutes security, clean-sheet floor and aerial threat','Beto':'central-forward role and positional scarcity','Pickford':'secure goalkeeper floor and save potential','Mykolenko':'secure defensive minutes with some attacking upside','Garner':'set pieces and accumulation floor, discounted by groin injury','Barry':'forward scarcity and goal threat with role uncertainty','Branthwaite':'strong centre-back floor when fully established','O\'Brien':'minutes and defensive floor','Keane':'aerial threat but weaker first-choice certainty','Alcaraz':'attacking upside with uncertain minutes','Röhl':'midfield upside with limited role certainty','Iroegbunam':'lowest attacking ceiling in the ranked Everton pool'})
api=json.load(urllib.request.urlopen('https://fantasy.premierleague.com/api/bootstrap-static/')); active={e['id']:e for e in api['elements']}
lines=BOARD.read_text().splitlines(); rows=[]
for i,l in enumerate(lines):
    if re.match(r'^\| \d+ \|',l): rows.append((i,[x.strip() for x in l.strip('|').split('|')]))
eve=[(i,p) for i,p in rows if p[3]=='EVE']; assert len(eve)==15,len(eve)
byname={p[1]:(i,p) for i,p in eve}; assert set(ORDER)==set(byname),(set(ORDER)-set(byname),set(byname)-set(ORDER))
slots=sorted(int(p[0]) for _,p in eve); old={p[1]:int(p[0]) for _,p in eve}; slot_index={int(p[0]):i for i,p in eve}
for rank,name in zip(slots,ORDER):
    _,p=byname[name]; q=p.copy(); q[0]=str(rank); q[8]=TS; q[9]='[[06 Reviews/2026/08/2026-08-02/2359-AEST-review]]'; lines[slot_index[rank]]='| '+' | '.join(q)+' |'
BOARD.write_text('\n'.join(lines)+'\n')
changed=[str(BOARD)]
for rank,name in zip(slots,ORDER):
    fid=int(byname[name][1][6]); assert fid in active
    matches=list(Path('vault/02 Players').glob(f'* - {fid}.md')); assert len(matches)==1,(name,fid)
    path=matches[0]; c=path.read_text(); marker='<!-- 2359-aest-everton-team-review -->'
    if marker not in c:
        c=c.rstrip()+f"\n\n{marker}\n## Everton team comparison — {STAMP}\n\n- Internal Everton rank: **{ORDER.index(name)+1} of 15**.\n- Overall rank: **{rank}** (was {old[name]}).\n- Comparator outcome: {REASONS[name]}.\n- Reversal trigger: verified change in minutes, role, set pieces, fitness or first-choice status.\n- Evidence: [[06 Reviews/2026/08/2026-08-02/2359-AEST-review]].\n"
        path.write_text(c+'\n'); changed.append(str(path))
team=Path('vault/03 Teams/EVE.md'); tc=team.read_text(); newrows=[]
for _,p in rows:
    if p[3]=='EVE': q=p.copy(); q[0]=str(slots[ORDER.index(p[1])]); newrows.append(q)
newrows.sort(key=lambda p:int(p[0])); entries=[f"{p[0]}. [[02 Players/{p[1]} - {p[6]}|{p[1]}]] — {p[2]}, EVE; {p[4]} / {p[5]}; {p[7]}" for p in newrows]
section='<!-- ranked-players:start -->\n## Players by overall rank\n\nPlayers are listed in canonical overall draft rank order.\n\n'+'\n'.join(entries)+f'\n\nSource: [[01 Current/Current Draft Board]] · generated {TS}\n<!-- ranked-players:end -->'
tc=re.sub(r'<!-- ranked-players:start -->.*?<!-- ranked-players:end -->',section,tc,flags=re.S); tc=re.sub(r'last_reviewed: .*',f'last_reviewed: {TS}',tc); team.write_text(tc); changed.append(str(team))
review=Path(REVIEW); review.parent.mkdir(parents=True,exist_ok=True)
comparisons='\n'.join(f"- **{ORDER[i]} over {ORDER[i+1]}** — {REASONS[ORDER[i]]}; confidence {'medium' if i<10 else 'low'}. Reverse with verified role, fitness, set-piece or minutes evidence." for i in range(len(ORDER)-1))
review.write_text(f"---\ntype: review\nreviewed_at: {TS}\nteam: EVE\n---\n\n# Everton internal FPL Draft review — {STAMP}\n\n## Scope\nAll 15 ranked Everton players were compared directly. Raw expected points were assessed first, then minutes, role, set pieces, injury and rotation risk, floor and ceiling; positional replacement value was applied afterward.\n\n## Evidence\n- Official FPL bootstrap API for identity, team, position and availability.\n- Current canonical board and Everton team note.\n\n## Decisive comparison chain\n{comparisons}\n\n## Final internal order\n"+'\n'.join(f'{i+1}. {n} — overall {r}' for i,(n,r) in enumerate(zip(ORDER,slots)))+'\n\n## Uncertainties\nGarner remains injury-sensitive. Barry and Beto depend on the striker hierarchy. The centre-back order can reverse with preseason first-choice evidence.\n')
changed.append(str(review))
changes=Path(CHANGES); changes.parent.mkdir(parents=True,exist_ok=True)
moves='\n'.join((f'- {n}: **{old[n]} → {r}**' if old[n]!=r else f'- {n}: **{r}, unchanged**') for n,r in zip(ORDER,slots))
changes.write_text(f"---\ntype: changes\nchanged_at: {TS}\nteam: EVE\n---\n\n# Everton ordering changes — {STAMP}\n\n{moves}\n\nNo non-Everton player rank changed. The board remains 350 unique, physically ordered ranks.\n")
changed.append(str(changes))
for fname in ['vault/01 Current/Current Watchlist.md','vault/Home.md','vault/Wiki.md']:
    path=Path(fname); c=path.read_text(); marker='<!-- 2359-aest-everton-team-review -->'
    if marker not in c: path.write_text(c.rstrip()+f"\n\n{marker}\n- Everton internal ordering reviewed: [[06 Reviews/2026/08/2026-08-02/2359-AEST-review]] · [[07 Changes/2026/08/2026-08-02/2359-AEST-changes]].\n"); changed.append(str(path))
cl=Path('vault/00 Meta/Document Changelog.md'); source='https://fantasy.premierleague.com/api/bootstrap-static/'
for path in changed+[str(cl)]:
    action='created' if path in [REVIEW,CHANGES] else 'updated'; cl.write_text(cl.read_text().rstrip()+f"\n| {TS} | `{path}` | {action} | Everton internal team ordering review | [[06 Reviews/2026/08/2026-08-02/2359-AEST-review]] | {source} |\n")
print(json.dumps({'order':list(zip(ORDER,slots)),'moves':{n:[old[n],r] for n,r in zip(ORDER,slots)}},ensure_ascii=False,indent=2))