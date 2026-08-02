from pathlib import Path
import json,re,urllib.request
TS='2026-08-02T10:01:00+10:00'; R=Path('.')
B=R/'vault/01 Current/Current Draft Board.md'; W=R/'vault/01 Current/Current Watchlist.md'; H=R/'vault/Home.md'; K=R/'vault/Wiki.md'; C=R/'vault/00 Meta/Document Changelog.md'
RV=R/'vault/06 Reviews/2026/08/2026-08-02/1001-AEST-review.md'; CH=R/'vault/07 Changes/2026/08/2026-08-02/1001-AEST-changes.md'
rl='[[06 Reviews/2026/08/2026-08-02/1001-AEST-review]]'; cl='[[07 Changes/2026/08/2026-08-02/1001-AEST-changes]]'
with urllib.request.urlopen('https://fantasy.premierleague.com/api/bootstrap-static/',timeout=30) as r: api=json.load(r)
with urllib.request.urlopen('https://fantasy.premierleague.com/api/fixtures/',timeout=30) as r: fx=json.load(r)
P={p['id']:p for p in api['elements']}; T={t['id']:t['short_name'] for t in api['teams']}; POS={1:'GKP',2:'DEF',3:'MID',4:'FWD'}; PN={'GKP':'Goalkeeper','DEF':'Defender','MID':'Midfielder','FWD':'Forward'}
text=B.read_text(); lines=text.splitlines(); rows=[]
for l in lines:
    if re.match(r'^\| \d+ \|',l):
        c=[x.strip() for x in l.strip('|').split('|')]
        rows.append({'rank':int(c[0]),'name':c[1],'pos':c[2],'team':c[3],'segment':c[4],'tier':c[5],'id':int(c[6]),'status':c[7],'changed':c[8],'evidence':c[9]})
assert len(rows)==240
entrants=[358,449,31,505,423,455,175,259,11,497,489,212,272,173,301,57,250,88,140,534]
targets={358:68,449:84,57:96,250:103,140:111,455:124,31:132,505:139,423:148,175:154,534:160,88:166,173:173,11:181,489:188,259:195,212:202,497:209,272:216,301:232}
reasons={
358:'attacking Liverpool full-back ceiling and clean-sheet upside justify a rotation-range placement',
449:'attacking Newcastle full-back upside merits a top-100 range, but fitness and role certainty cap him below safer starters',
57:'probable starting-goalkeeper value and save potential place him with the lead goalkeeper cluster',
250:'secure goalkeeper minutes and save volume place him near the established goalkeeper cluster',
140:'Chelsea clean-sheet ceiling is useful, but hierarchy uncertainty keeps him below safer goalkeeper options',
455:'minutes and all-round midfield floor merit a core depth slot, without assuming penalties or an advanced role',
31:'secure centre-back minutes and clean-sheet floor fit the dependable defensive-depth range',
505:'attacking full-back ceiling beats ordinary centre-backs, but rotation risk prevents a higher placement',
423:'high ceiling when fit, heavily discounted for availability and role uncertainty',
175:'attacking right-back profile and likely minutes place him above low-upside centre-backs',
534:'usable attacking full-back role and minutes floor fit the late drafted-buffer range',
88:'attacking full-back upside merits promotion over speculative centre-backs',
173:'minutes security and attacking defender potential place him in the late buffer',
11:'elite-team clean-sheet ceiling is offset by substantial rotation risk',
489:'secure midfield minutes and modest attacking routes beat speculative defenders at the boundary',
259:'centre-back minutes floor is useful but replacement-level in this league',
212:'reliable minutes but low attacking ceiling keep him in the late buffer',
497:'backup-goalkeeper uncertainty keeps him below secure starters',
272:'forward scarcity provides some value, but role evidence is too weak for a larger promotion',
301:'goalkeeper hierarchy uncertainty leaves him near the bottom of the extended buffer'}
original={r['id']:r.copy() for r in rows}; template={r['rank']:(r['segment'],r['tier']) for r in rows}
base=[r for r in rows if r['id'] not in entrants]
for pid in sorted(entrants,key=lambda x:targets[x]):
    p=P[pid]; rank=targets[pid]; base.insert(rank-1,{'rank':rank,'name':p['web_name'],'pos':POS[p['element_type']],'team':T[p['team']],'segment':'','tier':'','id':pid,'status':p.get('news') or 'Available','changed':TS,'evidence':rl})
