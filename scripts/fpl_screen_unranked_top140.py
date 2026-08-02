from pathlib import Path
import json,re,urllib.request
TS='2026-08-02T10:12:00+10:00'; stamp='1012-AEST'; R=Path('.')
B=R/'vault/01 Current/Current Draft Board.md'; W=R/'vault/01 Current/Current Watchlist.md'; H=R/'vault/Home.md'; K=R/'vault/Wiki.md'; C=R/'vault/00 Meta/Document Changelog.md'
RV=R/'vault/06 Reviews/2026/08/2026-08-02/1012-AEST-review.md'; CH=R/'vault/07 Changes/2026/08/2026-08-02/1012-AEST-changes.md'
rl='[[06 Reviews/2026/08/2026-08-02/1012-AEST-review]]'; cl='[[07 Changes/2026/08/2026-08-02/1012-AEST-changes]]'
with urllib.request.urlopen('https://fantasy.premierleague.com/api/bootstrap-static/',timeout=30) as r: api=json.load(r)
with urllib.request.urlopen('https://fantasy.premierleague.com/api/fixtures/',timeout=30) as r: fx=json.load(r)
P={p['id']:p for p in api['elements']}; T={t['id']:t['short_name'] for t in api['teams']}; POS={1:'GKP',2:'DEF',3:'MID',4:'FWD'}; PN={'GKP':'Goalkeeper','DEF':'Defender','MID':'Midfielder','FWD':'Forward'}
insertions=[(78,357),(85,18),(96,494),(108,116),(110,233),(114,457),(118,262),(123,97),(129,254),(132,167),(134,144),(136,115),(138,330),(140,157)]
text=B.read_text(); lines=text.splitlines(); rows=[]; start=None; end=None
for i,l in enumerate(lines):
    if re.match(r'^\| \d+ \|',l):
        if start is None:start=i
        c=[x.strip() for x in l.strip('|').split('|')]; rows.append({'rank':int(c[0]),'player':c[1],'pos':c[2],'team':c[3],'segment':c[4],'tier':c[5],'id':int(c[6]),'status':c[7],'changed':c[8],'evidence':c[9]}); end=i
ranked={r['id'] for r in rows}; assert len(rows)==240
for _,pid in insertions: assert pid in P and pid not in ranked
for target,pid in insertions:
    p=P[pid]; rows.insert(target-1,{'rank':target,'player':p['web_name'],'pos':POS[p['element_type']],'team':T[p['team']],'segment':'','tier':'','id':pid,'status':p.get('news') or 'Available','changed':TS,'evidence':rl})

def classify(rank,old_tier='Watch'):
    if rank<=8:return ('Franchise',old_tier)
    if rank<=32:return ('Foundation',old_tier)
    if rank<=63:return ('Core',old_tier)
    if rank<=79:return ('Core','C+')
    if rank<=124:return ('Depth','C')
    if rank<=160:return ('Endgame','D+')
    if rank<=220:return ('Undrafted buffer', 'D' if old_tier!='Watch' else 'Watch')
    return ('Extended watch buffer','Watch')
for n,r in enumerate(rows,1):
    r['rank']=n; r['segment'],r['tier']=classify(n,r['tier'])
newrows=[f"| {r['rank']} | {r['player']} | {r['pos']} | {r['team']} | {r['segment']} | {r['tier']} | {r['id']} | {r['status']} | {r['changed']} | {r['evidence']} |" for r in rows]
lines[start:end+1]=newrows
text='\n'.join(lines)+'\n'; text=re.sub(r'ranking_depth: \d+','ranking_depth: 254',text,1); text=re.sub(r'last_updated: .*',f'last_updated: {TS}',text,1); text=re.sub(r'status: .*','status: full_pool_top140_omissions_integrated',text,1); B.write_text(text)

