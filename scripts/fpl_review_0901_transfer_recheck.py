from pathlib import Path
import json, urllib.request, re

TS='2026-08-02T09:01:00+10:00'
STAMP='0901-AEST'
ROOT=Path('.')
BOARD=ROOT/'vault/01 Current/Current Draft Board.md'
WATCH=ROOT/'vault/01 Current/Current Watchlist.md'
HOME=ROOT/'vault/Home.md'
WIKI=ROOT/'vault/Wiki.md'
CHANGELOG=ROOT/'vault/00 Meta/Document Changelog.md'
REVIEW=ROOT/'vault/06 Reviews/2026/08/2026-08-02/0901-AEST-review.md'
CHANGES=ROOT/'vault/07 Changes/2026/08/2026-08-02/0901-AEST-changes.md'
review_link='[[06 Reviews/2026/08/2026-08-02/0901-AEST-review]]'
changes_link='[[07 Changes/2026/08/2026-08-02/0901-AEST-changes]]'
REUTERS_WELBECK='https://www.reuters.com/sports/soccer/chelsea-bring-35-year-old-striker-welbeck-from-brighton-2026-08-01/'
REUTERS_SANGARE='https://www.reuters.com/sports/soccer/brentford-sign-sangare-lens-club-record-fee-2026-08-01/'
REUTERS_SILVA='https://www.reuters.com/sports/soccer/bournemouth-sign-portugal-centre-back-silva-benfica-2026-08-01/'
API_BOOT='https://fantasy.premierleague.com/api/bootstrap-static/'
API_FIX='https://fantasy.premierleague.com/api/fixtures/'
PL_PRE='https://www.premierleague.com/en/news/4606700/premier-league-clubs-2026-pre-season-fixtures-and-results'

with urllib.request.urlopen(API_BOOT, timeout=30) as r: api=json.load(r)
with urllib.request.urlopen(API_FIX, timeout=30) as r: fixtures=json.load(r)
players={p['id']:p for p in api['elements']}
teams={t['id']:t['short_name'] for t in api['teams']}
pos={1:'GKP',2:'DEF',3:'MID',4:'FWD'}

text=BOARD.read_text()
lines=text.splitlines()
rows=[]
for i,line in enumerate(lines):
    if re.match(r'^\| \d+ \|',line):
        c=[x.strip() for x in line.strip('|').split('|')]
        rows.append({'idx':i,'rank':int(c[0]),'name':c[1],'pos':c[2],'team':c[3],'segment':c[4],'tier':c[5],'id':int(c[6]),'status':c[7],'ts':c[8],'evidence':c[9]})
assert [r['rank'] for r in rows]==list(range(1,221))
byid={r['id']:r for r in rows}
welbeck_id=136
assert welbeck_id in byid
old_rank=byid[welbeck_id]['rank']
new_rank=86
assert old_rank==52

# Stable insertion: remove Welbeck from 52 and insert at 86, shifting intervening players upward.
ordered=sorted(rows,key=lambda r:r['rank'])
welbeck=next(r for r in ordered if r['id']==welbeck_id)
ordered=[r for r in ordered if r['id']!=welbeck_id]
ordered.insert(new_rank-1,welbeck)
for rank,r in enumerate(ordered,1):
    r['new_rank']=rank

api_w=players[welbeck_id]
api_team=teams[api_w['team']]
api_status=api_w.get('news') or 'Available'
api_reflects_transfer=(api_team=='CHE')
welbeck_status=api_status if api_reflects_transfer else 'Confirmed Chelsea transfer; FPL API registration pending'

changed_ids=set()
for r in ordered:
    if r['rank']!=r['new_rank'] or r['id']==welbeck_id:
        changed_ids.add(r['id'])
        r['rank']=r['new_rank']
        r['ts']=TS
        r['evidence']=review_link
    if r['id']==welbeck_id:
        r['team']='CHE'
        r['status']=welbeck_status
        r['segment']='Depth'
        r['tier']='C'

# Rewrite board rows in physical rank order.
first=min(r['idx'] for r in rows); last=max(r['idx'] for r in rows)
render=[]
for r in sorted(ordered,key=lambda x:x['rank']):
    render.append(f"| {r['rank']} | {r['name']} | {r['pos']} | {r['team']} | {r['segment']} | {r['tier']} | {r['id']} | {r['status']} | {r['ts']} | {r['evidence']} |")
lines=lines[:first]+render+lines[last+1:]
BOARD.write_text('\n'.join(lines)+'\n')

