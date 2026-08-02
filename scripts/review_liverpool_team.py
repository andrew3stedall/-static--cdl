from pathlib import Path
import re, glob

TS='2026-08-03T00:18:00+10:00'; HM='0018-AEST'; team='LIV'
root=Path('.')
boardp=root/'vault/01 Current/Current Draft Board.md'
text=boardp.read_text()
rows=[]
for line in text.splitlines():
    m=re.match(r'\| (\d+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| (\d+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|',line)
    if m: rows.append({'rank':int(m.group(1)),'name':m.group(2).strip(),'pos':m.group(3).strip(),'team':m.group(4).strip(),'segment':m.group(5).strip(),'tier':m.group(6).strip(),'id':int(m.group(7)),'status':m.group(8).strip(),'changed':m.group(9).strip(),'evidence':m.group(10).strip(),'line':line})
liv=[r for r in rows if r['team']=='LIV']
slots=sorted(r['rank'] for r in liv)
order=[379,366,367,368,356,357,358,350,372,371,380,373,369,370,364,360,362,351,377]
byid={r['id']:r for r in liv}
assert set(order)==set(byid), (set(order)-set(byid),set(byid)-set(order))
slotmeta={r['rank']:(r['segment'],r['tier']) for r in rows}
new=[]
for rank,pid in zip(slots,order):
    r=byid[pid].copy(); r['old']=r['rank']; r['rank']=rank; r['segment'],r['tier']=slotmeta[rank]; r['changed']=TS; r['evidence']='[[06 Reviews/2026/08/2026-08-03/0018-AEST-review]]'; new.append(r)
newbyrank={r['rank']:r for r in new}
out=[]
for line in text.splitlines():
    m=re.match(r'\| (\d+) \|',line)
    if m and int(m.group(1)) in newbyrank:
        r=newbyrank[int(m.group(1))]
        line=f"| {r['rank']} | {r['name']} | {r['pos']} | LIV | {r['segment']} | {r['tier']} | {r['id']} | {r['status']} | {r['changed']} | {r['evidence']} |"
    out.append(line)
boardp.write_text('\n'.join(out)+'\n')

reasons={379:'best raw-points ceiling, penalties-level talismanic role and forward scarcity',366:'elite creative and goal-involvement ceiling in the post-Salah attack',367:'established scoring threat with a strong route to central minutes',368:'set pieces and secure minutes outweigh the deeper-role concern',356:'elite minutes, clean-sheet access and aerial threat',357:'greater attacking ceiling than the other defenders, with rotation risk',358:'strong attacking full-back profile and clean-sheet access',350:'elite goalkeeper floor but replaceable position',372:'set pieces and accumulation floor provide the best remaining midfield route',371:'secure minutes but more limited direct attacking output',380:'high striker ceiling heavily discounted by the Achilles injury',373:'useful attacking-midfield upside with rotation risk',369:'breakout winger ceiling but weak minutes certainty',370:'senior attacking upside with substantial role uncertainty',364:'backup full-back value and possible set-piece route',360:'attacking full-back upside, heavily injury-discounted',362:'centre-back depth with limited present role certainty',351:'high-quality goalkeeper but blocked by Alisson',377:'lowest current first-team role certainty in the ranked Liverpool pool'}
for i,r in enumerate(new,1):
    files=glob.glob(f"vault/02 Players/* - {r['id']}.md")
    assert len(files)==1,(r['id'],files)
    p=Path(files[0]); s=p.read_text(); marker='<!-- 0018-aest-liverpool-team-review -->'
    block=f"\n{marker}\n## Liverpool team comparison — 0018-AEST\n\n- Internal Liverpool rank: **{i} of {len(new)}**.\n- Overall rank: **{r['rank']}** (was {r['old']}).\n- Segment/tier: **{r['segment']} / {r['tier']}**.\n- Comparator outcome: {reasons[r['id']]}.\n- Reversal trigger: verified change in minutes, role, penalties, set pieces, fitness or first-choice status.\n- Evidence: [[06 Reviews/2026/08/2026-08-03/0018-AEST-review]].\n"
    if marker not in s: p.write_text(s.rstrip()+'\n'+block)

