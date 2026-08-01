from pathlib import Path
import re

TS='2026-08-02T08:30:00+10:00'; HM='0830'; DATE='2026-08-02'
REV='06 Reviews/2026/08/2026-08-02/0830-AEST-review'
CHG='07 Changes/2026/08/2026-08-02/0830-AEST-changes'
review_link=f'[[{REV}]]'; changes_link=f'[[{CHG}]]'
root=Path('vault')
board_path=root/'01 Current/Current Draft Board.md'
board=board_path.read_text()
rows=[]
for line in board.splitlines():
    if re.match(r'^\| \d+ \|', line):
        p=[x.strip() for x in line.strip('|').split('|')]
        rows.append({'rank':int(p[0]),'player':p[1],'pos':p[2],'team':p[3],'segment':p[4],'tier':p[5],'id':int(p[6]),'status':p[7],'changed':p[8],'evidence':p[9]})
by_rank={r['rank']:r for r in rows}
old={r['player']:r['rank'] for r in rows}
order=['Beto','N.Jackson','Brobbey','Scott','Cash','McGinn','Rashford','Sessegnon','Aït-Nouri','Botman','Hill','Alderete','Thiaw','Wieffer','Hincapie','N.Williams','Bassey','Van den Berg','Zubimendi','Canvot','Andersen','Grealish','Ekitiké','Verbruggen','Lammens','Sels','Wilson','Kinsky','Van de Ven','Aaronson','Dalot','Ayari','Hinshelwood','Livramento','Boscagli','Justin','Palestra','Caicedo','Burn','Garner']
pool={r['player']:r for r in rows if 106<=r['rank']<=145}
assert set(order)==set(pool), (set(order)-set(pool),set(pool)-set(order))
newrows=[]
for rank in range(1,221):
    if 106<=rank<=145:
        r=pool[order[rank-106]].copy(); r['rank']=rank; r['changed']=TS; r['evidence']=review_link
        r['segment']='Depth' if rank<=128 else 'Endgame'; r['tier']='C' if rank<=128 else 'D+'
        newrows.append(r)
    else:
        newrows.append(by_rank[rank])
header,tail=board.split('## Advised order',1)
pre,rest=tail.split('|---:|---|---|---|---|---|---:|---|---|---|',1)
_,cautions=rest.split('## Method cautions',1)
header=re.sub(r'last_updated: .*',f'last_updated: {TS}',header)
header=re.sub(r'status: .*','status: ranks111_140_pairwise_sorted',header)
header=re.sub(r'The first 110 have now been manually stable-sorted; this run reviewed ranks 81–110 with challengers from 76–115\.', 'The first 140 have now been manually stable-sorted; this run reviewed ranks 111–140 with challengers from 106–145.', header)
out=header+'## Advised order'+pre+'|---:|---|---|---|---|---|---:|---|---|---|\n'
for r in newrows:
    out+=f"| {r['rank']} | {r['player']} | {r['pos']} | {r['team']} | {r['segment']} | {r['tier']} | {r['id']} | {r['status']} | {r['changed']} | {r['evidence']} |\n"
out+='## Method cautions'+cautions
out=out.replace('The top 80 have been manually pairwise sorted; ranks 81-220 retain the prior relative order unless official metadata changed.','Ranks 1–140 have now received a manual pairwise pass; ranks 141–220 retain the prior relative order unless official metadata changed.')
board_path.write_text(out)

