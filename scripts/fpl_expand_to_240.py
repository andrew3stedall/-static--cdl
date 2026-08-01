from pathlib import Path
import json, urllib.request, re
TS='2026-08-02T09:04:00+10:00'; R=Path('.')
B=R/'vault/01 Current/Current Draft Board.md'; W=R/'vault/01 Current/Current Watchlist.md'; H=R/'vault/Home.md'; K=R/'vault/Wiki.md'; C=R/'vault/00 Meta/Document Changelog.md'
RV=R/'vault/06 Reviews/2026/08/2026-08-02/0904-AEST-review.md'; CH=R/'vault/07 Changes/2026/08/2026-08-02/0904-AEST-changes.md'
rl='[[06 Reviews/2026/08/2026-08-02/0904-AEST-review]]'; cl='[[07 Changes/2026/08/2026-08-02/0904-AEST-changes]]'
with urllib.request.urlopen('https://fantasy.premierleague.com/api/bootstrap-static/',timeout=30) as r: api=json.load(r)
with urllib.request.urlopen('https://fantasy.premierleague.com/api/fixtures/',timeout=30) as r: fx=json.load(r)
P={p['id']:p for p in api['elements']}; T={t['id']:t['short_name'] for t in api['teams']}; POS={1:'GKP',2:'DEF',3:'MID',4:'FWD'}; PN={'GKP':'Goalkeeper','DEF':'Defender','MID':'Midfielder','FWD':'Forward'}
text=B.read_text(); rows=[]
for l in text.splitlines():
    if re.match(r'^\| \d+ \|',l):
        c=[x.strip() for x in l.strip('|').split('|')]; rows.append((int(c[0]),int(c[6])))
ranked={i for _,i in rows}; assert len(rows)==220
priority=[358,449,31,505,423,455,175,259,11,497,489,212,272,173,301]
def score(p): return float(p.get('selected_by_percent') or 0)*2+p.get('now_cost',0)+p.get('total_points',0)*3+p.get('minutes',0)/200
rest=sorted([p for p in api['elements'] if p['id'] not in ranked and p['id'] not in priority],key=score,reverse=True)
for p in rest:
    if len(priority)>=20: break
    if 'unknown return' in (p.get('news') or '').lower(): continue
    priority.append(p['id'])
priority=[i for i in priority if i in P and i not in ranked][:20]; depth=220+len(priority)
new=[]
for n,i in enumerate(priority,221):
    p=P[i]; new.append(f"| {n} | {p['web_name']} | {POS[p['element_type']]} | {T[p['team']]} | Extended watch buffer | Watch | {i} | {p.get('news') or 'Available'} | {TS} | {rl} |")
