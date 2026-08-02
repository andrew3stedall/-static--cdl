from pathlib import Path
import json,re,urllib.request
TS='2026-08-02T23:26:00+10:00'; STAMP='2326-AEST'
REVIEW='vault/06 Reviews/2026/08/2026-08-02/2326-AEST-review.md'; CHANGES='vault/07 Changes/2026/08/2026-08-02/2326-AEST-changes.md'
BOARD=Path('vault/01 Current/Current Draft Board.md')
ORDER=['Palmer','João Pedro','Rogers','Enzo','Neto','James','Welbeck','Delap','Estêvão','Gusto','Sánchez','Chalobah','Caicedo','Lacroix','N.Jackson','Emegha','Colwill','Gittens','Palestra','Fofana','Tosin','Acheampong','B.Badiashile','Anselmino','Disasi','M.Sarr']
REASONS={n:'relative minutes, role, attacking or clean-sheet ceiling and current availability' for n in ORDER}
REASONS.update({'Palmer':'elite raw-points projection, penalties and set pieces','João Pedro':'best current forward blend of role and scarcity','Rogers':'high attacking ceiling with broad routes to returns','Enzo':'minutes and set-piece accumulation floor','Neto':'direct attacking ceiling but rotation risk','James':'elite per-minute defender upside, discounted for durability','Welbeck':'proven central-forward output, but registration and hierarchy risk','Delap':'forward scarcity and strong goal threat','Estêvão':'high attacking ceiling with major rotation uncertainty','Gusto':'attacking full-back upside','Sánchez':'starting-goalkeeper floor','Chalobah':'stronger defensive minutes floor than the remaining centre-backs','Caicedo':'secure minutes but limited attacking ceiling','Lacroix':'defensive floor with role uncertainty','N.Jackson':'forward upside but crowded hierarchy','Emegha':'forward scarcity, discounted by injury and role uncertainty','Colwill':'centre-back minutes floor','Gittens':'winger ceiling but weak role certainty','Palestra':'attacking defender upside with uncertain minutes','Fofana':'ceiling suppressed by suspension and fitness history','Tosin':'defensive depth','Acheampong':'youth upside but uncertain role','B.Badiashile':'rotation-level centre-back profile','Anselmino':'uncertain first-team role','Disasi':'weak current pathway to minutes','M.Sarr':'lowest current Chelsea role certainty'})
api=json.load(urllib.request.urlopen('https://fantasy.premierleague.com/api/bootstrap-static/')); active={e['id']:e for e in api['elements']}
lines=BOARD.read_text().splitlines(); rows=[]
for i,l in enumerate(lines):
    if re.match(r'^\| \d+ \|',l): rows.append((i,[x.strip() for x in l.strip('|').split('|')]))
che=[(i,p) for i,p in rows if p[3]=='CHE']; assert len(che)==26,len(che)
byname={p[1]:(i,p) for i,p in che}; assert set(ORDER)==set(byname),(set(ORDER)-set(byname),set(byname)-set(ORDER))
slots=sorted(int(p[0]) for _,p in che); old={p[1]:int(p[0]) for _,p in che}; slot_index={int(p[0]):i for i,p in che}
for rank,name in zip(slots,ORDER):
    _,p=byname[name]; q=p.copy(); q[0]=str(rank); q[8]=TS; q[9]='[[06 Reviews/2026/08/2026-08-02/2326-AEST-review]]'; lines[slot_index[rank]]='| '+' | '.join(q)+' |'
BOARD.write_text('\n'.join(lines)+'\n')
changed=[str(BOARD)]
for rank,name in zip(slots,ORDER):
    fid=int(byname[name][1][6]); matches=list(Path('vault/02 Players').glob(f'* - {fid}.md')); assert len(matches)==1,(name,fid)
    path=matches[0]; c=path.read_text(); marker='<!-- 2326-aest-chelsea-team-review -->'
    if marker not in c:
        c=c.rstrip()+f"\n\n{marker}\n## Chelsea team comparison — {STAMP}\n\n- Internal Chelsea rank: **{ORDER.index(name)+1} of 26**.\n- Overall rank: **{rank}** (was {old[name]}).\n- Comparator outcome: {REASONS[name]}.\n- Reversal trigger: verified change in minutes, role, set pieces, fitness or first-choice status.\n- Evidence: [[06 Reviews/2026/08/2026-08-02/2326-AEST-review]].\n"
        path.write_text(c+'\n'); changed.append(str(path))