comparisons={
'Beto':'N.Jackson','N.Jackson':'Brobbey','Brobbey':'Scott','Scott':'Cash','Cash':'McGinn','McGinn':'Rashford','Rashford':'Sessegnon','Sessegnon':'Aït-Nouri','Aït-Nouri':'Botman','Botman':'Hill','Hill':'Alderete','Alderete':'Thiaw','Thiaw':'Wieffer','Wieffer':'Hincapie','Hincapie':'N.Williams','N.Williams':'Bassey','Bassey':'Van den Berg','Van den Berg':'Zubimendi','Zubimendi':'Canvot','Canvot':'Andersen','Andersen':'Grealish','Grealish':'Ekitiké','Ekitiké':'Verbruggen','Verbruggen':'Lammens','Lammens':'Sels','Sels':'Wilson','Wilson':'Kinsky','Kinsky':'Van de Ven','Van de Ven':'Aaronson','Aaronson':'Dalot','Dalot':'Ayari','Ayari':'Hinshelwood','Hinshelwood':'Livramento','Livramento':'Boscagli','Boscagli':'Justin','Justin':'Palestra','Palestra':'Caicedo','Caicedo':'Burn','Burn':'Garner','Garner':'next challenger'}
notes=[]
for rank in range(106,146):
    r=newrows[rank-1]; name=r['player']; path=root/f"02 Players/{name} - {r['id']}.md"; action='Updated' if path.exists() else 'Created'
    raw='Higher expected season points and/or safer usable minutes.'
    if name in {'Beto','N.Jackson','Brobbey','Ekitiké'}: raw='Forward scarcity supports the pick after first assessing expected points and availability.'
    if name=='Ekitiké': raw='Elite ceiling remains, but the unknown-return Achilles flag creates a major availability discount.'
    if name=='Andersen': raw='Reliable season role is retained despite the opening suspension.'
    if name=='Garner': raw='The groin return-date uncertainty pushes him to the bottom of this pool.'
    content=f'''---\ntype: player\nfpl_id: {r['id']}\nplayer_name: {name}\nteam: "[[03 Teams/{r['team']}]]"\nposition: "[[04 Positions/{'Forward' if r['pos']=='FWD' else 'Midfielder' if r['pos']=='MID' else 'Defender' if r['pos']=='DEF' else 'Goalkeeper'}]]"\napi_status: {r['status']}\ncurrent_rank: {rank}\ncurrent_segment: {r['segment']}\nlast_reviewed: {TS}\n---\n\n# {name}\n\n## Current assessment\n\nRanked {rank} after the ranks 111–140 review with challengers 106–145.\n\n## Pairwise placement\n\n- Compared with: **{comparisons[name]}**.\n- Decision: {raw}\n- Confidence: {'low' if name in {'Ekitiké','Grealish','Garner','Livramento'} else 'medium'}.\n- Reversal trigger: confirmed role, fitness, set pieces, transfer evidence or repeated probable-first-team minutes.\n\n## Evidence timeline\n\n- 2026-08-02 08:30 AEST — Pairwise-reviewed and placed at rank {rank}.\n- [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/)\n- [Official fixtures](https://fantasy.premierleague.com/api/fixtures/)\n- [Premier League preseason tracker](https://www.premierleague.com/en/news/4606700/premier-league-clubs-2026-pre-season-fixtures-and-results)\n\n## Backlinks\n\n- [[01 Current/Current Draft Board]]\n- {review_link}\n- {changes_link}\n'''
    path.parent.mkdir(parents=True,exist_ok=True); path.write_text(content); notes.append((path,action,name))

review=root/f'06 Reviews/2026/08/2026-08-02/{HM}-AEST-review.md'; review.parent.mkdir(parents=True,exist_ok=True)
review.write_text(f'''---\ntype: review\ntimestamp: {TS}\ntarget_block: 111-140\nchallengers: 106-145\n---\n\n# FPL Draft review — ranks 111–140\n\n## API reconciliation\n\nThe current canonical board and official FPL IDs were retained. The official bootstrap and fixtures endpoints remain authoritative for player identity, position, club and availability metadata. All 40 players in ranks 106–145 remained active board cases.\n\n## Sources searched\n\n- Official FPL bootstrap, fixtures and player-summary endpoints.\n- Premier League preseason fixture/results tracker and club channels.\n- Public searches for Planet FPL/James Linden, Ben Crellin and equivalent fixture specialists, Sam Martin, Fabrizio Romano, club journalists, tactical analysts and supporter communities.\n\nPublic X indexing remained incomplete. No inaccessible or profile-only item was treated as evidence. No newly indexed post supplied a sufficiently specific role, medical or transfer fact to override official metadata in this block.\n\n## Pairwise method\n\nThe target block was ranks 111–140 with challengers 106–145. Raw expected season points were considered first. Minutes, role, set pieces, injury and rotation risk were then assessed. Positional replacement value was applied only after that comparison.\n\n## Decisive comparisons\n\n- Beto over Nicolas Jackson: Beto has the clearer current route to central-forward minutes; forward scarcity supports both.\n- Nicolas Jackson over Brobbey: stronger proven Premier League ceiling, although Chelsea role competition limits confidence.\n- Brobbey over Scott: the forward scarcity adjustment reverses a close raw-points comparison.\n- Scott over Cash: more routes to attacking points; defender replacement remains deep.\n- Rashford over Sessegnon: higher attacking ceiling, but role security is not assumed.\n- Sessegnon over Aït-Nouri: safer current route to attacking full-back minutes.\n- Botman over Hill: stronger clean-sheet environment and role floor.\n- Hincapie over Neco Williams: Arsenal defensive ceiling outweighs Williams's attacking route.\n- Andersen over Grealish: reliable season-long role beats uncertain Manchester City attacking minutes despite the opening suspension.\n- Grealish over Ekitiké: current probability of usable minutes wins; this reverses immediately on a positive Ekitiké medical update.\n- Ekitiké over Verbruggen: forward ceiling and scarcity still beat another goalkeeper once injury risk is explicitly discounted.\n- Livramento over Boscagli: greater attacking ceiling, but calf fitness makes this low confidence.\n- Burn over Garner: immediate availability wins over Garner's groin return-date uncertainty.\n\n## Evidence adopted\n\nConfirmed official availability flags and current positions were adopted. Forward scarcity was used only as a second-stage draft-order adjustment. Secure goalkeeper minutes were valued, but the position remains replaceable in an eight-manager league.\n\n## Evidence rejected\n\nRaw friendly goals, assists and participation without probable-first-team context were rejected. Transfer speculation below advanced or completed status was not used. Account profiles without exact posts were not cited as evidence.\n\n## Close calls and reversal triggers\n\nEkitiké is the largest potential mover on medical clearance. Jackson, Rashford and Grealish require repeated first-team role evidence. Livramento and Garner require fitness confirmation. Goalkeepers from Verbruggen through Kinsky remain tightly grouped and can move with confirmed starting hierarchies.\n\n## Next block\n\nRanks 141–170 with challengers 136–175.\n''')
changes=root/f'07 Changes/2026/08/2026-08-02/{HM}-AEST-changes.md'; changes.parent.mkdir(parents=True,exist_ok=True)
movement=[]
for rank in range(106,146):
    n=newrows[rank-1]['player']; movement.append(f"| {n} | {old[n]} | {rank} | {'↑' if rank<old[n] else '↓' if rank>old[n] else '—'} |")
