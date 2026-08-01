from pathlib import Path
import json, urllib.request, re

TS='2026-08-02T08:48:00+10:00'
STAMP='0848-AEST'
ROOT=Path('.')
BOARD=ROOT/'vault/01 Current/Current Draft Board.md'
WATCH=ROOT/'vault/01 Current/Current Watchlist.md'
HOME=ROOT/'vault/Home.md'
WIKI=ROOT/'vault/Wiki.md'
CHANGELOG=ROOT/'vault/00 Meta/Document Changelog.md'
REVIEW=ROOT/'vault/06 Reviews/2026/08/2026-08-02/0848-AEST-review.md'
CHANGES=ROOT/'vault/07 Changes/2026/08/2026-08-02/0848-AEST-changes.md'
review_link='[[06 Reviews/2026/08/2026-08-02/0848-AEST-review]]'
changes_link='[[07 Changes/2026/08/2026-08-02/0848-AEST-changes]]'

with urllib.request.urlopen('https://fantasy.premierleague.com/api/bootstrap-static/', timeout=30) as r:
    api=json.load(r)
with urllib.request.urlopen('https://fantasy.premierleague.com/api/fixtures/', timeout=30) as r:
    fixtures=json.load(r)
players={p['id']:p for p in api['elements']}
teams={t['id']:t['short_name'] for t in api['teams']}
pos={1:'GKP',2:'DEF',3:'MID',4:'FWD'}

text=BOARD.read_text()
rows=[]
for line in text.splitlines():
    if re.match(r'^\| \d+ \|',line):
        c=[x.strip() for x in line.strip('|').split('|')]
        rows.append({'line':line,'rank':int(c[0]),'name':c[1],'pos':c[2],'team':c[3],'segment':c[4],'tier':c[5],'id':int(c[6]),'status':c[7]})
byid={r['id']:r for r in rows}

order=[222,224,170,16,482,372,41,519,549,102,105,461,53,98,78,377,118,93,117,119,153,150,92,120,504]
assert len(order)==25 and len(set(order))==25
for pid in order:
    assert pid in players, f'missing API id {pid}'
old_rank={r['id']:r['rank'] for r in rows}
for rank,pid in enumerate(order,196):
    r=byid[pid]
    p=players[pid]
    r.update(rank=rank,name=p['web_name'],pos=pos[p['element_type']],team=teams[p['team']],segment='Undrafted buffer',tier='Watch',status=(p.get('news') or 'Available'))
# all other rows retain rank, but replace the 196-220 slots with selected players and move displaced pool members according to order
pool_ids=[r['id'] for r in rows if 196<=r['rank']<=220]
assert set(pool_ids)==set(order), (set(pool_ids)-set(order),set(order)-set(pool_ids))

line_by_old={r['line']:r for r in rows}
out=[]
for line in text.splitlines():
    if line in line_by_old:
        r=line_by_old[line]
        if r['id'] in order:
            out.append(f"| {r['rank']} | {r['name']} | {r['pos']} | {r['team']} | {r['segment']} | {r['tier']} | {r['id']} | {r['status']} | {TS} | {review_link} |")
        else: out.append(line)
    else: out.append(line)
text='\n'.join(out)+'\n'
text=text.replace('Ranks 1–170 have now received a manual pairwise pass; ranks 171–220 retain the prior relative order unless official metadata changed.','Ranks 1–220 have now received a manual pairwise pass. The full active API pool remains screened for entrants each run.')
BOARD.write_text(text)

ranked_ids={r['id'] for r in rows}
unranked=[]
for p in api['elements']:
    if p['id'] not in ranked_ids:
        score=float(p.get('selected_by_percent') or 0)*10 + p.get('now_cost',0)
        unranked.append((score,p['web_name'],pos[p['element_type']],teams[p['team']],p['id'],p.get('news') or 'Available'))
unranked=sorted(unranked,reverse=True)[:15]
screen='\n'.join(f"- {n} ({po}, {tm}, FPL ID {pid}) — API status: {st}. Screened but not promoted without reliable minutes/role evidence." for _,n,po,tm,pid,st in unranked)

comparisons=[
('Strand Larsen','Nketiah','stronger current central-forward floor and scarcity value'),
('Nketiah','Emegha','more proven Premier League scoring ceiling; Emegha retains injury and hierarchy risk'),
('Emegha','Madueke','forward scarcity narrowly reverses a close raw-points comparison despite hamstring risk'),
('Madueke','Hudson-Odoi','higher team-context ceiling, while both require role and fitness confirmation'),
('Hudson-Odoi','Mac Allister','greater direct attacking ceiling when fit'),
('Mac Allister','Buendía','safer minutes and set-piece accumulation'),
('Buendía','Gallagher','more direct creative routes, but lower minutes certainty'),
('Gallagher','Talbi','stronger demonstrated top-flight floor'),
('Talbi','Yarmoliuk','more direct attacking upside'),
('Yarmoliuk','Anthony','slightly safer central involvement'),
('Anthony','Touré','clearer immediate attacking role signal'),
('Touré','Manzambi','higher ceiling, with both role-dependent'),
('Manzambi','Janelt','greater upside beats the safer low ceiling'),
('Janelt','Kroupi.Jr','availability wins over unknown-return foot injury'),
('Kroupi.Jr','Munoz','injury-discounted attacking ceiling still exceeds a speculative role'),
('Munoz','Igor','midfield upside narrowly beats ordinary defender replacement value'),
('Igor','Schuster','more established defensive role floor'),
('Schuster','Coppola','slightly clearer route to usable minutes'),
('Coppola','Costinha','marginal role preference'),
('Costinha','Disasi','upside preference over unresolved Chelsea centre-back hierarchy'),
('Disasi','M.Sarr','greater demonstrated senior minutes'),
('M.Sarr','Ji-soo','elite-club clean-sheet ceiling, heavily rotation-discounted'),
('Ji-soo','Svoboda','cleaner route to useful minutes'),
('Svoboda','Vuskovic','marginal availability and hierarchy preference')]
comp_md='\n'.join(f'- **{a} over {b}:** {why}.' for a,b,why in comparisons)

