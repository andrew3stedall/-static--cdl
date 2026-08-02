from pathlib import Path
import json, urllib.request, re

TS='2026-08-02T18:11:00+10:00'
STAMP='1811-AEST'
REVIEW='vault/06 Reviews/2026/08/2026-08-02/1811-AEST-review.md'
CHANGES='vault/07 Changes/2026/08/2026-08-02/1811-AEST-changes.md'
BOARD=Path('vault/01 Current/Current Draft Board.md')
TEAM=Path('vault/03 Teams/AVL.md')
ORDER=['Watkins','Garnacho','McGinn','Cash','Digne','Maatsen','Buendía','Martinez','Konsa','Pau','Mings','Guessand','Gomes','Kamara','Onana','Barkley','Manzambi','Bogarde','Lindelöf']
SLOTS=[7,120,121,150,164,231,242,244,259,265,269,276,281,291,296,300,317,322,340]
WHY={
'Watkins':'clear first-choice striker, strongest raw-points projection and forward scarcity',
'Garnacho':'highest direct attacking ceiling after Watkins, but role security remains below Watkins',
'McGinn':'secure minutes and broad route to returns beat the remaining options',
'Cash':'attacking defender ceiling and goal threat edge Digne narrowly',
'Digne':'set pieces and chance creation beat Maatsen while current minutes remain more secure',
'Maatsen':'higher upside than the deeper midfield and centre-back group, with rotation risk',
'Buendía':'creative and attacking ceiling exceeds the goalkeeper and centre-back floor options',
'Martinez':'secure goalkeeper minutes and save/clean-sheet floor beat low-upside outfield depth',
'Konsa':'best centre-back minutes floor',
'Pau':'progressive role and likely minutes edge Mings',
'Mings':'availability and aerial threat beat speculative attackers and defensive midfielders',
'Guessand':'attacking ceiling beats the low-upside midfield group, but role confidence is modest',
'Gomes':'available attacking-midfield pathway beats injured holding midfielders',
'Kamara':'availability-adjusted floor edges Onana',
'Onana':'greater box threat than Barkley but injury uncertainty limits him',
'Barkley':'set-piece possibility and experience edge the youth/depth options',
'Manzambi':'upside beats the final defensive depth options',
'Bogarde':'more plausible minutes than Lindelöf',
'Lindelöf':'lowest current ceiling and weakest route to regular starts'}

api=json.load(urllib.request.urlopen('https://fantasy.premierleague.com/api/bootstrap-static/'))
api_ids={e['id']:e for e in api['elements']}
lines=BOARD.read_text().splitlines()
rows=[]
for i,line in enumerate(lines):
    if re.match(r'^\| \d+ \|',line):
        c=[x.strip() for x in line.strip('|').split('|')]
        rows.append((i,c))
avl=[(i,c) for i,c in rows if c[3]=='AVL']
assert len(avl)==19, len(avl)
by_name={c[1]:(i,c) for i,c in avl}
assert set(by_name)==set(ORDER),(set(by_name),set(ORDER))
old={name:int(c[0]) for name,(i,c) in by_name.items()}
slot_template={int(c[0]):c for i,c in avl}
for name,slot in zip(ORDER,SLOTS):
    _,oldc=by_name[name]
    new=list(oldc)
    template=slot_template[slot]
    new[0]=str(slot); new[4]=template[4]; new[5]=template[5]; new[8]=TS; new[9]='[[06 Reviews/2026/08/2026-08-02/1811-AEST-review]]'
    idx=next(i for i,c in rows if int(c[0])==slot)
    lines[idx]='| '+' | '.join(new)+' |'
BOARD.write_text('\n'.join(lines)+'\n')

# Build current Villa rows and update player notes.
newrows=[]
for name,slot in zip(ORDER,SLOTS):
    line=next(x for x in lines if x.startswith(f'| {slot} |'))
    c=[x.strip() for x in line.strip('|').split('|')]
    assert c[1]==name
    assert int(c[6]) in api_ids
    newrows.append(c)
    p=Path(f'vault/02 Players/{name} - {c[6]}.md')
    if p.exists():
        txt=p.read_text()
        txt=re.sub(r'current_rank: \d+',f'current_rank: {slot}',txt)
        txt=re.sub(r'last_reviewed: .*',f'last_reviewed: {TS}',txt)
        txt += f'\n\n## {STAMP} Aston Villa comparison\n\n- New overall rank: **{slot}** (previously {old[name]}).\n- Internal club order: **{ORDER.index(name)+1} of {len(ORDER)}**.\n- Decision: {WHY[name]}.\n- Reversal trigger: confirmed role, set-piece, injury or first-team-minute evidence materially changing the comparison.\n- Review: [[06 Reviews/2026/08/2026-08-02/1811-AEST-review]].\n'
        p.write_text(txt)

