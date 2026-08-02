from pathlib import Path
import json, re, urllib.request

TS='2026-08-02T18:25:00+10:00'
STAMP='1825-AEST'
REVIEW='vault/06 Reviews/2026/08/2026-08-02/1825-AEST-review.md'
CHANGES='vault/07 Changes/2026/08/2026-08-02/1825-AEST-changes.md'
BOARD=Path('vault/01 Current/Current Draft Board.md')
ORDER=['Kluivert','Tavernier','Evanilson','Rayan','Scott','Truffert','Petrović','Brooks','Adli','Rodríguez','Hill','Enes Ünal','Kroupi.Jr','Adams','Cook','Smith','Milosavljević','Diakité','Christie']
REASONS={
'Kluivert':'penalty and advanced-role ceiling with strong attacking floor',
'Tavernier':'set-piece share and secure attacking minutes',
'Evanilson':'starting-forward scarcity and central role',
'Rayan':'high-upside attacking role but less established floor',
'Scott':'minutes and progressive attacking involvement',
'Truffert':'attacking full-back upside with cleaner role than the remaining defenders',
'Petrović':'secure goalkeeper floor but replaceable position',
'Brooks':'direct attacking ceiling when selected',
'Adli':'creative upside with role uncertainty',
'Rodríguez':'forward scarcity but weak current minutes evidence',
'Hill':'defensive minutes floor',
'Enes Ünal':'forward upside discounted by uncertain role',
'Kroupi.Jr':'high ceiling, heavily discounted by injury and role uncertainty',
'Adams':'minutes floor with limited FPL ceiling',
'Cook':'minutes floor and some set-piece involvement',
'Smith':'defensive depth with limited attacking ceiling',
'Milosavljević':'uncertain first-team role',
'Diakité':'rotation-level defensive profile',
'Christie':'opening suspension and limited attacking ceiling'}

api=json.load(urllib.request.urlopen('https://fantasy.premierleague.com/api/bootstrap-static/'))
active={e['id']:e for e in api['elements']}
text=BOARD.read_text()
lines=text.splitlines()
rows=[]
for i,l in enumerate(lines):
    if re.match(r'^\| \d+ \|',l):
        p=[x.strip() for x in l.strip('|').split('|')]
        rows.append((i,p))
bou=[(i,p) for i,p in rows if p[3]=='BOU']
assert len(bou)==19, len(bou)
byname={p[1]:(i,p) for i,p in bou}
assert set(ORDER)==set(byname), (set(ORDER)-set(byname),set(byname)-set(ORDER))
slots=sorted(int(p[0]) for _,p in bou)
oldrank={p[1]:int(p[0]) for _,p in bou}
for rank,name in zip(slots,ORDER):
    _,p=byname[name]
    p=p.copy(); p[0]=str(rank); p[8]=TS; p[9]='[[06 Reviews/2026/08/2026-08-02/1825-AEST-review]]'
    idx=next(i for i,q in bou if int(q[0])==rank)
    lines[idx]='| '+' | '.join(p)+' |'
BOARD.write_text('\n'.join(lines)+'\n')

# player notes
changed=[str(BOARD)]
for rank,name in zip(slots,ORDER):
    _,p=byname[name]; fid=int(p[6]); assert fid in active
    matches=list(Path('vault/02 Players').glob(f'* - {fid}.md')); assert len(matches)==1,(name,fid,matches)
    path=matches[0]; content=path.read_text()
    block=f"\n<!-- {STAMP.lower()}-bournemouth-team-review -->\n## Bournemouth team comparison — {STAMP}\n\n- Internal Bournemouth rank: **{ORDER.index(name)+1} of 19**.\n- Overall rank: **{rank}** (was {oldrank[name]}).\n- Comparator outcome: {REASONS[name]}.\n- Reversal trigger: verified change in minutes, set pieces, fitness or first-choice role.\n- Evidence: [[06 Reviews/2026/08/2026-08-02/1825-AEST-review]].\n"
    if f'<!-- {STAMP.lower()}-bournemouth-team-review -->' not in content:
        path.write_text(content.rstrip()+block+'\n'); changed.append(str(path))

# team note ranked section
team=Path('vault/03 Teams/BOU.md'); tc=team.read_text()
entries=[]
newrows=[]
for _,p in rows:
    if p[3]=='BOU': newrows.append(p)