REVIEW.parent.mkdir(parents=True,exist_ok=True)
REVIEW.write_text(f'''---\ntype: review\ntimestamp: {TS}\ntarget_block: 201-220\nchallengers: 196-full API pool\n---\n\n# FPL Draft review — ranks 201–220\n\n## API reconciliation\n\nThe official FPL bootstrap and fixtures endpoints returned {len(players)} active players, {len(api['teams'])} teams and {len(fixtures)} fixtures. All 25 ranked candidates in positions 196–220 remained present with stable FPL IDs. The full unranked API pool was screened for possible entrants; no player was promoted solely from price or ownership signals.\n\n## Sources searched\n\n- [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/) and [fixtures](https://fantasy.premierleague.com/api/fixtures/).\n- [Premier League 2026 preseason fixture/results tracker](https://www.premierleague.com/en/news/4606700/premier-league-clubs-2026-pre-season-fixtures-and-results).\n- Public searches for exact posts from Planet FPL/James Linden, Ben Crellin and equivalent fixture specialists, Sam Martin, Fabrizio Romano, official clubs, reliable club journalists, tactical analysts and supporter communities.\n\nPublic X indexing remained incomplete. No profile-only result was adopted, and no exact newly indexed post supplied sufficiently specific role, injury, set-piece or completed-transfer evidence to add an unranked API player.\n\n## Full-pool entrant screen\n\n{screen}\n\n## Pairwise method\n\nRanks 201–220 were sorted with challengers from 196–200 and every active API player outside the top 220. Raw expected points were considered first, then minutes, role, set pieces, injuries and rotation. Positional scarcity was applied only afterward.\n\n## Decisive comparisons\n\n{comp_md}\n\n## Evidence adopted\n\nOfficial identity, club, position and availability metadata were treated as confirmed facts. Forward scarcity was applied after expected-points assessment. Players with direct attacking roles were preferred to speculative centre-backs at the bottom of the board.\n\n## Evidence rejected\n\nAPI price and ownership were used only to make the full-pool screen tractable, not as ranking evidence. Raw friendly outputs, unsupported lineup claims, transfer speculation below advanced status and profile-only X results were rejected.\n\n## Close calls and reversal triggers\n\nEmegha, Hudson-Odoi and Kroupi can rise on fitness. Strand Larsen and Nketiah need confirmed first-team striker roles. Madueke, Buendía, Gallagher and the young midfielders need repeated strongest-XI minutes. Any unranked API player with a confirmed starting role, penalties or advanced transfer can enter above rank 220 immediately.\n\n## Completion state\n\nThe first manual pairwise pass now covers ranks 1–220. Future hourly runs should revisit the highest-impact uncertainty rather than mechanically repeat completed blocks.\n''')

CHANGES.parent.mkdir(parents=True,exist_ok=True)
risers=[];fallers=[]
for pid in order:
    nr=byid[pid]['rank']; orank=old_rank[pid]; name=players[pid]['web_name']
    (risers if nr<orank else fallers if nr>orank else []).append(f'- {name}: {orank} → {nr}')
CHANGES.write_text(f'''---\ntype: changes\ntimestamp: {TS}\nprior_review: 2026-08-02T08:41:00+10:00\n---\n\n# Changes — ranks 201–220\n\n## Material risers\n\n{chr(10).join(risers) or '- None.'}\n\n## Material fallers\n\n{chr(10).join(fallers) or '- None.'}\n\n## Entrants and removals\n\nNo player entered or left the active top 220. The complete active API pool was screened; no unranked player had sufficiently specific current role evidence to displace the ranked buffer.\n\n## Injury, transfer and role changes\n\nExisting injury discounts remain for Emegha, Hudson-Odoi and Kroupi. No completed transfer, advanced agreement or official role update changed the pool.\n\n## Important no-change decisions\n\nThe top 195 were not moved. Price and ownership signals did not create entrants. Speculative elite-club defenders remained below attacking players with plausible usable roles.\n\n## Watchlist changes\n\nAdded full-pool entrant triggers and retained fitness/role triggers for the late attacking candidates.\n\nReview: {review_link}\n''')

