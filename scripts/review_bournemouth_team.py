from pathlib import Path
import json,re,urllib.request
TS='2026-08-02T18:25:00+10:00'; STAMP='1825-AEST'
REVIEW='vault/06 Reviews/2026/08/2026-08-02/1825-AEST-review.md'; CHANGES='vault/07 Changes/2026/08/2026-08-02/1825-AEST-changes.md'
ORDER=['Kluivert','Tavernier','Evanilson','Rayan','Scott','Truffert','Petrović','Brooks','Adli','Rodríguez','Hill','Enes Ünal','Kroupi.Jr','Adams','Cook','Smith','Milosavljević','Diakité','Christie']
WHY=['penalties and advanced role','set pieces and secure attacking minutes','starting-forward scarcity','attacking upside','minutes and progression','attacking full-back role','secure goalkeeper floor','direct attacking ceiling','creative upside','forward scarcity','defensive minutes floor','forward upside with role risk','ceiling discounted by injury','minutes floor','minutes and some set pieces','defensive depth','uncertain role','rotation-level role','suspension and limited ceiling']
active={e['id'] for e in json.load(urllib.request.urlopen('https://fantasy.premierleague.com/api/bootstrap-static/'))['elements']}
board=Path('vault/01 Current/Current Draft Board.md'); lines=board.read_text().splitlines(); rows=[]
for i,l in enumerate(lines):
    if re.match(r'^\| \d+ \|',l): rows.append((i,[x.strip() for x in l.strip('|').split('|')]))
bou=[x for x in rows if x[1][3]=='BOU']; assert len(bou)==19
by={p[1]:(i,p) for i,p in bou}; assert set(by)==set(ORDER)
slots=sorted(int(p[0]) for _,p in bou); old={p[1]:int(p[0]) for _,p in bou}
for rank,name in zip(slots,ORDER):
    _,p=by[name]; p=p.copy(); p[0]=str(rank); p[8]=TS; p[9]='[[06 Reviews/2026/08/2026-08-02/1825-AEST-review]]'
    idx=next(i for i,q in bou if int(q[0])==rank); lines[idx]='| '+' | '.join(p)+' |'
board.write_text('\n'.join(lines)+'\n'); changed=[str(board)]
for n,rank,why in zip(ORDER,slots,WHY):
    fid=int(by[n][1][6]); assert fid in active
    paths=list(Path('vault/02 Players').glob(f'* - {fid}.md')); assert len(paths)==1
    p=paths[0]; c=p.read_text(); m=f'<!-- {STAMP.lower()}-bournemouth-team-review -->'
    if m not in c:
        p.write_text(c.rstrip()+f"\n\n{m}\n## Bournemouth team comparison — {STAMP}\n\n- Internal rank: **{ORDER.index(n)+1} of 19**.\n- Overall rank: **{rank}** (was {old[n]}).\n- Comparator outcome: {why}.\n- Reversal trigger: verified change in minutes, role, set pieces or fitness.\n- Evidence: [[06 Reviews/2026/08/2026-08-02/1825-AEST-review]].\n"); changed.append(str(p))
team=Path('vault/03 Teams/BOU.md'); tc=team.read_text(); entries=[]
for rank,n in zip(slots,ORDER):
    p=by[n][1]; entries.append(f"{rank}. [[02 Players/{n} - {p[6]}|{n}]] — {p[2]}, BOU; {p[4]} / {p[5]}; {p[7]}")
sec='<!-- ranked-players:start -->\n## Players by overall rank\n\nPlayers are listed in canonical overall draft rank order.\n\n'+'\n'.join(entries)+f"\n\nSource: [[01 Current/Current Draft Board]] · generated {TS}\n<!-- ranked-players:end -->"
tc=re.sub(r'<!-- ranked-players:start -->.*?<!-- ranked-players:end -->',sec,tc,flags=re.S); tc=re.sub(r'last_reviewed: .*',f'last_reviewed: {TS}',tc); team.write_text(tc); changed.append(str(team))
review=Path(REVIEW); review.parent.mkdir(parents=True,exist_ok=True)
chain='\n'.join(f"- **{ORDER[i]} over {ORDER[i+1]}** — {WHY[i]}; confidence {'medium' if i<10 else 'low'}." for i in range(18))
review.write_text(f"---\ntype: review\nreviewed_at: {TS}\nteam: BOU\n---\n\n# Bournemouth internal FPL Draft review — {STAMP}\n\nAll 19 ranked Bournemouth players were compared using raw expected points first, then minutes, role, set pieces, injury and rotation risk, floor and ceiling, with positional scarcity applied afterward.\n\n## Decisive comparison chain\n{chain}\n\n## Final internal order\n"+'\n'.join(f"{i+1}. {n} — overall {r}" for i,(n,r) in enumerate(zip(ORDER,slots)))+'\n\n## Uncertainties\nBrooks, Adli, Rodríguez, Enes Ünal and Kroupi Jr remain role-sensitive; Christie is suspension-discounted.\n'); changed.append(str(review))
changes=Path(CHANGES); changes.parent.mkdir(parents=True,exist_ok=True); moves='\n'.join(f"- {n}: **{old[n]} → {r}**" if old[n]!=r else f"- {n}: **{r}, unchanged**" for n,r in zip(ORDER,slots))
changes.write_text(f"---\ntype: changes\nchanged_at: {TS}\nteam: BOU\n---\n\n# Bournemouth ordering changes — {STAMP}\n\n{moves}\n\nNo non-Bournemouth player rank changed.\n"); changed.append(str(changes))
for f in ['vault/01 Current/Current Watchlist.md','vault/Home.md','vault/Wiki.md']:
    p=Path(f); c=p.read_text(); m=f'<!-- {STAMP.lower()}-bournemouth-team-review -->'
    if m not in c: p.write_text(c.rstrip()+f"\n\n{m}\n- Bournemouth internal ordering reviewed: [[06 Reviews/2026/08/2026-08-02/1825-AEST-review]] · [[07 Changes/2026/08/2026-08-02/1825-AEST-changes]].\n"); changed.append(str(p))
cl=Path('vault/00 Meta/Document Changelog.md'); src='https://fantasy.premierleague.com/api/bootstrap-static/'
for f in changed+[str(cl)]:
    action='created' if f in [REVIEW,CHANGES] else 'updated'; cl.write_text(cl.read_text().rstrip()+f"\n| {TS} | `{f}` | {action} | Bournemouth internal team ordering review | [[06 Reviews/2026/08/2026-08-02/1825-AEST-review]] | {src} |\n")
print(json.dumps({'order':list(zip(ORDER,slots)),'moves':{n:[old[n],r] for n,r in zip(ORDER,slots)}},ensure_ascii=False))