comparators={357:'Dorgu',18:'Hall',494:'Petrović',116:'Keane',233:'Dunk',457:'Beto',262:'N.Jackson',97:'Tonali',254:'Konsa',167:'Gusto',144:'De Cuyper',115:'Bogle',330:'Estêvão',157:'Spence'}
reasons={357:'elite-team attacking full-back ceiling outweighs rotation risk',18:'higher direct goal ceiling than the goalkeeper/defender cluster, but role risk prevents a Core placement',494:'secure starting-goalkeeper floor belongs with the established goalkeeper cluster',116:'durable minutes and aerial/clean-sheet floor beat lower-certainty centre-backs',233:'secure full-back minutes and attacking routes justify Depth placement',457:'direct attacking role and proven returns beat lower-ceiling midfield depth',262:'creative and goal routes merit a Depth slot, discounted for competition',97:'set-piece and creative accumulation beat lower-ceiling central midfielders',254:'attacking full-back upside beats ordinary centre-back replacement value',167:'forward scarcity and scoring ceiling merit late top-140 inclusion despite Chelsea competition',144:'attacking Chelsea full-back upside narrowly beats the late defensive cluster',115:'attacking role and Brighton clean-sheet potential justify Endgame placement',330:'secure attacking full-back minutes beat speculative defenders',157:'elite attacking ceiling earns the final top-140 slot, heavily rotation-discounted'}
changed=[B]
for r in rows:
    if r['rank']<78: continue
    matches=list((R/'vault/02 Players').glob(f"* - {r['id']}.md")); q=matches[0] if matches else R/f"vault/02 Players/{r['player']} - {r['id']}.md"
    if q.exists():
        s=q.read_text(); s=re.sub(r'current_rank: \d+',f"current_rank: {r['rank']}",s,1); s=re.sub(r'current_segment: .*',f"current_segment: {r['segment']}",s,1); s=re.sub(r'last_reviewed: .*',f'last_reviewed: {TS}',s,1)
        if rl not in s:s+=f"\n## 2026-08-02 10:12 AEST\n\nRank updated to {r['rank']} after the unranked-player top-140 screen. Evidence: {rl}.\n"
    else:
        p=P[r['id']]; s=f'''---\ntype: player\nfpl_id: {r['id']}\nplayer_name: {r['player']}\nteam: "[[03 Teams/{r['team']}]]"\nposition: "[[04 Positions/{PN[r['pos']]}]]"\napi_status: "{r['status']}"\ncurrent_rank: {r['rank']}\ncurrent_segment: {r['segment']}\nlast_reviewed: {TS}\n---\n\n# {r['player']}\n\nInserted at rank {r['rank']} after the full unranked-player screen. Compared with {comparators.get(r['id'],'nearby peers')}: {reasons.get(r['id'],'placement reflects expected points, role and replacement value')}.\n\n## Backlinks\n- [[01 Current/Current Draft Board]]\n- {rl}\n- {cl}\n'''
    q.write_text(s); changed.append(q)

