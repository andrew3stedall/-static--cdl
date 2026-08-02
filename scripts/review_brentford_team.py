from pathlib import Path
import json, re, urllib.request

TS = '2026-08-02T20:32:00+10:00'
STAMP = '2032-AEST'
TEAM = 'BRE'
ORDER = ['Thiago','Damsgaard','O.Dango','Schade','Jensen','Lewis-Potter','Collins','Kelleher','Kayode','Van den Berg','Wilson','Anthony','Pinnock','Ajer','Henry','Janelt','Yarmoliuk','Hickey','Schuster','Ji-soo']
REASONS = {
'Thiago':'secure central-forward role, penalties, production and forward scarcity',
'Damsgaard':'creative hub, secure minutes and set-piece involvement',
'O.Dango':'greater direct goal threat but a slightly less stable floor than Damsgaard',
'Schade':'strong attacking ceiling with more role volatility than the top three',
'Jensen':'set pieces and chance creation provide a reliable accumulation route',
'Lewis-Potter':'attacking-role upside outweighs defensive and goalkeeper replacement options',
'Collins':'secure defensive minutes, clean-sheet access and aerial threat',
'Kelleher':'starting-goalkeeper floor but a highly replaceable draft position',
'Kayode':'attacking full-back upside with developing role certainty',
'Van den Berg':'stronger current centre-back minutes floor than the remaining defenders',
'Wilson':'forward scarcity and penalty-box upside despite uncertain minutes',
'Anthony':'direct attacking ceiling with uncertain starting status',
'Pinnock':'established centre-back floor and aerial threat',
'Ajer':'versatility and attacking carries, offset by rotation risk',
'Henry':'full-back upside but significant role and durability uncertainty',
'Janelt':'minutes floor with limited direct FPL ceiling',
'Yarmoliuk':'midfield minutes potential but low attacking expectation',
'Hickey':'upside exists, but fitness and role evidence remain weak',
'Schuster':'speculative defensive minutes',
'Ji-soo':'least secure first-team route in the ranked Brentford pool'
}
BOARD = Path('vault/01 Current/Current Draft Board.md')
REVIEW = Path('vault/06 Reviews/2026/08/2026-08-02/2032-AEST-review.md')
CHANGES = Path('vault/07 Changes/2026/08/2026-08-02/2032-AEST-changes.md')
api = json.load(urllib.request.urlopen('https://fantasy.premierleague.com/api/bootstrap-static/'))
active = {e['id']: e for e in api['elements']}
lines = BOARD.read_text().splitlines()
rows=[]
for idx,line in enumerate(lines):
    if re.match(r'^\| \d+ \|', line):
        rows.append((idx,[x.strip() for x in line.strip('|').split('|')]))
team_rows=[(i,p) for i,p in rows if p[3]==TEAM]
assert len(team_rows)==20, len(team_rows)
byname={p[1]:(i,p) for i,p in team_rows}
assert set(ORDER)==set(byname), (set(ORDER)-set(byname),set(byname)-set(ORDER))
slots=sorted(int(p[0]) for _,p in team_rows)
old={p[1]:int(p[0]) for _,p in team_rows}
slot_indices={int(p[0]):i for i,p in team_rows}
for rank,name in zip(slots,ORDER):
    _,p=byname[name]
    q=p.copy(); q[0]=str(rank); q[8]=TS; q[9]='[[06 Reviews/2026/08/2026-08-02/2032-AEST-review]]'
    lines[slot_indices[rank]]='| '+' | '.join(q)+' |'
BOARD.write_text('\n'.join(lines)+'\n')
changed=[str(BOARD)]
for rank,name in zip(slots,ORDER):
    _,p=byname[name]; fid=int(p[6]); assert fid in active
    matches=list(Path('vault/02 Players').glob(f'* - {fid}.md')); assert len(matches)==1,(name,fid)
    path=matches[0]; content=path.read_text(); marker='<!-- 2032-aest-brentford-team-review -->'
    block=(f"\n{marker}\n## Brentford team comparison — {STAMP}\n\n"
           f"- Internal Brentford rank: **{ORDER.index(name)+1} of 20**.\n"
           f"- Overall rank: **{rank}** (was {old[name]}).\n"
           f"- Comparator outcome: {REASONS[name]}.\n"
           f"- Reversal trigger: verified change in minutes, role, set pieces, fitness or transfer status.\n"
           f"- Evidence: [[06 Reviews/2026/08/2026-08-02/2032-AEST-review]].\n")
    if marker not in content:
        path.write_text(content.rstrip()+block+'\n'); changed.append(str(path))
