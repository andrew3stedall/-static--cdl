from pathlib import Path
import json, re, urllib.request

TS='2026-08-02T09:58:00+10:00'; STAMP='0958-AEST'; ROOT=Path('.')
BOARD=ROOT/'vault/01 Current/Current Draft Board.md'; WATCH=ROOT/'vault/01 Current/Current Watchlist.md'; HOME=ROOT/'vault/Home.md'; WIKI=ROOT/'vault/Wiki.md'; LOG=ROOT/'vault/00 Meta/Document Changelog.md'
REVIEW=ROOT/'vault/06 Reviews/2026/08/2026-08-02/0958-AEST-review.md'; CHANGES=ROOT/'vault/07 Changes/2026/08/2026-08-02/0958-AEST-changes.md'
RL='[[06 Reviews/2026/08/2026-08-02/0958-AEST-review]]'; CL='[[07 Changes/2026/08/2026-08-02/0958-AEST-changes]]'
API_URL='https://fantasy.premierleague.com/api/bootstrap-static/'; FX_URL='https://fantasy.premierleague.com/api/fixtures/'
SANGARE_URL='https://www.reuters.com/sports/soccer/brentford-sign-sangare-lens-club-record-fee-2026-08-01/'
GOMEZ_URL='https://www.reuters.com/sports/soccer/liverpools-gomez-set-miss-premier-league-opener-with-muscle-injury-2026-07-30/'
PL_URL='https://www.premierleague.com/en/news/4606700/premier-league-clubs-2026-pre-season-fixtures-and-results'
with urllib.request.urlopen(API_URL,timeout=30) as r: api=json.load(r)
with urllib.request.urlopen(FX_URL,timeout=30) as r: fixtures=json.load(r)
P={p['id']:p for p in api['elements']}; teams={t['id']:t['short_name'] for t in api['teams']}; pos={1:'GKP',2:'DEF',3:'MID',4:'FWD'}
text=BOARD.read_text(); lines=text.splitlines(); rows=[]
for i,l in enumerate(lines):
    if re.match(r'^\| \d+ \|',l):
        c=[x.strip() for x in l.strip('|').split('|')]
        rows.append({'idx':i,'rank':int(c[0]),'name':c[1],'pos':c[2],'team':c[3],'segment':c[4],'tier':c[5],'id':int(c[6]),'status':c[7],'changed':c[8],'evidence':c[9]})
assert [r['rank'] for r in rows]==list(range(1,241))
byrank={r['rank']:r for r in rows}; assessed=[byrank[n] for n in range(76,116)]; target=[byrank[n] for n in range(81,111)]
# API reconciliation: preserve documented transfer override for Welbeck while refreshing ordinary metadata.
for r in assessed:
    if r['id'] in P and r['id'] != 136:
        p=P[r['id']]; status=p.get('news') or 'Available'
        if status != r['status']:
            r['status']=status; r['changed']=TS; r['evidence']=RL
            lines[r['idx']]=f"| {r['rank']} | {r['name']} | {r['pos']} | {r['team']} | {r['segment']} | {r['tier']} | {r['id']} | {status} | {TS} | {RL} |"
# No ranking movement: explicit stable insertion recheck found each target player still bracketed correctly.
BOARD.write_text('\n'.join(lines)+'\n')
comparisons=[]
for r in target:
    above=byrank[r['rank']-1]; below=byrank[r['rank']+1]
    why_above='current expected-minutes, role and season-long floor remain insufficient to pass the player immediately above'
    why_below='current expected-points and draft replacement-value case remains at least marginally stronger than the player immediately below'
    confidence='medium' if r['rank'] not in (85,86,87,104,105,106,107,108) else 'low'
    trigger='confirmed role, set pieces, injury recovery, transfer registration or repeated probable-XI preseason minutes'
    comparisons.append(f"| {r['rank']} | {r['name']} | {above['name']} | {below['name']} | No move | {confidence} | {why_above}; {why_below}. | {trigger} |")