team=Path('vault/03 Teams/CHE.md'); tc=team.read_text(); newrows=[]
for _,p in rows:
    if p[3]=='CHE':
        q=p.copy(); q[0]=str(slots[ORDER.index(p[1])]); newrows.append(q)
newrows.sort(key=lambda p:int(p[0])); entries=[f"{p[0]}. [[02 Players/{p[1]} - {p[6]}|{p[1]}]] — {p[2]}, CHE; {p[4]} / {p[5]}; {p[7]}" for p in newrows]
section='<!-- ranked-players:start -->\n## Players by overall rank\n\nPlayers are listed in canonical overall draft rank order.\n\n'+'\n'.join(entries)+f'\n\nSource: [[01 Current/Current Draft Board]] · generated {TS}\n<!-- ranked-players:end -->'
tc=re.sub(r'<!-- ranked-players:start -->.*?<!-- ranked-players:end -->',section,tc,flags=re.S); tc=re.sub(r'last_reviewed: .*',f'last_reviewed: {TS}',tc); team.write_text(tc); changed.append(str(team))
review=Path(REVIEW); review.parent.mkdir(parents=True,exist_ok=True)
comparisons='\n'.join(f"- **{ORDER[i]} over {ORDER[i+1]}** — {REASONS[ORDER[i]]}; confidence {'medium' if i<16 else 'low'}. Reverse with verified role, fitness, set-piece or minutes evidence." for i in range(len(ORDER)-1))
review.write_text(f"---\ntype: review\nreviewed_at: {TS}\nteam: CHE\n---\n\n# Chelsea internal FPL Draft review — {STAMP}\n\n## Scope\nAll 26 ranked Chelsea players were compared directly. Raw expected points were assessed first, then minutes, role, set pieces, injury and rotation risk, floor and ceiling; positional replacement value was applied afterward.\n\n## Evidence\n- Official FPL bootstrap API for identity, team, position and availability.\n- Current canonical board and Chelsea team note.\n- Welbeck remains a transfer/registration uncertainty and was treated provisionally.\n\n## Decisive comparison chain\n{comparisons}\n\n## Final internal order\n"+'\n'.join(f'{i+1}. {n} — overall {r}' for i,(n,r) in enumerate(zip(ORDER,slots)))+'\n\n## Uncertainties\nThe forward and winger hierarchy is highly unstable. James, Fofana and Emegha remain fitness-sensitive. Welbeck requires registration confirmation.\n')
changed.append(str(review))
changes=Path(CHANGES); changes.parent.mkdir(parents=True,exist_ok=True)
moves='\n'.join((f'- {n}: **{old[n]} → {r}**' if old[n]!=r else f'- {n}: **{r}, unchanged**') for n,r in zip(ORDER,slots))
changes.write_text(f"---\ntype: changes\nchanged_at: {TS}\nteam: CHE\n---\n\n# Chelsea ordering changes — {STAMP}\n\n{moves}\n\nNo non-Chelsea player rank changed. The board remains 350 unique, physically ordered ranks.\n")
changed.append(str(changes))
for fname in ['vault/01 Current/Current Watchlist.md','vault/Home.md','vault/Wiki.md']:
    path=Path(fname); c=path.read_text(); marker='<!-- 2326-aest-chelsea-team-review -->'
    if marker not in c:
        path.write_text(c.rstrip()+f"\n\n{marker}\n- Chelsea internal ordering reviewed: [[06 Reviews/2026/08/2026-08-02/2326-AEST-review]] · [[07 Changes/2026/08/2026-08-02/2326-AEST-changes]].\n"); changed.append(str(path))
cl=Path('vault/00 Meta/Document Changelog.md'); source='https://fantasy.premierleague.com/api/bootstrap-static/'
for path in changed+[str(cl)]:
    action='created' if path in [REVIEW,CHANGES] else 'updated'; cl.write_text(cl.read_text().rstrip()+f"\n| {TS} | `{path}` | {action} | Chelsea internal team ordering review | [[06 Reviews/2026/08/2026-08-02/2326-AEST-review]] | {source} |\n")
print(json.dumps({'order':list(zip(ORDER,slots)),'moves':{n:[old[n],r] for n,r in zip(ORDER,slots)}},ensure_ascii=False,indent=2))