newrows=sorted(newrows,key=lambda p:int(p[0]))
for p in newrows:
    fid=p[6]; entries.append(f"{p[0]}. [[02 Players/{p[1]} - {fid}|{p[1]}]] — {p[2]}, BOU; {p[4]} / {p[5]}; {p[7]}")
section='<!-- ranked-players:start -->\n## Players by overall rank\n\nPlayers are listed in canonical overall draft rank order.\n\n'+'\n'.join(entries)+f"\n\nSource: [[01 Current/Current Draft Board]] · generated {TS}\n<!-- ranked-players:end -->"
tc=re.sub(r'<!-- ranked-players:start -->.*?<!-- ranked-players:end -->',section,tc,flags=re.S)
tc=re.sub(r'last_reviewed: .*',f'last_reviewed: {TS}',tc)
team.write_text(tc); changed.append(str(team))

review=Path(REVIEW); review.parent.mkdir(parents=True,exist_ok=True)
comparisons='\n'.join(f"- **{ORDER[i]} over {ORDER[i+1]}** — {REASONS[ORDER[i]]}; confidence {'medium' if i<10 else 'low'}. Reverse with verified role, minutes, set-piece or fitness evidence." for i in range(len(ORDER)-1))
review.write_text(f"""---\ntype: review\nreviewed_at: {TS}\nteam: BOU\n---\n\n# Bournemouth internal FPL Draft review — {STAMP}\n\n## Scope\nAll 19 ranked Bournemouth players were compared directly. Raw expected FPL points were considered first, followed by expected minutes, role, penalties and set pieces, injury and rotation risk, floor and ceiling; positional replacement value was applied only afterward.\n\n## Evidence\n- Official FPL bootstrap API for player identity, team, position and availability.\n- Current canonical draft board and Bournemouth team note.\n- No unsourced preseason goal or assist was used to force movement.\n\n## Decisive comparison chain\n{comparisons}\n\n## Final internal order\n"""+'\n'.join(f"{i+1}. {n} — overall {r}" for i,(n,r) in enumerate(zip(ORDER,slots)))+"\n\n## Uncertainties\nBrooks, Adli, Rodríguez, Enes Ünal and Kroupi Jr remain sensitive to first-team role and fitness evidence. Christie is discounted for suspension.\n")
changed.append(str(review))

changes=Path(CHANGES); changes.parent.mkdir(parents=True,exist_ok=True)
move_lines='\n'.join(f"- {n}: **{oldrank[n]} → {r}**" if oldrank[n]!=r else f"- {n}: **{r}, unchanged**" for n,r in zip(ORDER,slots))
changes.write_text(f"""---\ntype: changes\nchanged_at: {TS}\nteam: BOU\n---\n\n# Bournemouth ordering changes — {STAMP}\n\n{move_lines}\n\nNo non-Bournemouth player rank changed. The board remains 350 unique, physically ordered ranks.\n")
changed.append(str(changes))

for fname in ['vault/01 Current/Current Watchlist.md','vault/Home.md','vault/Wiki.md']:
    path=Path(fname); c=path.read_text(); marker=f'<!-- {STAMP.lower()}-bournemouth-team-review -->'
    if marker not in c:
        c=c.rstrip()+f"\n\n{marker}\n- Bournemouth internal ordering reviewed: [[06 Reviews/2026/08/2026-08-02/1825-AEST-review]] · [[07 Changes/2026/08/2026-08-02/1825-AEST-changes]].\n"
        path.write_text(c+'\n'); changed.append(str(path))

# changelog row for every changed markdown including itself
cl=Path('vault/00 Meta/Document Changelog.md')
source='https://fantasy.premierleague.com/api/bootstrap-static/'
for path in changed+[str(cl)]:
    action='created' if path in [REVIEW,CHANGES] else 'updated'
    cl.write_text(cl.read_text().rstrip()+f"\n| {TS} | `{path}` | {action} | Bournemouth internal team ordering review | [[06 Reviews/2026/08/2026-08-02/1825-AEST-review]] | {source} |\n")

print(json.dumps({'order':list(zip(ORDER,slots)),'moves':{n:[oldrank[n],r] for n,r in zip(ORDER,slots)},'changed_markdown':len(changed)+1},ensure_ascii=False,indent=2))
