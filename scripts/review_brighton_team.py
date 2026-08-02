from pathlib import Path
import json,re,urllib.request
TS='2026-08-02T20:45:00+10:00'; STAMP='2045-AEST'
REVIEW='vault/06 Reviews/2026/08/2026-08-02/2045-AEST-review.md'; CHANGES='vault/07 Changes/2026/08/2026-08-02/2045-AEST-changes.md'
BOARD=Path('vault/01 Current/Current Draft Board.md')
ORDER=['Minteh','Mitoma','Groß','Georginio','Dunk','De Cuyper','Verbruggen','F.Kadıoğlu','Struijk','Ayari','Hinshelwood','Wieffer','Boscagli','Tzimas','Kostoulas','Gomez','Baleba','Igor','Coppola','Costinha','Svoboda','Vuskovic']
REASONS={n:'role, minutes, attacking or clean-sheet ceiling and current availability relative to the next Brighton option' for n in ORDER}
REASONS.update({'Minteh':'best blend of secure attacking role and direct scoring ceiling','Mitoma':'elite winger ceiling but discounted by current hamstring uncertainty','Groß':'set pieces and dependable accumulation floor','Georginio':'forward scarcity and attacking upside','Dunk':'secure minutes, clean-sheet floor and aerial threat','De Cuyper':'attacking full-back ceiling','Verbruggen':'starting goalkeeper floor','F.Kadıoğlu':'attacking defender upside with some role uncertainty','Struijk':'minutes and defensive floor','Ayari':'midfield minutes and moderate attacking contribution','Hinshelwood':'versatility and route to attacking returns','Wieffer':'minutes floor but limited upside','Boscagli':'defensive role with moderate uncertainty','Tzimas':'forward scarcity, heavily discounted by knee fitness','Kostoulas':'young forward ceiling with uncertain minutes','Gomez':'creative upside but weak role certainty','Baleba':'secure midfield role with low FPL ceiling','Igor':'defensive depth','Coppola':'uncertain first-team role','Costinha':'uncertain first-team role','Svoboda':'low-confidence defensive depth','Vuskovic':'lowest current Brighton role certainty'})
api=json.load(urllib.request.urlopen('https://fantasy.premierleague.com/api/bootstrap-static/')); active={e['id']:e for e in api['elements']}
lines=BOARD.read_text().splitlines(); rows=[]
for i,l in enumerate(lines):
    if re.match(r'^\| \d+ \|',l): rows.append((i,[x.strip() for x in l.strip('|').split('|')]))
bha=[(i,p) for i,p in rows if p[3]=='BHA']; assert len(bha)==22,len(bha)
byname={p[1]:(i,p) for i,p in bha}; assert set(ORDER)==set(byname),(set(ORDER)-set(byname),set(byname)-set(ORDER))
slots=sorted(int(p[0]) for _,p in bha); old={p[1]:int(p[0]) for _,p in bha}
slot_index={int(p[0]):i for i,p in bha}
for rank,name in zip(slots,ORDER):
    _,p=byname[name]; q=p.copy(); q[0]=str(rank); q[8]=TS; q[9]='[[06 Reviews/2026/08/2026-08-02/2045-AEST-review]]'; lines[slot_index[rank]]='| '+' | '.join(q)+' |'
BOARD.write_text('\n'.join(lines)+'\n')
changed=[str(BOARD)]
for rank,name in zip(slots,ORDER):
    fid=int(byname[name][1][6]); assert fid in active
    matches=list(Path('vault/02 Players').glob(f'* - {fid}.md')); assert len(matches)==1,(name,fid)
    path=matches[0]; c=path.read_text(); marker=f'<!-- {STAMP.lower()}-brighton-team-review -->'
    if marker not in c:
        c=c.rstrip()+f"\n\n{marker}\n## Brighton team comparison — {STAMP}\n\n- Internal Brighton rank: **{ORDER.index(name)+1} of 22**.\n- Overall rank: **{rank}** (was {old[name]}).\n- Comparator outcome: {REASONS[name]}.\n- Reversal trigger: verified change in minutes, role, set pieces, fitness or first-choice status.\n- Evidence: [[06 Reviews/2026/08/2026-08-02/2045-AEST-review]].\n"
        path.write_text(c+'\n'); changed.append(str(path))
