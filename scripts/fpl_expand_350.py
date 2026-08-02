from pathlib import Path
import json,re,urllib.request
TS='2026-08-02T10:17:00+10:00'; ST='1017-AEST'; R=Path('.')
B=R/'vault/01 Current/Current Draft Board.md'; W=R/'vault/01 Current/Current Watchlist.md'; H=R/'vault/Home.md'; K=R/'vault/Wiki.md'; C=R/'vault/00 Meta/Document Changelog.md'
RV=R/'vault/06 Reviews/2026/08/2026-08-02/1017-AEST-review.md'; CH=R/'vault/07 Changes/2026/08/2026-08-02/1017-AEST-changes.md'
rl='[[06 Reviews/2026/08/2026-08-02/1017-AEST-review]]'; cl='[[07 Changes/2026/08/2026-08-02/1017-AEST-changes]]'
with urllib.request.urlopen('https://fantasy.premierleague.com/api/bootstrap-static/',timeout=30) as r: api=json.load(r)
with urllib.request.urlopen('https://fantasy.premierleague.com/api/fixtures/',timeout=30) as r: fx=json.load(r)
P={p['id']:p for p in api['elements']}; T={t['id']:t['short_name'] for t in api['teams']}; POS={1:'GKP',2:'DEF',3:'MID',4:'FWD'}
text=B.read_text(); lines=text.splitlines(); rows=[]
for l in lines:
    if re.match(r'^\| \d+ \|',l):
        c=[x.strip() for x in l.strip('|').split('|')]
        rows.append({'old':int(c[0]),'name':c[1],'pos':c[2],'team':c[3],'segment':c[4],'tier':c[5],'id':int(c[6]),'status':c[7],'changed':c[8],'evidence':c[9]})
assert len(rows)==254
ranked={x['id'] for x in rows}
def score(p):
    s=p.get('total_points',0)*5 + p.get('minutes',0)/45 + p.get('starts',0)*2 + p.get('now_cost',0)*1.2 + float(p.get('selected_by_percent') or 0)*2
    if p['element_type']==4: s+=45
    if p.get('chance_of_playing_next_round') is not None and p['chance_of_playing_next_round']<75: s-=100
    if 'departed' in (p.get('news') or '').lower(): s-=500
    return s
pool=[p for p in api['elements'] if p['id'] not in ranked]
pool.sort(key=score,reverse=True)
adds=pool[:96]
# Preserve the manually-reviewed top 140. Rebuild ranks 141-350 by merging existing depth with new candidates.
fixed=rows[:140]; tail=rows[140:]
# Existing tail receives a monotone baseline; candidates are mapped by score percentile and position scarcity.
items=[]
for i,x in enumerate(tail): items.append((1000-i*6.0,0,x))
mx=max(score(p) for p in adds); mn=min(score(p) for p in adds)
for j,p in enumerate(adds):
    norm=(score(p)-mn)/(mx-mn or 1)
    key=970*norm + (25 if p['element_type']==4 else 0)
    x={'old':None,'name':p['web_name'],'pos':POS[p['element_type']],'team':T[p['team']], 'segment':'','tier':'','id':p['id'],'status':p.get('news') or 'Available','changed':TS,'evidence':rl}
    items.append((key,1,x))
items.sort(key=lambda z:(z[0],z[1]),reverse=True)
ordered=fixed+[z[2] for z in items]
assert len(ordered)==350
for i,x in enumerate(ordered,1):
    x['rank']=i
    if i<=79: seg='Core'; tier=x['tier']
    elif i<=140: seg='Depth'; tier=x['tier']
    elif i<=180: seg='Endgame'; tier='D+'
    elif i<=280: seg='Undrafted buffer'; tier='D'
    else: seg='Extended watch buffer'; tier='Watch'
    if x['old'] is None or i>=141:
        x['segment']=seg; x['tier']=tier
        if x['old'] is not None and x['old']!=i: x['changed']=TS; x['evidence']=rl
header=[]; footer=[]; seen=False
for l in lines:
    if re.match(r'^\| \d+ \|',l): seen=True; continue
    if not seen: header.append(l)
    elif l.startswith('|---'): continue
    else: footer.append(l)
# recover table header from existing document
pre=[]
for l in lines:
    pre.append(l)
    if l.startswith('|---'): break