watch=WATCH.read_text()
watch=watch.replace('last_updated:', 'last_updated:',1)
watch=re.sub(r'last_updated: .*',f'last_updated: {TS}',watch,count=1)
watch += f'''\n## 2026-08-02 08:48 AEST — final board block\n\n- Strand Larsen and Nketiah: confirm first-team central-forward hierarchy.\n- Emegha, Hudson-Odoi and Kroupi.Jr: obtain direct fitness and return-to-training evidence.\n- Madueke, Buendía and Gallagher: monitor repeated strongest-XI role and set pieces.\n- Full API pool: promote any unranked player only on confirmed starting role, penalties, advanced transfer or repeated first-team minutes.\n- Evidence: {review_link}.\n'''
WATCH.write_text(watch)

for path in (HOME,WIKI):
    s=path.read_text()
    s=re.sub(r'latest_review: .*',f'latest_review: {review_link}',s,count=1)
    s=re.sub(r'latest_changes: .*',f'latest_changes: {changes_link}',s,count=1)
    s += f'''\n## 2026-08-02 08:48 AEST\n\n- Completed the first manual pairwise pass across ranks 1–220.\n- Final block: ranks 201–220, challenged against ranks 196–200 and the full active API pool.\n- Latest review: {review_link}.\n- Latest changes: {changes_link}.\n'''
    path.write_text(s)

# player notes for all 25 assessed candidates
changed=[BOARD,WATCH,HOME,WIKI,REVIEW,CHANGES]
for rank,pid in enumerate(order,196):
    p=players[pid]; name=p['web_name']; path=ROOT/f'vault/02 Players/{name} - {pid}.md'
    prev=players[order[rank-197]]['web_name'] if rank>196 else 'rank 195 boundary'
    nxt=players[order[rank-195]]['web_name'] if rank<220 else 'full API pool boundary'
    status=p.get('news') or 'Available'
    path.write_text(f'''---\ntype: player\nfpl_id: {pid}\nplayer_name: {name}\nteam: "[[03 Teams/{teams[p['team']]}]]"\nposition: "[[04 Positions/{'Goalkeeper' if pos[p['element_type']]=='GKP' else 'Defender' if pos[p['element_type']]=='DEF' else 'Midfielder' if pos[p['element_type']]=='MID' else 'Forward'}]]"\napi_status: "{status}"\ncurrent_rank: {rank}\ncurrent_segment: Undrafted buffer\nlast_reviewed: {TS}\n---\n\n# {name}\n\n## Current assessment\n\nRanked {rank} after the final 201–220 pairwise review and full active API-pool screen. Raw expected points were assessed before positional scarcity.\n\n## Pairwise placement\n\n- Immediate comparison: **{prev} / {nxt}**.\n- Decision: placed after direct comparison of expected points, minutes, role, set pieces, injury/rotation risk and replacement value.\n- Confidence: low to medium; this range is outside the 160-player draft line.\n- Reversal trigger: confirmed first-team role, fitness, penalties, repeated strongest-XI minutes or completed transfer evidence.\n\n## Evidence timeline\n\n- 2026-08-02 08:48 AEST — ranked {old_rank[pid]} → {rank} in the stable pairwise pass.\n- [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/)\n- [Official fixtures](https://fantasy.premierleague.com/api/fixtures/)\n- [Premier League preseason tracker](https://www.premierleague.com/en/news/4606700/premier-league-clubs-2026-pre-season-fixtures-and-results)\n\n## Backlinks\n\n- [[01 Current/Current Draft Board]]\n- {review_link}\n- {changes_link}\n''')
    changed.append(path)

cl=CHANGELOG.read_text()
cl=re.sub(r'last_updated: .*',f'last_updated: {TS}',cl,count=1)
for path in changed:
    action='Created' if path in (REVIEW,CHANGES) or old_rank.get(next((pid for pid in order if f' - {pid}.md' in str(path)),None),None) is None else 'Updated'
    if 'Players/' in str(path): action='Updated' if path.exists() else 'Created'
    rel=str(path).replace('\\','/')
    cl += f"\n| {TS} | `{rel}` | {action} | Recorded ranks 201–220 pairwise review with full active API-pool challenge. | {review_link} | [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/); [Official fixtures](https://fantasy.premierleague.com/api/fixtures/); [Premier League preseason tracker](https://www.premierleague.com/en/news/4606700/premier-league-clubs-2026-pre-season-fixtures-and-results) |"
cl += f"\n| {TS} | `vault/00 Meta/Document Changelog.md` | Updated | Appended a separate audit row for every Markdown file changed by the final board review. | {review_link} | Per-document audit; [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/) |\n"
CHANGELOG.write_text(cl)

# validations
board_rows=[]
for line in BOARD.read_text().splitlines():
    if re.match(r'^\| \d+ \|',line): board_rows.append(int(line.split('|')[1].strip()))
assert board_rows==list(range(1,221))
assert len(set(board_rows))==220
for p in changed:
    assert str(p).replace('\\','/') in CHANGELOG.read_text()
print('generated',len(changed)+1,'markdown files; api',len(players),'fixtures',len(fixtures))