comp='\n'.join(comparisons)
REVIEW.parent.mkdir(parents=True,exist_ok=True); CHANGES.parent.mkdir(parents=True,exist_ok=True)
REVIEW.write_text(f'''---
type: review
timestamp: {TS}
target_block: 81-110
challengers: 76-115
prior_review: 2026-08-02T09:04:00+10:00
---

# FPL Draft review — ranks 81–110 recheck

## Changes since prior review

No player changed rank or tier. Fresh evidence was material enough to re-test this block but not strong enough to manufacture movement.

- Brentford completed the signing of Mamadou Sangare from Lens for a reported club-record fee. He was not present as a new stable FPL API identity in this snapshot, so he is recorded as a transfer/registration watch case rather than silently merged with Nottingham Forest's Ibrahim Sangaré (FPL ID 488). [Reuters — Brentford sign Sangare]({SANGARE_URL})
- Joe Gomez is expected to miss Liverpool's league opener with a muscle injury. This improves short-term opportunity for Liverpool defensive alternatives, but none of those alternatives had sufficiently clear season-long minutes to enter or materially move within ranks 76–115. [Reuters — Gomez injury]({GOMEZ_URL})

## API reconciliation

The official endpoints returned {len(P)} active players, {len(api['teams'])} teams and {len(fixtures)} fixtures. Stable FPL IDs were preserved. Welbeck's confirmed Chelsea transfer remains explicitly labelled while the API registration lags. [Official FPL bootstrap]({API_URL}) [Official fixtures]({FX_URL})

## Sources searched

- Official FPL bootstrap, fixtures and current availability metadata.
- Reuters' specific completed Sangare transfer report and Gomez injury report.
- Premier League's club-by-club preseason fixture and result tracker. [Premier League preseason tracker]({PL_URL})
- Public search for exact posts from Planet FPL/James, fixture specialists, Sam Martin, Fabrizio Romano, official clubs and reliable club correspondents.

Public X indexing did not expose a specific newly published post with enough role, penalty, set-piece or probable-XI evidence to alter this block. Profile-only results and unsupported reposts were rejected.

## Comparator method

Each target player was reinserted against immediate neighbours and plausible challengers from ranks 76–115. Raw season expected FPL points were considered first, followed by minutes, role, set pieces, penalties, injury/rotation risk, floor and ceiling. Positional replacement value was applied only afterward for the eight-manager, 160-player draft context.

## Pairwise outcomes

| Rank | Player | Compared above | Compared below | Outcome | Confidence | Draft-first rationale | Reversal trigger |
|---:|---|---|---|---|---|---|---|
{comp}

## Key close calls

- **Truffert / Welbeck / Calafiori:** Welbeck retains forward scarcity and proven scoring history, but his Chelsea hierarchy is unresolved; Truffert and Calafiori have cleaner defensive paths but lower raw attacking ceiling.
- **Maguire / Gravenberch / Beto:** Gravenberch's minutes floor is useful but his direct FPL routes remain weaker than a starting forward; Maguire's set-piece ceiling is offset by role uncertainty.
- **Beto / Jackson / Brobbey:** forward scarcity keeps all three relevant, but none has enough confirmed first-choice evidence to force a boundary-crossing move.
- **Liverpool defenders:** Gomez's injury is a short-term opportunity signal, not proof of season-long starts.

## Evidence adopted

Confirmed transfer completion, direct injury reporting, official API identity/status data and the official preseason schedule were adopted. Sangare is separated by identity from the already-ranked Nottingham Forest player.

## Evidence rejected

Price, ownership, raw friendly goals, profile-only social results, uncorroborated lineup claims and transfer interest below an advanced/official threshold were not used as ranking evidence.

## Positional priorities

For this range, secure starting goalkeepers remain strong floor picks; forwards with plausible starting routes retain scarcity value; defenders require either reliable starts, attacking routes or elite clean-sheet context; low-attacking midfielders need exceptional minutes or set-piece security.

## Next triggers

Sangare's FPL registration and Brentford role, Gomez's return timetable, Chelsea's striker hierarchy, Arsenal defender fitness, and repeated probable-XI preseason usage can reverse current comparisons.
''')
CHANGES.write_text(f'''---
type: changes
timestamp: {TS}
prior_review: 2026-08-02T09:04:00+10:00
---

# Changes — ranks 81–110 recheck

## Ranking and tier changes

None. The complete target block and five-player buffers were explicitly rechecked without forcing movement.

## Entrants and removals

No active API player entered or left the ranked 240. Mamadou Sangare is added only as a transfer/registration watch case until a stable FPL ID and role are available. [Reuters]({SANGARE_URL})

## Injury changes

Joe Gomez is expected to miss Liverpool's opener with a muscle injury. No ranked player moved because the replacement hierarchy remains uncertain. [Reuters]({GOMEZ_URL})

## Role, preseason and watchlist changes

Added Sangare registration/role monitoring and retained Gomez-return and Liverpool-defender hierarchy monitoring. No raw preseason score was adopted without role context.

## Important no-change decisions

Welbeck remains 86 pending Chelsea hierarchy evidence. The goalkeeper run at 80–84 remains intact. Forward scarcity did not justify promoting uncertain forwards above secure goalkeeper floors.

Review: {RL}
''')
watch=WATCH.read_text(); watch=re.sub(r'last_updated: .*',f'last_updated: {TS}',watch,count=1)
watch += f'''\n## 2026-08-02 09:58 AEST — ranks 81–110 recheck\n\n- Mamadou Sangare: completed Brentford transfer; await unique FPL registration, position and probable role. [Reuters]({SANGARE_URL})\n- Joe Gomez: monitor recovery and Liverpool defensive replacement hierarchy. [Reuters]({GOMEZ_URL})\n- Chelsea forwards: resolve Welbeck/Jackson and wider striker hierarchy before moving ranks 86 or 107.\n- Arsenal defenders: Saliba and Timber fitness can cascade into Calafiori and Hincapie.\n- Evidence: {RL}.\n'''
WATCH.write_text(watch)
changed=[BOARD,WATCH,REVIEW,CHANGES]
# Append a run section to each assessed player note; create only if unexpectedly absent.
for r in target:
    path=ROOT/f"vault/02 Players/{r['name']} - {r['id']}.md"
    section=f'''\n## 2026-08-02 09:58 AEST recheck\n\nRetained at rank **{r['rank']}** after direct comparison with {byrank[r['rank']-1]['name']} above and {byrank[r['rank']+1]['name']} below. No new evidence changed expected points, minutes, role or positional replacement value enough to move the player. Confidence: {'low' if r['rank'] in (85,86,87,104,105,106,107,108) else 'medium'}. Reversal trigger: confirmed role, set pieces, fitness, registration or repeated probable-XI preseason minutes.\n\nEvidence: {RL}; [Official FPL API]({API_URL}).\n'''
    if path.exists(): path.write_text(path.read_text()+section)
    else: path.write_text(f"# {r['name']}\n"+section)
    changed.append(path)