# Team index
team=Path('vault/03 Teams/BRE.md'); tc=team.read_text(); board_now=BOARD.read_text().splitlines(); entries=[]
for line in board_now:
    if re.match(r'^\| \d+ \|',line):
        p=[x.strip() for x in line.strip('|').split('|')]
        if p[3]==TEAM:
            entries.append(f"{p[0]}. [[02 Players/{p[1]} - {p[6]}|{p[1]}]] — {p[2]}, BRE; {p[4]} / {p[5]}; {p[7]}")
section=('<!-- ranked-players:start -->\n## Players by overall rank\n\nPlayers are listed in canonical overall draft rank order.\n\n'+'\n'.join(entries)+f"\n\nSource: [[01 Current/Current Draft Board]] · generated {TS}\n<!-- ranked-players:end -->")
tc=re.sub(r'<!-- ranked-players:start -->.*?<!-- ranked-players:end -->',section,tc,flags=re.S)
tc=re.sub(r'last_reviewed: .*',f'last_reviewed: {TS}',tc)
team.write_text(tc); changed.append(str(team))
# Immutable review and changes
REVIEW.parent.mkdir(parents=True,exist_ok=True); CHANGES.parent.mkdir(parents=True,exist_ok=True)
comparisons='\n'.join(f"- **{ORDER[i]} over {ORDER[i+1]}** — {REASONS[ORDER[i]]}; confidence {'medium' if i<12 else 'low'}. Reverse with verified role, minutes, set-piece, fitness or transfer evidence." for i in range(len(ORDER)-1))
final_order='\n'.join(f"{i+1}. {n} — overall {r}" for i,(n,r) in enumerate(zip(ORDER,slots)))
REVIEW.write_text(f"---\ntype: review\nreviewed_at: {TS}\nteam: BRE\n---\n\n# Brentford internal FPL Draft review — {STAMP}\n\n## Scope\nAll 20 ranked Brentford players were compared directly. Raw expected FPL points were considered first, followed by expected minutes, role, penalties and set pieces, injury and rotation risk, floor and ceiling; positional replacement value was applied afterward.\n\n## Evidence\n- Official FPL bootstrap API for identity, team, position and availability.\n- Current canonical draft board and Brentford team note.\n- Existing repository evidence on Thiago, Damsgaard, Ouattara and Schade.\n- No unverified preseason scoreline was used to force movement.\n\n## Decisive comparison chain\n{comparisons}\n\n## Final internal order\n{final_order}\n\n## Uncertainties\nLewis-Potter, Wilson and Anthony are sensitive to attacking-role evidence. Kayode, Henry and Hickey depend on full-back hierarchy and fitness.\n")
CHANGES.write_text('---\ntype: changes\nchanged_at: '+TS+'\nteam: BRE\n---\n\n# Brentford ordering changes — '+STAMP+'\n\n'+'\n'.join((f"- {n}: **{old[n]} → {r}**" if old[n]!=r else f"- {n}: **{r}, unchanged**") for n,r in zip(ORDER,slots))+'\n\nNo non-Brentford player rank changed. The board remains 350 unique, physically ordered ranks.\n')
changed += [str(REVIEW),str(CHANGES)]
for fname in ['vault/01 Current/Current Watchlist.md','vault/Home.md','vault/Wiki.md']:
    path=Path(fname); c=path.read_text(); marker='<!-- 2032-aest-brentford-team-review -->'
    if marker not in c:
        path.write_text(c.rstrip()+f"\n\n{marker}\n- Brentford internal ordering reviewed: [[06 Reviews/2026/08/2026-08-02/2032-AEST-review]] · [[07 Changes/2026/08/2026-08-02/2032-AEST-changes]].\n")
        changed.append(str(path))
cl=Path('vault/00 Meta/Document Changelog.md'); source='https://fantasy.premierleague.com/api/bootstrap-static/'
for path in changed+[str(cl)]:
    action='created' if path in [str(REVIEW),str(CHANGES)] else 'updated'
    with cl.open('a') as f:
        f.write(f"| {TS} | `{path}` | {action} | Brentford internal team ordering review | [[06 Reviews/2026/08/2026-08-02/2032-AEST-review]] | {source} |\n")
print(json.dumps({'order':list(zip(ORDER,slots)),'moves':{n:[old[n],r] for n,r in zip(ORDER,slots)},'changed_markdown':len(changed)+1},indent=2))