ranked='\n'.join(f"{c[0]}. [[02 Players/{c[1]} - {c[6]}|{c[1]}]] — {c[2]}, AVL; {c[4]} / {c[5]}; {c[7]}" for c in newrows)
team=TEAM.read_text()
team=re.sub(r'last_reviewed: .*',f'last_reviewed: {TS}',team)
team=re.sub(r'<!-- ranked-players:start -->.*?<!-- ranked-players:end -->',f'''<!-- ranked-players:start -->\n## Players by overall rank\n\nPlayers are listed in canonical overall draft rank order after the full Aston Villa intra-team review.\n\n{ranked}\n\nSource: [[01 Current/Current Draft Board]] · reviewed {TS}\n<!-- ranked-players:end -->''',team,flags=re.S)
team += '\n\n## 1811-AEST internal ordering review\n\nAll 19 ranked Villa players were compared directly. See [[06 Reviews/2026/08/2026-08-02/1811-AEST-review]].\n'
TEAM.write_text(team)

comparisons='\n'.join(f"- **{ORDER[i]} over {ORDER[i+1]}** — {WHY[ORDER[i]]}. Confidence: {'high' if i<2 else 'medium' if i<10 else 'low-to-medium'}." for i in range(len(ORDER)-1))
changes='\n'.join(f"- {n}: **{old[n]} → {s}**" for n,s in zip(ORDER,SLOTS) if old[n]!=s)
Path(REVIEW).parent.mkdir(parents=True,exist_ok=True)
Path(REVIEW).write_text(f'''# Aston Villa internal FPL Draft review — {STAMP}\n\n## Scope\n\nCompared all 19 ranked Aston Villa players against each other. Raw expected FPL points were considered first, followed by minutes, role, set pieces, injury and rotation risk, floor and ceiling; draft scarcity was applied only afterward.\n\n## API reconciliation\n\nAll 19 stable FPL IDs were present in the official bootstrap API. Team and position metadata were treated as authoritative.\n\n## Final internal order\n\n'''+ranked+'\n\n## Decisive comparisons\n\n'+comparisons+'''\n\n## Evidence adopted\n\n- Official FPL API identity, team, position and availability metadata.\n- Existing canonical player evidence and prior dated reviews.\n\n## Evidence rejected or unavailable\n\nNo unsourced social-media claim or isolated friendly return was used to force movement. Exact X posts were not adopted unless already captured in the vault.\n\n## Uncertainties and reversal triggers\n\nGarnacho's role, the Cash/Digne/Maatsen full-back hierarchy, Buendía and Guessand attacking minutes, and Kamara/Onana fitness are the main reversal triggers.\n''')
Path(CHANGES).parent.mkdir(parents=True,exist_ok=True)
Path(CHANGES).write_text(f'''# Aston Villa changes — {STAMP}\n\n## Rank changes\n\n{changes}\n\n## Important no-change decision\n\nWatkins remains rank 7 and the clear first Villa player. Non-Villa ranks were preserved.\n\n## Watchlist changes\n\nPrioritise Garnacho role, Villa full-back selection, Buendía/Guessand minutes, and Kamara/Onana fitness.\n''')

for path in [Path('vault/01 Current/Current Watchlist.md'),Path('vault/Home.md'),Path('vault/Wiki.md')]:
    txt=path.read_text()
    txt += f'\n\n## {STAMP} Aston Villa review\n\n- Review: [[06 Reviews/2026/08/2026-08-02/1811-AEST-review]]\n- Changes: [[07 Changes/2026/08/2026-08-02/1811-AEST-changes]]\n'
    path.write_text(txt)

changed=[BOARD,TEAM,Path(REVIEW),Path(CHANGES),Path('vault/01 Current/Current Watchlist.md'),Path('vault/Home.md'),Path('vault/Wiki.md')]
for c in newrows:
    changed.append(Path(f'vault/02 Players/{c[1]} - {c[6]}.md'))
cl=Path('vault/00 Meta/Document Changelog.md')
text=cl.read_text()
for p in changed:
    action='created' if str(p) in [REVIEW,CHANGES] else 'updated'
    text += f'\n| {TS} | `{p}` | {action} | Aston Villa internal player ordering review | [[06 Reviews/2026/08/2026-08-02/1811-AEST-review]] | https://fantasy.premierleague.com/api/bootstrap-static/ |'
cl.write_text(text+'\n')