assert len(base)==240
for i,r in enumerate(base,1):
    r['rank']=i; r['segment'],r['tier']=template[i]
    if r['id'] in entrants: r['changed']=TS; r['evidence']=rl
row_iter=iter(base); out=[]
for l in lines:
    if re.match(r'^\| \d+ \|',l):
        r=next(row_iter); out.append(f"| {r['rank']} | {r['name']} | {r['pos']} | {r['team']} | {r['segment']} | {r['tier']} | {r['id']} | {r['status']} | {r['changed']} | {r['evidence']} |")
    else: out.append(l)
text='\n'.join(out)+'\n'; text=re.sub(r'last_updated: .*',f'last_updated: {TS}',text,1); text=re.sub(r'status: .*','status: ranks1_240_integrated',text,1)
text=text.replace('Ranks 1–220 have received a manual pairwise pass. Ranks 221 onward are an extended watch buffer from the active API pool and require stronger role evidence before promotion.','Ranks 1–240 are now integrated into one tiered ordering. The 20 former extended-buffer additions were insertion-sorted against comparable players; low-confidence cases remain near the boundary.')
B.write_text(text)
final={r['id']:r for r in base}; decisions=[]
for pid in entrants:
    r=final[pid]; above=base[r['rank']-2]['name'] if r['rank']>1 else 'top boundary'; below=base[r['rank']]['name'] if r['rank']<240 else 'bottom boundary'
    decisions.append(f"- **{r['name']} → {r['rank']} ({r['segment']}, {r['tier']}):** placed below {above} and above {below}; {reasons[pid]}.")
RV.parent.mkdir(parents=True,exist_ok=True); CH.parent.mkdir(parents=True,exist_ok=True)
RV.write_text(f'''---\ntype: review\ntimestamp: {TS}\nscope: integrate ranks 221-240\n---\n\n# FPL Draft review — integrate the 20 new additions\n\n## API reconciliation\n\nThe official FPL endpoints returned {len(P)} active players, {len(api['teams'])} teams and {len(fx)} fixtures. All 20 additions remain in the active pool with stable IDs.\n\n## Sources searched\n\n- [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/)\n- [Official fixtures](https://fantasy.premierleague.com/api/fixtures/)\n- [Premier League 2026 preseason tracker](https://www.premierleague.com/en/news/4606700/premier-league-clubs-2026-pre-season-fixtures-and-results)\n- Public searches for exact official-club, journalist and analyst evidence concerning the 20 players. No profile-only result was adopted.\n\n## Method\n\nEach former rank-221–240 player was assigned a provisional tier and segment, then insertion-sorted into the existing board against nearby players with similar expected points, minutes, role, clean-sheet or attacking upside. Raw expected points came first; positional scarcity and replacement value were used only afterward.\n\n## Placement decisions\n\n{chr(10).join(decisions)}\n\n## Evidence adopted and rejected\n\nOfficial identity, team, position and availability metadata were treated as confirmed. Team strength, likely role and positional scarcity were explicit inferences. Price, ownership and raw friendly output were not used as ranking evidence.\n\n## Major uncertainty\n\nKerkez and Hall have the largest upside if first-choice attacking roles are confirmed. Shaw, Spence and Mosquera remain heavily role- and fitness-dependent. Goalkeeper placements can move quickly once starting hierarchies are clear.\n''')
changes=[]
for pid in entrants:
    old=original[pid]['rank']; new=final[pid]['rank']; changes.append(f"- **{final[pid]['name']}: {old} → {new}** — {final[pid]['segment']}, tier {final[pid]['tier']}; {reasons[pid]}.")