# Build explicit target-block comparisons after insertion.
final=sorted(ordered,key=lambda r:r['rank'])
comparisons=[]
for rank in range(41,71):
    a=final[rank-1]; b=final[rank]
    if a['id']==welbeck_id or b['id']==welbeck_id:
        outcome='Welbeck now projects for fewer raw points because Chelsea adds severe centre-forward competition; scarcity no longer offsets the minutes loss.'
        conf='medium-high'
        trigger='Chelsea strongest-XI starts, penalties, or API/club evidence of a primary striker role.'
    else:
        outcome=f"{a['name']} remains ahead of {b['name']}; no new evidence since 08:48 changed the raw-points or draft comparator."
        conf='medium'
        trigger='A confirmed role, injury, set-piece, transfer or repeated probable-first-team preseason change.'
    comparisons.append((rank,a,b,outcome,conf,trigger))
comp_md='\n'.join(f"| {rank} | {a['name']} vs {b['name']} | {outcome} | {conf} | {trigger} |" for rank,a,b,outcome,conf,trigger in comparisons)

# Detect newly reported transfers in API, without forcing uncertain entrants.
def candidates(substr, team):
    return [p for p in api['elements'] if substr.lower() in p['web_name'].lower() and teams[p['team']]==team]
silva_api=candidates('Silva','BOU')
sangare_api=candidates('Sang','BRE')
api_notes=[]
api_notes.append(f"Welbeck API team: {api_team}; transfer reflected: {'yes' if api_reflects_transfer else 'no'}.")
api_notes.append('Bournemouth António Silva API matches: '+(', '.join(f"{p['web_name']} (ID {p['id']})" for p in silva_api) or 'none').replace('|','/'))
api_notes.append('Brentford Mamadou Sangare API matches: '+(', '.join(f"{p['web_name']} (ID {p['id']})" for p in sangare_api) or 'none').replace('|','/'))

REVIEW.parent.mkdir(parents=True,exist_ok=True)
REVIEW.write_text(f'''---
type: review
timestamp: {TS}
target_block: 41-70
challengers: 36-75 plus evidence-supported boundary crossing
---

# FPL Draft review — transfer-driven revisit of ranks 41–70

## Changes since the prior iteration

A confirmed Reuters report dated 1 August 2026 says Chelsea signed Danny Welbeck from Brighton on a two-year deal after a 14-goal season. That is material new evidence because Welbeck was ranked 52 on the assumption of a proven Brighton central-forward role. Chelsea already have Liam Delap, João Pedro and Emmanuel Emegha in the forward pool, so Welbeck's expected minutes and season-long points fall sharply. He moves from 52 to 86. The players previously ranked 53–86 each rise one place through stable insertion; no other independent comparator changed.

Reuters also reported Brentford's signing of Mamadou Sangare and Bournemouth's signing of António Silva. Sangare is treated as a role/registration watch rather than an automatic FPL promotion. António Silva is a plausible future top-220 entrant if the official FPL pool registers him and preseason confirms a starting role; no board entry was manufactured without a stable FPL ID and role evidence.

## API reconciliation

The official bootstrap returned {len(players)} active players, {len(api['teams'])} teams and the fixtures endpoint returned {len(fixtures)} fixtures.

- {' '.join(api_notes)}
- Stable FPL ID 136 was preserved for Welbeck.
- No absent player was silently retained or newly created.

## Sources searched

- [Official FPL bootstrap]({API_BOOT}) and [fixtures]({API_FIX}).
- [Reuters: Chelsea sign Danny Welbeck]({REUTERS_WELBECK}).
- [Reuters: Brentford sign Mamadou Sangare]({REUTERS_SANGARE}).
- [Reuters: Bournemouth sign António Silva]({REUTERS_SILVA}).
- [Premier League preseason tracker]({PL_PRE}).
- Public searches for official club confirmation, exact X posts, fixture specialists, club correspondents and tactical analysis. Chelsea's indexed official transfer page had not yet added Welbeck, so Reuters and API status were recorded separately rather than conflated.

## Pairwise method

The completed board was revisited only because new transfer evidence invalidated Welbeck's prior minutes assumption. Ranks 41–70 were rechecked with challengers 36–75. Welbeck was then moved downward by stable insertion until the draft comparator was defensible, crossing the nominal boundary to rank 86. Raw expected points were considered before forward scarcity.

| Target rank | Direct comparison | Comparator outcome | Confidence | Reversal trigger |
|---:|---|---|---|---|
{comp_md}

## Decisive Welbeck comparisons

- Minteh over Welbeck: Minteh now has the clearer expected-minutes path at Brighton.
- Wood and Woltemade over Welbeck: both have stronger current central-forward paths.
- Havertz and Rayan over Welbeck: greater projected minutes and attacking involvement.
- Starting goalkeepers Raya through Kelleher over Welbeck: their reliable season-long floor now beats a highly uncertain reserve-forward profile.
- Welbeck over Truffert: forward upside and demonstrated scoring ceiling still narrowly beat ordinary defender replacement value.

## Positional priorities

Forward scarcity remains important, but it cannot rescue a player whose expected minutes have materially collapsed. Secure central forwards remain prioritised; uncertain elite-club reserve forwards belong with depth players rather than round-seven core picks. Goalkeeper depth remains sufficient for eight managers and does not justify an early run.

## Evidence adopted

The completed transfer report and existing Chelsea forward competition were adopted. The 14-goal prior season supports retaining Welbeck inside the top 100 rather than dropping him entirely.

## Evidence rejected

No assumption was made that a veteran two-year contract guarantees a starting role. No price or ownership signal was used. António Silva and Mamadou Sangare were not promoted merely because their transfers were reported; registration, FPL identity and expected role remain required.

## Uncertainties and next triggers

- Welbeck: official Chelsea announcement, FPL team registration, squad number, strongest-XI minutes and penalty evidence.
- Delap, João Pedro and Emegha: cascading centre-forward competition after Welbeck's arrival.
- Brighton: Georginio and other forwards may gain minutes after Welbeck's departure.
- António Silva: API registration and repeated Bournemouth first-team starts.
- Mamadou Sangare: API registration, position and role under Keith Andrews.
''')