placements='\n'.join(f"- **{P[pid]['web_name']} → {target}** ({POS[P[pid]['element_type']]}, {T[P[pid]['team']]}) — compared with {comparators[pid]}; {reasons[pid]}." for target,pid in insertions)
RV.parent.mkdir(parents=True,exist_ok=True); CH.parent.mkdir(parents=True,exist_ok=True)
RV.write_text(f'''---\ntype: review\ntimestamp: {TS}\nscope: unranked players challenging top 140\n---\n\n# FPL Draft review — unranked top-140 screen\n\n## API reconciliation\n\nThe official FPL endpoints returned {len(P)} active players, {len(api['teams'])} teams and {len(fx)} fixtures. The 240 ranked IDs were reconciled against the active pool before screening all omitted players.\n\n## Screening method\n\nThe full omitted pool was first triaged using current FPL metadata and prior-season minutes/points only as a discovery aid. Candidates were then assessed for expected minutes, role, set pieces, attacking or clean-sheet routes, injury and rotation risk, floor, ceiling and positional replacement value. Raw screening score did not determine final rank.\n\n## Players inserted into the top 140\n\n{placements}\n\n## High-profile rejects\n\n- **Xavi:** unknown-return knee injury and uncertain role prevented promotion.\n- **Rodri:** unknown-return back injury and defensive-midfield scoring profile prevented promotion.\n- **Tielemans:** hamstring flag and uncertain advanced/set-piece share prevented promotion.\n- **Mainoo, Joelinton, Kamada, Lerma and similar central midfielders:** useful minutes floors but insufficient attacking ceiling versus the existing top-140 boundary.\n- **Robertson, Maatsen, Yoro and other defenders:** retained outside the top 140 because current role certainty or attacking upside was weaker than the selected entrants.\n\n## Evidence adopted\n\nOfficial identity, team, position, availability, prior minutes and prior points were treated as confirmed API metadata. Team strength, likely role and draft scarcity were explicit inferences.\n\n## Evidence rejected\n\nPrice, ownership and the triage score were not used as ranking evidence. Profile-only social results, unsupported lineup claims and raw friendly output were rejected.\n\n## Uncertainty and reversal triggers\n\nFrimpong, Martinelli, Gusto, Estêvão and Delap can move sharply with confirmed strongest-XI roles. Vicario, Dunk and Mykolenko have safer floors. A clear role loss, transfer, injury or set-piece change can reverse any insertion.\n\n## Sources\n\n- [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/)\n- [Official fixtures](https://fantasy.premierleague.com/api/fixtures/)\n- [Premier League preseason tracker](https://www.premierleague.com/en/news/4606700/premier-league-clubs-2026-pre-season-fixtures-and-results)\n''')
CH.write_text(f'''---\ntype: changes\ntimestamp: {TS}\nprior_review: 2026-08-02T10:01:00+10:00\n---\n\n# Changes — omitted-player top-140 integration\n\nFourteen previously unranked active players were inserted into the top 140. The board expanded from 240 to 254 so no existing watch case was silently removed.\n\n## Entrants\n\n{placements}\n\n## Boundary impact\n\nExisting players at and below rank 78 moved down mechanically. The top 77 did not change. The new rank-140 boundary is Estêvão; prior boundary players moved below it rather than being deleted.\n\n## No-add decisions\n\nNo other omitted player had sufficient current expected points, role certainty or scarcity value to enter the top 140.\n\nReview: {rl}\n''')
changed += [RV,CH]
ws=W.read_text(); ws=re.sub(r'last_updated: .*',f'last_updated: {TS}',ws,1); ws+=f'\n## 2026-08-02 10:12 AEST — omitted-player screen\n\n- Added 14 previously omitted active players inside the top 140.\n- Highest-upside role checks: Frimpong, Martinelli, Gusto, Estêvão and Delap.\n- Evidence: {rl}.\n'; W.write_text(ws); changed.append(W)
for p in (H,K):
    s=p.read_text(); s=re.sub(r'latest_review: .*',f'latest_review: {rl}',s,1); s=re.sub(r'latest_changes: .*',f'latest_changes: {cl}',s,1); s+=f'\n## 2026-08-02 10:12 AEST\n\n- Screened every active player omitted from the 240-player board and inserted 14 credible top-140 candidates.\n- Latest review: {rl}.\n- Latest changes: {cl}.\n'; p.write_text(s); changed.append(p)
ch=C.read_text(); ch=re.sub(r'last_updated: .*',f'last_updated: {TS}',ch,1)
seen=[]
for q in changed:
    if q in seen: continue
    seen.append(q); act='Created' if q in (RV,CH) or (q.parent.name=='02 Players' and q.stat().st_size<800) else 'Updated'
    ch+=f"\n| {TS} | `{q.as_posix()}` | {act} | Recorded the full omitted-player top-140 screen and rank consequences. | {rl} | [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/); [Official fixtures](https://fantasy.premierleague.com/api/fixtures/); [Premier League preseason tracker](https://www.premierleague.com/en/news/4606700/premier-league-clubs-2026-pre-season-fixtures-and-results) |"
ch+=f"\n| {TS} | `vault/00 Meta/Document Changelog.md` | Updated | Appended one audit row per changed Markdown file. | {rl} | Per-document audit |\n"; C.write_text(ch)
ranks=[int(l.split('|')[1].strip()) for l in B.read_text().splitlines() if re.match(r'^\| \d+ \|',l)]; assert ranks==list(range(1,255)); assert all(pid in [r['id'] for r in rows[:140]] for _,pid in insertions)
print({'depth':254,'inserted':[(P[i]['web_name'],n) for n,i in insertions]})