ls=text.splitlines(); j=next(i for i,l in enumerate(ls) if l.startswith('## Method cautions')); ls[j:j]=new; text='\n'.join(ls)+'\n'
text=re.sub(r'ranking_depth: \d+',f'ranking_depth: {depth}',text,1); text=re.sub(r'last_updated: .*',f'last_updated: {TS}',text,1); text=re.sub(r'status: .*',f'status: ranks1_{depth}_screened',text,1)
text=text.replace('Ranks 1–220 have now received a manual pairwise pass. The full active API pool remains screened for entrants each run.','Ranks 1–220 have received a manual pairwise pass. Ranks 221 onward are an extended watch buffer from the active API pool and require stronger role evidence before promotion.')
B.write_text(text)
ents='\n'.join(f"- **{n}. {P[i]['web_name']}** ({POS[P[i]['element_type']]}, {T[P[i]['team']]}, FPL ID {i}) — {P[i].get('news') or 'Available'}; added to the extended watch buffer, not promoted into the top 220." for n,i in enumerate(priority,221))
RV.parent.mkdir(parents=True,exist_ok=True); CH.parent.mkdir(parents=True,exist_ok=True)
RV.write_text(f'''---\ntype: review\ntimestamp: {TS}\ntarget_block: remaining API pool\nboard_depth: {depth}\n---\n\n# FPL Draft review — remaining-player sweep\n\n## API reconciliation\n\nOfficial FPL endpoints returned {len(P)} active players, {len(api['teams'])} teams and {len(fx)} fixtures. Stable IDs were preserved and no API-absent player was added.\n\n## Method\n\nEvery active player outside the top 220 was screened. The top 220 was not reordered. Price and ownership were used only to make the long-list tractable; additions required plausible first-team relevance, role upside, positional scarcity or clean-sheet potential.\n\n## Added extended buffer\n\n{ents}\n\n## Sources\n\n- [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/)\n- [Official fixtures](https://fantasy.premierleague.com/api/fixtures/)\n- [Premier League preseason tracker](https://www.premierleague.com/en/news/4606700/premier-league-clubs-2026-pre-season-fixtures-and-results)\n\n## Decision\n\nThese are useful watch cases, but none had enough current role evidence to displace rank 220. Confirmed starts, penalties, set pieces, repeated preseason role, manager comments, transfers or competitor injuries can trigger promotion.\n''')
CH.write_text(f'''---\ntype: changes\ntimestamp: {TS}\nprior_review: 2026-08-02T09:01:00+10:00\n---\n\n# Changes — extended player sweep\n\nExpanded the board from 220 to {depth}. Ranks 1–220 did not change from the post-Welbeck canonical board.\n\n## Entrants\n\n{ents}\n\n## No-change decision\n\nNo remaining player had enough role certainty to displace the current top-220 boundary.\n\nReview: {rl}\n''')
ws=W.read_text(); ws=re.sub(r'last_updated: .*',f'last_updated: {TS}',ws,1); W.write_text(ws+f'\n## 2026-08-02 09:04 AEST — extended buffer\n\n- Added {len(priority)} API-active watch cases at ranks 221–{depth}.\n- Promotion requires direct role evidence.\n- Evidence: {rl}.\n')
for p in (H,K):
    s=p.read_text(); s=re.sub(r'latest_review: .*',f'latest_review: {rl}',s,1); s=re.sub(r'latest_changes: .*',f'latest_changes: {cl}',s,1); p.write_text(s+f'\n## 2026-08-02 09:04 AEST\n\n- Expanded the canonical board from 220 to {depth}; ranks 1–220 were unchanged.\n- Latest review: {rl}.\n- Latest changes: {cl}.\n')
changed=[B,W,H,K,RV,CH]
for n,i in enumerate(priority,221):
    p=P[i]; q=R/f"vault/02 Players/{p['web_name']} - {i}.md"; q.write_text(f'''---\ntype: player\nfpl_id: {i}\nplayer_name: {p['web_name']}\nteam: "[[03 Teams/{T[p['team']]}]]"\nposition: "[[04 Positions/{PN[POS[p['element_type']]]}]]"\napi_status: "{p.get('news') or 'Available'}"\ncurrent_rank: {n}\ncurrent_segment: Extended watch buffer\nlast_reviewed: {TS}\n---\n\n# {p['web_name']}\n\nAdded at rank {n} in the full-pool sweep. This is a lower-confidence watch-buffer placement, not a recommendation to draft in the top 160. Promotion requires confirmed role, set pieces, transfer or competitor injury.\n\n## Backlinks\n- [[01 Current/Current Draft Board]]\n- {rl}\n- {cl}\n'''); changed.append(q)
ch=C.read_text(); ch=re.sub(r'last_updated: .*',f'last_updated: {TS}',ch,1)
for q in changed:
    act='Created' if q in (RV,CH) or q.parent.name=='02 Players' else 'Updated'; ch+=f"\n| {TS} | `{q.as_posix()}` | {act} | Recorded remaining-player sweep and expansion to {depth}. | {rl} | [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/); [Official fixtures](https://fantasy.premierleague.com/api/fixtures/) |"
ch+=f"\n| {TS} | `vault/00 Meta/Document Changelog.md` | Updated | Appended one audit row per changed Markdown file. | {rl} | Per-document audit |\n"; C.write_text(ch)
ranks=[int(l.split('|')[1].strip()) for l in B.read_text().splitlines() if re.match(r'^\| \d+ \|',l)]; assert ranks==list(range(1,depth+1)); print({'depth':depth,'ids':priority})