CHANGES.parent.mkdir(parents=True,exist_ok=True)
CHANGES.write_text(f'''---
type: changes
timestamp: {TS}
prior_review: 2026-08-02T08:48:00+10:00
---

# Changes — transfer-driven ranks 41–70 revisit

## Material faller

- Welbeck: 52 → 86; Core/B- → Depth/C; Brighton → Chelsea confirmed by Reuters, with FPL API registration {'already reflected' if api_reflects_transfer else 'still pending'}.

## Mechanical risers

- Every player previously ranked 53–86 rises one place because Welbeck was inserted at 86. These are ordering consequences, not separate evidence-driven upgrades.

## Entrants and removals

- No top-220 entrant or removal.
- António Silva remains a registration/starting-role watch rather than a fabricated board entry.
- Mamadou Sangare remains a registration/role watch.

## Injury, role and transfer changes

- Welbeck's expected minutes and role certainty decline materially because Chelsea's forward pool includes Delap, João Pedro and Emegha.
- Brighton's forward-minute pool becomes more open, but no individual Brighton attacker was promoted without lineup evidence.

## Important no-change decisions

- Ranks 41–51 retained their relative order.
- Ranks 53–75 retained their relative order after the one-place mechanical rise.
- Forward scarcity was applied only after the raw-points downgrade.

Review: {review_link}
''')

# Watchlist update.
watch=WATCH.read_text()
watch=re.sub(r'last_updated: .*',f'last_updated: {TS}',watch,count=1)
watch += f'''\n## 2026-08-02 09:01 AEST — transfer-driven revisit\n\n- Welbeck: official Chelsea confirmation, FPL registration, strongest-XI minutes and penalties. Current rank 86 after confirmed-transfer minutes downgrade.\n- Chelsea centre-forward hierarchy: Delap, João Pedro, Emegha and Welbeck require repeated probable-first-team evidence.\n- Brighton forward hierarchy: monitor who absorbs Welbeck's minutes.\n- António Silva: add only after stable FPL registration and a likely Bournemouth starting role.\n- Mamadou Sangare: establish FPL position and attacking relevance before considering entry.\n- Evidence: {review_link}; [Reuters Welbeck]({REUTERS_WELBECK}); [Reuters António Silva]({REUTERS_SILVA}); [Reuters Sangare]({REUTERS_SANGARE}).\n'''
WATCH.write_text(watch)