teamp=root/'vault/03 Teams/LIV.md'; s=teamp.read_text(); s=re.sub(r'last_reviewed: .*',f'last_reviewed: {TS}',s,1)
start=s.index('<!-- ranked-players:start -->'); end=s.index('<!-- ranked-players:end -->')+len('<!-- ranked-players:end -->')
lines=['<!-- ranked-players:start -->','## Players by overall rank','','Players are listed in canonical overall draft rank order.','']
for r in new:
    files=glob.glob(f"vault/02 Players/* - {r['id']}.md"); stem=Path(files[0]).stem
    lines.append(f"{r['rank']}. [[02 Players/{stem}|{r['name']}]] — {r['pos']}, LIV; {r['segment']} / {r['tier']}; {r['status']}")
lines+=['',f'Source: [[01 Current/Current Draft Board]] · generated {TS}','<!-- ranked-players:end -->']
teamp.write_text(s[:start]+'\n'.join(lines)+s[end:])

pairs=[]
for a,b in zip(new,new[1:]): pairs.append(f"- **{a['name']} over {b['name']}** — {reasons[a['id']]}; confidence {'medium' if a['rank']<160 else 'low'}. Reverse with verified role, fitness, set-piece or minutes evidence.")
review=root/'vault/06 Reviews/2026/08/2026-08-03/0018-AEST-review.md'; review.parent.mkdir(parents=True,exist_ok=True)
review.write_text(f"---\ntype: review\nreviewed_at: {TS}\nteam: LIV\n---\n\n# Liverpool internal FPL Draft review — 0018-AEST\n\n## Scope\nAll {len(new)} ranked Liverpool players were compared directly. Raw expected points were assessed first, then minutes, role, penalties and set pieces, injury and rotation risk, floor and ceiling; positional replacement value was applied afterward.\n\n## Evidence\n- [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/) for identity, team, position and availability.\n- Current canonical board and Liverpool team note.\n- Existing exact Liverpool evidence links in the team note were retained; no unsupported social-media inference was promoted to fact.\n\n## Decisive comparison chain\n"+'\n'.join(pairs)+"\n\n## Final internal order\n"+'\n'.join(f"{i}. {r['name']} — overall {r['rank']} — {r['segment']} / {r['tier']}" for i,r in enumerate(new,1))+"\n\n## Uncertainties\nEkitiké's Achilles recovery, Frimpong/Kerkez rotation, Szoboszlai's depth of role, and the winger hierarchy are the main reversal triggers.\n")
changes=root/'vault/07 Changes/2026/08/2026-08-03/0018-AEST-changes.md'; changes.parent.mkdir(parents=True,exist_ok=True)
changes.write_text(f"---\ntype: changes\nchanged_at: {TS}\nteam: LIV\n---\n\n# Liverpool ordering changes — 0018-AEST\n\n"+'\n'.join(f"- {r['name']}: **{r['old']}, unchanged**" if r['old']==r['rank'] else f"- {r['name']}: **{r['old']} → {r['rank']}**" for r in new)+"\n\nNo non-Liverpool player rank changed. The board remains 350 unique, physically ordered ranks.\n")

for path in ['vault/01 Current/Current Watchlist.md','vault/Home.md','vault/Wiki.md']:
    p=Path(path); s=p.read_text(); marker='<!-- 0018-aest-liverpool-team-review -->'
    if marker not in s: p.write_text(s.rstrip()+f"\n\n{marker}\n- Liverpool internal ordering reviewed: [[06 Reviews/2026/08/2026-08-03/0018-AEST-review]] · [[07 Changes/2026/08/2026-08-03/0018-AEST-changes]].\n")

changed=[boardp]+[Path(glob.glob(f"vault/02 Players/* - {r['id']}.md")[0]) for r in new]+[teamp,review,changes,Path('vault/01 Current/Current Watchlist.md'),Path('vault/Home.md'),Path('vault/Wiki.md')]
cp=Path('vault/00 Meta/Document Changelog.md'); cs=cp.read_text().rstrip()
for p in changed:
    action='created' if p in [review,changes] else 'updated'
    cs+=f"\n| {TS} | `{p.as_posix()}` | {action} | Liverpool internal team ordering review | [[06 Reviews/2026/08/2026-08-03/0018-AEST-review]] | https://fantasy.premierleague.com/api/bootstrap-static/ |"
cs+=f"\n| {TS} | `vault/00 Meta/Document Changelog.md` | updated | Liverpool internal team ordering review | [[06 Reviews/2026/08/2026-08-03/0018-AEST-review]] | https://fantasy.premierleague.com/api/bootstrap-static/ |\n"
cp.write_text(cs)