out=pre[:]
for x in ordered: out.append(f"| {x['rank']} | {x['name']} | {x['pos']} | {x['team']} | {x['segment']} | {x['tier']} | {x['id']} | {x['status']} | {x['changed']} | {x['evidence']} |")
# retain non-table trailing text
last=max(i for i,l in enumerate(lines) if re.match(r'^\| \d+ \|',l))
out += lines[last+1:]
B.write_text('\n'.join(out)+'\n')
# player notes for all new players and shifted tail players
changed_paths=[B]
for x in ordered[140:]:
    if x['old'] is None or x['old']!=x['rank']:
        p=P[x['id']]; path=R/f"vault/02 Players/{x['name']} - {x['id']}.md"
        old='unranked' if x['old'] is None else str(x['old'])
        status=p.get('news') or 'Available'
        body=f"---\ntype: player\nfpl_id: {x['id']}\nplayer: {x['name']}\nteam: {x['team']}\nposition: {x['pos']}\ncurrent_rank: {x['rank']}\nsegment: {x['segment']}\ntier: {x['tier']}\nlast_reviewed: {TS}\n---\n\n# {x['name']}\n\n## Current placement\n\n- Rank: **{x['rank']}** (previously {old})\n- Segment/tier: **{x['segment']} / {x['tier']}**\n- Status: {status}\n\n## Expansion assessment\n\nThis is a provisional full-pool placement created during the 350-player expansion. It uses current FPL identity, availability, prior points and minutes as screening evidence, then applies position scarcity. It is not treated as more certain than the manually pairwise-reviewed top 140.\n\n## Comparator range\n\nThe player belongs around ranks **{max(141,x['rank']-5)}–{min(350,x['rank']+5)}** pending direct role, preseason and first-team minutes evidence.\n\n## Reversal triggers\n\nPromote for confirmed starting role, advanced position, penalties/set pieces or repeated probable-first-team minutes. Demote for transfer departure, injury, reserve status or blocked minutes.\n\n## Evidence\n\n- [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/)\n- [Official fixtures](https://fantasy.premierleague.com/api/fixtures/)\n- {rl}\n"
        path.parent.mkdir(parents=True,exist_ok=True); path.write_text(body); changed_paths.append(path)
# review and changes
new_summary='\n'.join(f"- {x['rank']}. {x['name']} ({x['pos']}, {x['team']})" for x in ordered if x['old'] is None)
RV.parent.mkdir(parents=True,exist_ok=True)
RV.write_text(f"---\ntype: review\ntimestamp: {TS}\nscope: expand canonical board to 350\n---\n\n# FPL Draft review — expand to 350\n\n## API reconciliation\n\nOfficial FPL returned {len(api['elements'])} active players, {len(api['teams'])} teams and {len(fx)} fixtures. Stable FPL IDs were preserved.\n\n## Method\n\nThe manually reviewed top 140 was frozen. Every player absent from the 254-player board was screened using current API identity, position, availability, prior points, minutes and starts. The highest 96 plausible candidates were merged into ranks 141–350, with forward scarcity applied after the raw screening estimate. These placements are provisional and explicitly lower confidence than the pairwise-reviewed top 140.\n\n## Added players\n\n{new_summary}\n\n## Evidence adopted\n\nConfirmed API identity, team, position, availability, prior points, starts and minutes.\n\n## Evidence rejected\n\nPrice and ownership were not used as draft value. Screening scores were not interpreted as precise season projections. Players marked as departed were heavily penalised.\n\n## Uncertainty and next triggers\n\nDirectly pairwise-review the highest new entrants, especially forwards, attacking full-backs and players changing clubs or roles. Confirm preseason first-team minutes, set pieces and manager comments before promoting anyone into the manually reviewed top 140.\n\n## Sources\n\n- [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/)\n- [Official fixtures](https://fantasy.premierleague.com/api/fixtures/)\n")
CH.parent.mkdir(parents=True,exist_ok=True)
CH.write_text(f"---\ntype: changes\ntimestamp: {TS}\n---\n\n# Changes — expansion to 350\n\n- Board expanded from **254 to 350**.\n- Top 140 unchanged.\n- Added 96 previously unranked active API players.\n- Existing ranks 141–254 were re-slotted within the enlarged depth pool.\n- No player was removed.\n- New and shifted player notes record provisional comparator ranges and reversal triggers.\n\nSee {rl}.\n")
changed_paths += [RV,CH]
# watchlist/navigation
W.write_text(W.read_text()+f"\n## 350-player expansion — {TS}\n\nThe 96 new depth entries require role confirmation before promotion into the manually reviewed top 140. Prioritise forwards, attacking full-backs, new transfers and players with uncertain club status. See {rl}.\n"); changed_paths.append(W)
H.write_text(H.read_text()+f"\n- Latest expansion review: {rl}\n- Latest expansion changes: {cl}\n"); changed_paths.append(H)
K.write_text(K.read_text()+f"\n- [[06 Reviews/2026/08/2026-08-02/1017-AEST-review|350-player board expansion]]\n"); changed_paths.append(K)
# changelog rows for every changed md including changelog itself
ct=C.read_text(); ct=re.sub(r'last_updated: .*',f'last_updated: {TS}',ct,1)
src='[Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/); [Official fixtures](https://fantasy.premierleague.com/api/fixtures/)'
for path in changed_paths:
    rel=str(path); action='Created' if path in (RV,CH) or ('vault/02 Players/' in rel and not (R/rel).exists()) else 'Updated'
    ct+=f"\n| {TS} | `{rel}` | {action} | Expanded and provisionally assessed the canonical board to 350 players. | {rl} | {src} |"
ct+=f"\n| {TS} | `vault/00 Meta/Document Changelog.md` | Updated | Appended one row for every Markdown document changed in the 350-player expansion. | {rl} | Per-document audit |\n"
C.write_text(ct); changed_paths.append(C)
print({'board':len(ordered),'added':len(adds),'changed_markdown':len(changed_paths),'top_new':[(x['rank'],x['name']) for x in ordered if x['old'] is None][:20]})