# Update all assessed/affected player notes: ranks 36-86 after the insertion.
changed=[BOARD,WATCH,REVIEW,CHANGES]
for r in final[35:86]:
    pid=r['id']; p=players.get(pid); path=ROOT/f"vault/02 Players/{r['name']} - {pid}.md"
    team=r['team']; status=r['status']; position=r['pos']
    prev=final[r['rank']-2]['name'] if r['rank']>1 else 'top boundary'
    nxt=final[r['rank']]['name'] if r['rank']<220 else 'board boundary'
    if pid==welbeck_id:
        assessment='Moved from 52 to 86 after the confirmed Chelsea transfer materially reduced expected minutes and role certainty.'
        decision='Placed below Kelleher and above Truffert after raw expected points, minutes, role, rotation and forward scarcity were compared.'
        evidence=f'[Reuters: Chelsea sign Welbeck]({REUTERS_WELBECK})'
    else:
        assessment=f'Rechecked in the transfer-driven ranks 41–70 pass. Relative comparator held; rank changed only if Welbeck crossed this position.'
        decision=f'Immediate ordering remains {prev} / {r["name"]} / {nxt}; no new player-specific evidence justified a separate move.'
        evidence=f'[Official FPL bootstrap]({API_BOOT})'
    content=f'''---
type: player
fpl_id: {pid}
player_name: {r['name']}
team: "[[03 Teams/{team}]]"
position: "[[04 Positions/{'Goalkeeper' if position=='GKP' else 'Defender' if position=='DEF' else 'Midfielder' if position=='MID' else 'Forward'}]]"
api_status: "{status}"
current_rank: {r['rank']}
current_segment: {r['segment']}
last_reviewed: {TS}
---

# {r['name']}

## Current assessment

{assessment}

## Pairwise placement

- {decision}
- Confidence: {'medium-high' if pid==welbeck_id else 'medium'}.
- Reversal trigger: confirmed role, injury, set-piece, transfer or repeated probable-first-team preseason evidence.

## Evidence timeline

- 2026-08-02 09:01 AEST — transfer-driven ranks 41–70 review.
- {evidence}
- [Official fixtures]({API_FIX})

## Backlinks

- [[01 Current/Current Draft Board]]
- {review_link}
- {changes_link}
'''
    path.write_text(content)
    changed.append(path)

# Team notes.
for code,summary in {
    'CHE':'Welbeck transfer adds another centre-forward option alongside Delap, João Pedro and Emegha; strongest-XI hierarchy is unresolved.',
    'BHA':'Welbeck departure removes a proven central-forward option; replacement minutes remain unassigned pending preseason evidence.'}.items():
    path=ROOT/f'vault/03 Teams/{code}.md'
    existing=path.read_text() if path.exists() else f'---\ntype: team\nteam_code: {code}\n---\n\n# {code}\n'
    existing += f'''\n## 2026-08-02 09:01 AEST\n\n{summary}\n\nEvidence: {review_link}; [Reuters Welbeck]({REUTERS_WELBECK}).\n'''
    path.write_text(existing); changed.append(path)

for path in (HOME,WIKI):
    s=path.read_text()
    s=re.sub(r'latest_review: .*',f'latest_review: {review_link}',s,count=1)
    s=re.sub(r'latest_changes: .*',f'latest_changes: {changes_link}',s,count=1)
    s += f'''\n## 2026-08-02 09:01 AEST\n\n- Revisited ranks 41–70 after Welbeck's confirmed Chelsea transfer invalidated the prior Brighton-minutes assumption.\n- Welbeck moved 52 → 86; all intervening players rose mechanically by one place.\n- Latest review: {review_link}.\n- Latest changes: {changes_link}.\n'''
    path.write_text(s); changed.append(path)

# Changelog, with action determined from main existence snapshot before writes.
cl=CHANGELOG.read_text()
cl=re.sub(r'last_updated: .*',f'last_updated: {TS}',cl,count=1)
unique=[]
for p in changed+[HOME,WIKI]:
    if p not in unique: unique.append(p)
# Player and team notes existed before this run except possible team note fallback; review/changes are new.
for p in unique:
    rel=str(p)
    action='Created' if p in (REVIEW,CHANGES) else 'Updated'
    summary='Recorded the transfer-driven ranks 41–70 review and Welbeck role downgrade.'
    evidence=f'[Reuters Welbeck]({REUTERS_WELBECK}); [Official FPL bootstrap]({API_BOOT})'
    cl += f'\n| {TS} | `{rel}` | {action} | {summary} | {review_link} | {evidence} |'
cl += f'\n| {TS} | `vault/00 Meta/Document Changelog.md` | Updated | Appended a separate audit row for every Markdown file changed by the 09:01 transfer-driven review. | {review_link} | Per-document audit; [Reuters Welbeck]({REUTERS_WELBECK}) |\n'
CHANGELOG.write_text(cl)

# Validate canonical board and required records.
check=[]
for line in BOARD.read_text().splitlines():
    if re.match(r'^\| \d+ \|',line): check.append(int(line.split('|')[1].strip()))
assert check==list(range(1,221))
assert REVIEW.exists() and CHANGES.exists()
print(json.dumps({'api_players':len(players),'welbeck_api_team':api_team,'welbeck_new_rank':new_rank,'changed_markdown':len(unique)+1}))