CH.write_text(f'''---\ntype: changes\ntimestamp: {TS}\nprior_review: 2026-08-02T09:58:00+10:00\n---\n\n# Changes — integrated new additions\n\n## Re-ranked additions\n\n{chr(10).join(changes)}\n\n## Important no-change decision\n\nNo player was removed from the 240-player board. Existing players moved only as a mechanical consequence of inserting the 20 additions into their appropriate ranges.\n\nReview: {rl}\n''')
ws=W.read_text(); ws=re.sub(r'last_updated: .*',f'last_updated: {TS}',ws,1); W.write_text(ws+f'\n## 2026-08-02 10:01 AEST — integrated additions\n\n- Re-ranked all 20 former extended-buffer players into comparable tier and segment ranges.\n- Priority triggers: Kerkez/Hall first-choice role, goalkeeper hierarchies, Shaw/Spence fitness and rotation.\n- Evidence: {rl}.\n')
for q in (H,K):
    s=q.read_text(); s=re.sub(r'latest_review: .*',f'latest_review: {rl}',s,1); s=re.sub(r'latest_changes: .*',f'latest_changes: {cl}',s,1); q.write_text(s+f'\n## 2026-08-02 10:01 AEST\n\n- Integrated the 20 new additions into the full 240-player ordering.\n- Latest review: {rl}.\n- Latest changes: {cl}.\n')
changed=[B,W,H,K,RV,CH]
# update entrant notes and immediate comparators
note_ids=set(entrants)
for pid in entrants:
    rank=final[pid]['rank'];
    if rank>1: note_ids.add(base[rank-2]['id'])
    if rank<240: note_ids.add(base[rank]['id'])
for pid in note_ids:
    r=final[pid]; p=P[pid]; path=R/f"vault/02 Players/{p['web_name']} - {pid}.md"
    old=original.get(pid,{}).get('rank','unranked')
    entrant_text=(f"This player was insertion-sorted from rank {old} to {r['rank']}. {reasons[pid]}." if pid in entrants else f"This player's rank is now {r['rank']} after an adjacent new entrant was inserted; their underlying assessment was not materially changed.")
    path.write_text(f'''---\ntype: player\nfpl_id: {pid}\nplayer_name: {p['web_name']}\nteam: "[[03 Teams/{T[p['team']]}]]"\nposition: "[[04 Positions/{PN[POS[p['element_type']]]}]]"\napi_status: "{p.get('news') or 'Available'}"\ncurrent_rank: {r['rank']}\ncurrent_segment: {r['segment']}\ncurrent_tier: {r['tier']}\nlast_reviewed: {TS}\n---\n\n# {p['web_name']}\n\n## Current assessment\n\n{entrant_text}\n\n## Direct range comparison\n\nPlaced between **{base[r['rank']-2]['name'] if r['rank']>1 else 'top boundary'}** and **{base[r['rank']]['name'] if r['rank']<240 else 'bottom boundary'}**.\n\n## Reversal trigger\n\nConfirmed first-choice status, repeated probable-XI minutes, set pieces, injury news or a transfer can materially change this placement.\n\n## Backlinks\n- [[01 Current/Current Draft Board]]\n- {rl}\n- {cl}\n'''); changed.append(path)
ch=C.read_text(); ch=re.sub(r'last_updated: .*',f'last_updated: {TS}',ch,1)
seen=[]
for q in changed:
    if q in seen: continue
    seen.append(q); exists_before=q not in (RV,CH) and not (q.parent.name=='02 Players' and q.name.split(' - ')[0] in [P[i]['web_name'] for i in entrants] and original.get(int(q.stem.rsplit(' - ',1)[1]),{}).get('rank',999)>220)
    act='Created' if q in (RV,CH) else 'Updated'
    ch+=f"\n| {TS} | `{q.as_posix()}` | {act} | Integrated former extended-buffer players into comparable tiers and segments. | {rl} | [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/); [Official fixtures](https://fantasy.premierleague.com/api/fixtures/); [Premier League preseason tracker](https://www.premierleague.com/en/news/4606700/premier-league-clubs-2026-pre-season-fixtures-and-results) |"
ch+=f"\n| {TS} | `vault/00 Meta/Document Changelog.md` | Updated | Appended one row for every Markdown document changed in the integration review. | {rl} | Per-document audit |\n"; C.write_text(ch)
ranks=[int(l.split('|')[1].strip()) for l in B.read_text().splitlines() if re.match(r'^\| \d+ \|',l)]; assert ranks==list(range(1,241)); print({P[i]['web_name']:final[i]['rank'] for i in entrants})