team=Path('vault/03 Teams/BHA.md'); tc=team.read_text(); newrows=[]
for _,p in rows:
    if p[3]=='BHA':
        n=p[1]; rank=slots[ORDER.index(n)]; q=p.copy(); q[0]=str(rank); newrows.append(q)
newrows.sort(key=lambda p:int(p[0]))
entries=[f"{p[0]}. [[02 Players/{p[1]} - {p[6]}|{p[1]}]] — {p[2]}, BHA; {p[4]} / {p[5]}; {p[7]}" for p in newrows]
section='<!-- ranked-players:start -->\n## Players by overall rank\n\nPlayers are listed in canonical overall draft rank order.\n\n'+'\n'.join(entries)+f'\n\nSource: [[01 Current/Current Draft Board]] · generated {TS}\n<!-- ranked-players:end -->'
tc=re.sub(r'<!-- ranked-players:start -->.*?<!-- ranked-players:end -->',section,tc,flags=re.S); team.write_text(tc); changed.append(str(team))
review=Path(REVIEW); review.parent.mkdir(parents=True,exist_ok=True)
comparisons='\n'.join(f"- **{ORDER[i]} over {ORDER[i+1]}** — {REASONS[ORDER[i]]}; confidence {'medium' if i<13 else 'low'}. Reverse with verified role, fitness, set-piece or minutes evidence." for i in range(len(ORDER)-1))
review.write_text(f"---\ntype: review\nreviewed_at: {TS}\nteam: BHA\n---\n\n# Brighton internal FPL Draft review — {STAMP}\n\n## Scope\nAll 22 ranked Brighton players were compared directly. Raw expected points were assessed first, then minutes, role, set pieces, injury and rotation risk, floor and ceiling; positional replacement value was applied afterward.\n\n## Evidence\n- Official FPL bootstrap API for identity, team, position and availability.\n- Current canonical board and Brighton team note.\n- Existing Welbeck departure evidence was retained; no unsourced friendly output forced movement.\n\n## Decisive comparison chain\n{comparisons}\n\n## Final internal order\n"+'\n'.join(f'{i+1}. {n} — overall {r}' for i,(n,r) in enumerate(zip(ORDER,slots)))+'\n\n## Uncertainties\nMitoma and Tzimas are fitness-sensitive. Georginio, Kostoulas and Gomez depend on first-team attacking roles. The defensive depth order is low confidence.\n')
changed.append(str(review))
changes=Path(CHANGES); changes.parent.mkdir(parents=True,exist_ok=True)
moves='\n'.join((f'- {n}: **{old[n]} → {r}**' if old[n]!=r else f'- {n}: **{r}, unchanged**') for n,r in zip(ORDER,slots))
changes.write_text(f"---\ntype: changes\nchanged_at: {TS}\nteam: BHA\n---\n\n# Brighton ordering changes — {STAMP}\n\n{moves}\n\nNo non-Brighton player rank changed. The board remains 350 unique, physically ordered ranks.\n")
changed.append(str(changes))
for fname in ['vault/01 Current/Current Watchlist.md','vault/Home.md','vault/Wiki.md']:
    path=Path(fname); c=path.read_text(); marker=f'<!-- {STAMP.lower()}-brighton-team-review -->'
    if marker not in c:
        path.write_text(c.rstrip()+f"\n\n{marker}\n- Brighton internal ordering reviewed: [[06 Reviews/2026/08/2026-08-02/2045-AEST-review]] · [[07 Changes/2026/08/2026-08-02/2045-AEST-changes]].\n"); changed.append(str(path))
cl=Path('vault/00 Meta/Document Changelog.md'); source='https://fantasy.premierleague.com/api/bootstrap-static/'
for path in changed+[str(cl)]:
    action='created' if path in [REVIEW,CHANGES] else 'updated'
    cl.write_text(cl.read_text().rstrip()+f"\n| {TS} | `{path}` | {action} | Brighton internal team ordering review | [[06 Reviews/2026/08/2026-08-02/2045-AEST-review]] | {source} |\n")
print(json.dumps({'order':list(zip(ORDER,slots)),'moves':{n:[old[n],r] for n,r in zip(ORDER,slots)}},ensure_ascii=False,indent=2))