changes.write_text(f'''---\ntype: changes\ntimestamp: {TS}\nprior_review: "[[06 Reviews/2026/08/2026-08-02/0815-AEST-review]]"\n---\n\n# Changes — ranks 111–140\n\n## Rank movements\n\n| Player | Old | New | Direction |\n|---|---:|---:|---|\n'''+"\n".join(movement)+'''\n\n## Material changes\n\nBeto, Nicolas Jackson, Brobbey, Scott, Cash, McGinn, Rashford, Sessegnon and Aït-Nouri moved materially upward. Ekitiké remains heavily discounted by the unknown-return Achilles flag. Garner fell to the bottom of the reviewed pool because his return date remains uncertain.\n\n## Status, transfer and preseason changes\n\nNo new official status or high-confidence transfer event was found beyond the metadata already represented on the board. No friendly output alone caused a move.\n\n## Watchlist changes\n\nAdded explicit triggers for Ekitiké, Jackson, Rashford, Grealish, Livramento, Garner and the goalkeeper hierarchy.\n\n## Important no-change decisions\n\nRanks 1–105 and 146–220 retained their prior order. No player absent from the official API pool was promoted into the active board.\n''')

for p,title in [(root/'Home.md','Home'),(root/'Wiki.md','Wiki')]:
    txt=p.read_text(); txt=re.sub(r'last_updated: .*',f'last_updated: {TS}',txt,1)
    txt+=f"\n\n## 2026-08-02 08:30 AEST — ranks 111–140\n\n- Review: {review_link}\n- Changes: {changes_link}\n- Beto, Nicolas Jackson, Brobbey, Scott and attacking full-backs rose; Ekitiké and Garner remain injury-discounted.\n"
    p.write_text(txt)
watch=root/'01 Current/Current Watchlist.md'; wt=watch.read_text(); wt=re.sub(r'last_updated: .*',f'last_updated: {TS}',wt,1)
wt+=f"\n\n## 2026-08-02 08:30 AEST block triggers\n\n- Ekitiké: Achilles return-to-training and probable-first-team minutes.\n- Nicolas Jackson, Rashford and Grealish: repeated starting role and position.\n- Livramento and Garner: fitness confirmation.\n- Verbruggen, Lammens, Sels, Wilson and Kinsky: confirmed goalkeeper hierarchies.\n\nEvidence: {review_link}.\n"; watch.write_text(wt)

changed=[(board_path,'Updated'),(watch,'Updated'),(root/'Home.md','Updated'),(root/'Wiki.md','Updated'),(review,'Created'),(changes,'Created')]+[(p,a) for p,a,_ in notes]
cl=root/'00 Meta/Document Changelog.md'; ct=cl.read_text(); ct=re.sub(r'last_updated: .*',f'last_updated: {TS}',ct,1)
for p,a in changed:
    rel=p.as_posix(); ct+=f"\n| {TS} | `{rel}` | {a} | Recorded ranks 111–140 pairwise review with challengers 106–145. | {review_link} | [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/); [Official fixtures](https://fantasy.premierleague.com/api/fixtures/); [Premier League preseason tracker](https://www.premierleague.com/en/news/4606700/premier-league-clubs-2026-pre-season-fixtures-and-results) |"
ct+=f"\n| {TS} | `vault/00 Meta/Document Changelog.md` | Updated | Appended a separate audit row for every Markdown file changed by the ranks 111–140 review. | {review_link} | Per-document audit; [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/) |\n"
cl.write_text(ct)
print('generated',len(changed)+1,'markdown changes')