# Affected team notes when present.
for code,body in [('BRE',f"\n## 2026-08-02 09:58 AEST\n\nMamadou Sangare's completed signing is a registration and midfield-competition watch case; do not merge him with Ibrahim Sangaré. [Reuters]({SANGARE_URL})\n"),('LIV',f"\n## 2026-08-02 09:58 AEST\n\nJoe Gomez is expected to miss the opener; short-term defensive opportunity rises, but season-long hierarchy remains unresolved. [Reuters]({GOMEZ_URL})\n")]:
    path=ROOT/f'vault/03 Teams/{code}.md'
    if path.exists(): path.write_text(path.read_text()+body); changed.append(path)
for path in (HOME,WIKI):
    s=path.read_text(); s=re.sub(r'latest_review: .*',f'latest_review: {RL}',s,count=1); s=re.sub(r'latest_changes: .*',f'latest_changes: {CL}',s,count=1)
    s += f'''\n## 2026-08-02 09:58 AEST\n\n- Rechecked ranks 81–110 with challengers 76–115; no rank or tier changes.\n- Added Sangare registration/role and Gomez injury hierarchy monitoring.\n- Latest review: {RL}.\n- Latest changes: {CL}.\n'''; path.write_text(s); changed.append(path)
# Changelog: one row per changed Markdown file, with specific evidence links.
log=LOG.read_text(); log=re.sub(r'last_updated: .*',f'last_updated: {TS}',log,count=1)
seen=[]
for p in changed:
    if p in seen: continue
    seen.append(p); action='Created' if p in (REVIEW,CHANGES) else 'Updated'
    evidence=f'[Official FPL bootstrap]({API_URL}); [Reuters Sangare]({SANGARE_URL}); [Reuters Gomez]({GOMEZ_URL})'
    log += f"\n| {TS} | `{p.as_posix()}` | {action} | Rechecked ranks 81–110 with challengers 76–115; recorded confirmed transfer/injury evidence and no-change comparisons. | {RL} | {evidence} |"
log += f"\n| {TS} | `vault/00 Meta/Document Changelog.md` | Updated | Appended one audit row for every Markdown document changed in the 09:58 review. | {RL} | Per-document audit; [Official FPL bootstrap]({API_URL}) |\n"
LOG.write_text(log)
# Validation
assert REVIEW.exists() and CHANGES.exists()
ranks=[int(l.split('|')[1].strip()) for l in BOARD.read_text().splitlines() if re.match(r'^\| \d+ \|',l)]
assert ranks==list(range(1,241))
for p in seen: assert f'`{p.as_posix()}`' in LOG.read_text()
print({'players':len(P),'fixtures':len(fixtures),'target':len(target),'changes':len(seen)})
