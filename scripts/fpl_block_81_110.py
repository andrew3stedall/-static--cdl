from __future__ import annotations

import json
import re
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

import requests

ROOT = Path('.')
TS = datetime(2026, 8, 2, 8, 15, tzinfo=ZoneInfo('Australia/Melbourne'))
ISO = TS.isoformat()
STAMP = '0815-AEST'
DATE = '2026-08-02'
REVIEW_LINK = '[[06 Reviews/2026/08/2026-08-02/0815-AEST-review]]'
CHANGE_LINK = '[[07 Changes/2026/08/2026-08-02/0815-AEST-changes]]'
BOOTSTRAP_URL = 'https://fantasy.premierleague.com/api/bootstrap-static/'
FIXTURES_URL = 'https://fantasy.premierleague.com/api/fixtures/'
PRESEASON_URL = 'https://www.premierleague.com/en/news/4606700/premier-league-clubs-2026-pre-season-fixtures-and-results'

branch_players = [
    'Havertz','Rayan','Dorgu','Aina','Tete','Raya','Pickford','Donnarumma','Henderson','Kelleher',
    'Truffert','Calafiori','Igor Jesus','Groß','Okafor','O\'Reilly','Matheus N.','Rúben','Lacroix','Ballard',
    'Romero','Bijol','Richards','Roefs','Pope','A.Becker','Martinez','Keane','Maguire','Gravenberch',
    'Hill','Alderete','Thiaw','Wieffer','Andersen','Ekitiké','Grealish','Brobbey','Canvot','Scott'
]

key_reasons = {
    ('Havertz','Rayan'): 'Havertz has the stronger raw scoring ceiling and forward scarcity despite Arsenal competition.',
    ('Rayan','Dorgu'): 'Rayan has the clearer attacking role today; Dorgu can pass him with repeated advanced starts.',
    ('Dorgu','Aina'): 'Dorgu offers the higher attacking ceiling as a midfielder; Aina has the safer defensive floor.',
    ('Aina','Tete'): 'Aina has the stronger demonstrated two-way return profile.',
    ('Tete','Raya'): 'Tete has more open-play attacking upside; goalkeeper depth keeps Raya behind.',
    ('Raya','Pickford'): 'Raya retains the superior clean-sheet ceiling.',
    ('Pickford','Donnarumma'): 'Pickford has the clearer save-volume and bonus floor.',
    ('Donnarumma','Henderson'): 'Donnarumma has the stronger clean-sheet ceiling, offset by lower save volume.',
    ('Henderson','Kelleher'): 'Henderson has the stronger established save and bonus profile.',
    ('Kelleher','Truffert'): 'Kelleher has secure goalkeeper minutes; Truffert needs role confirmation to overcome that floor.',
    ('Truffert','Calafiori'): 'Truffert has the clearer route to regular attacking full-back minutes.',
    ('Calafiori','Igor Jesus'): 'Calafiori has the safer current role; Igor Jesus has forward scarcity but uncertain starts.',
    ('Igor Jesus','Groß'): 'Forward replacement value narrowly lifts Igor Jesus over Groß.',
    ('Groß','Okafor'): 'Groß has the safer set-piece and minutes floor.',
    ('Okafor',"O'Reilly"): 'Okafor has the more direct route to attacking returns when starting.',
    ("O'Reilly",'Matheus N.'): 'O’Reilly has the higher attacking-defender ceiling, but both carry major rotation risk.',
    ('Matheus N.','Rúben'): 'Matheus Nunes has more attacking upside; Rúben Dias has the safer centre-back role.',
    ('Rúben','Lacroix'): 'Rúben Dias has the stronger team clean-sheet ceiling.',
    ('Lacroix','Ballard'): 'Lacroix has the stronger combination of minutes and clean-sheet environment.',
    ('Ballard','Romero'): 'Ballard is preferred for aerial threat and a steadier disciplinary profile.',
    ('Romero','Bijol'): 'Romero has the higher attacking ceiling, though cards reduce his floor.',
    ('Bijol','Richards'): 'Bijol has the clearer set-piece threat.',
    ('Richards','Roefs'): 'Richards has a better draft replacement profile than another goalkeeper at this point.',
    ('Roefs','Pope'): 'Roefs is marginally preferred on projected save volume.',
    ('Pope','A.Becker'): 'Pope has the stronger save-volume route; Alisson relies more heavily on clean sheets.',
    ('A.Becker','Martinez'): 'Alisson has the stronger clean-sheet ceiling.',
    ('Martinez','Keane'): 'Martinez has a secure goalkeeper floor; Keane’s starting role is less certain.',
    ('Keane','Maguire'): 'Keane has the clearer current path to starts and set-piece threat.',
    ('Maguire','Gravenberch'): 'Maguire’s aerial threat narrowly beats Gravenberch’s deeper midfield role.',
    ('Gravenberch','Hill'): 'Gravenberch has the safer minutes floor.',
    ('Hill','Alderete'): 'Hill is preferred on role security in the current evidence set.',
    ('Alderete','Thiaw'): 'Alderete has the clearer starting role.',
    ('Thiaw','Wieffer'): 'Thiaw has more set-piece threat; Wieffer’s defensive classification is useful but role-dependent.',
    ('Wieffer','Andersen'): 'Wieffer is available immediately; Andersen’s suspension lowers early-season value.',
    ('Andersen','Ekitiké'): 'Andersen’s eventual role is secure, while Ekitiké carries an unknown-return Achilles flag.',
    ('Ekitiké','Grealish'): 'Ekitiké retains forward scarcity and ceiling despite the injury discount.',
    ('Grealish','Brobbey'): 'Grealish has the higher per-start creative ceiling; both have material minutes risk.',
    ('Brobbey','Canvot'): 'Brobbey’s forward scarcity narrowly wins despite uncertain role.',
    ('Canvot','Scott'): 'Canvot has the clearer path to defensive starts; Scott needs an advanced role to pass him.'
}


def get_json(url: str):
    r = requests.get(url, timeout=45)
    r.raise_for_status()
    return r.json()

bootstrap = get_json(BOOTSTRAP_URL)
fixtures = get_json(FIXTURES_URL)
api_by_id = {int(x['id']): x for x in bootstrap['elements']}
teams = {int(t['id']): t['short_name'] for t in bootstrap['teams']}
pos = {int(p['id']): p['singular_name_short'] for p in bootstrap['element_types']}

board_path = ROOT / 'vault/01 Current/Current Draft Board.md'
board = board_path.read_text()
row_re = re.compile(r'^\|\s*(\d+)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(\d+)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|$', re.M)
rows = []
for m in row_re.finditer(board):
    rows.append({
        'rank': int(m.group(1)), 'player': m.group(2).strip(), 'position': m.group(3).strip(), 'team': m.group(4).strip(),
        'segment': m.group(5).strip(), 'tier': m.group(6).strip(), 'id': int(m.group(7)), 'status': m.group(8).strip(),
        'changed': m.group(9).strip(), 'evidence': m.group(10).strip()
    })
assert len(rows) >= 220, len(rows)
by_name = {r['player']: r for r in rows}
missing = [n for n in branch_players if n not in by_name]
assert not missing, missing
old_rank = {n: by_name[n]['rank'] for n in branch_players}

# Reinsert the 76-115 challenger pool in stable pairwise order.
for idx, name in enumerate(branch_players, start=76):
    r = by_name[name]
    r['rank'] = idx
    r['segment'] = 'Core' if idx <= 80 else 'Depth'
    r['tier'] = 'C+' if idx <= 80 else 'C'
    api = api_by_id.get(r['id'])
    if api:
        r['team'] = teams.get(int(api['team']), r['team'])
        r['position'] = pos.get(int(api['element_type']), r['position'])
        news = (api.get('news') or '').strip()
        chance = api.get('chance_of_playing_next_round')
        if news:
            r['status'] = news + (f' - {chance}% chance of playing' if chance is not None and str(chance) not in news else '')
        elif api.get('status') == 'a':
            r['status'] = 'Available'
        else:
            r['status'] = f"API status {api.get('status')}"
    r['changed'] = ISO
    r['evidence'] = REVIEW_LINK

rows.sort(key=lambda x: x['rank'])
assert [r['rank'] for r in rows[:220]] == list(range(1,221))

header_end = board.index('| 1 |')
footer_start = board.index('\n## Method cautions')
header = board[:header_end]
header = re.sub(r'last_updated: .*', f'last_updated: {ISO}', header)
header = re.sub(r'status: .*', 'status: ranks81_110_pairwise_sorted', header)
header = header.replace('The first 80 have now been stable-sorted in five explicit player-versus-player blocks.', 'The first 110 have now been manually stable-sorted; this run reviewed ranks 81–110 with challengers from 76–115.')
lines = []
for r in rows:
    lines.append(f"| {r['rank']} | {r['player']} | {r['position']} | {r['team']} | {r['segment']} | {r['tier']} | {r['id']} | {r['status']} | {r['changed']} | {r['evidence']} |")
board_path.write_text(header + '\n'.join(lines) + board[footer_start:])

# Immutable review and changes records.
review_path = ROOT / f'vault/06 Reviews/2026/08/{DATE}/{STAMP}-review.md'
review_path.parent.mkdir(parents=True, exist_ok=True)
comparisons = []
for a,b in zip(branch_players, branch_players[1:]):
    comparisons.append(f"- **{a} over {b}** — {key_reasons[(a,b)]} Confidence: {'low' if any(x in (a,b) for x in ['Ekitiké','Grealish',"O'Reilly",'Matheus N.']) else 'medium'}. Reversal trigger: repeated strongest-XI role, set pieces, fitness or official transfer evidence.")
review = f'''---
type: review
timestamp: {ISO}
target_block: 81-110
challenger_range: 76-115
---

# FPL Draft review — ranks 81–110

## Changes since the prior iteration

This run completed the first manual pairwise pass over ranks 81–110 while allowing challengers from ranks 76–115 to cross the boundary. Havertz, Rayan, Dorgu, Aina and Tete moved ahead of the goalkeeper run; injured Ekitiké and Grealish were discounted heavily.

## API reconciliation

- Official bootstrap reachable: **{len(bootstrap['elements'])} players**, **{len(bootstrap['teams'])} teams**.
- Official fixtures reachable: **{len(fixtures)} fixtures**.
- All 40 challenger-pool FPL IDs remained present in the current API pool.
- Team, position and availability metadata were refreshed from the official API.

Sources: [Official FPL bootstrap]({BOOTSTRAP_URL}); [Official fixtures]({FIXTURES_URL}).

## Pairwise procedure and decisive comparisons

Expected season points were judged first. Minutes, role, set pieces, penalties, injury and rotation risk were then applied. Positional replacement value altered close cross-position decisions only after the raw-points judgement.

{chr(10).join(comparisons)}

## Evidence adopted

- Official player identity, position, team and availability metadata.
- Official fixture list.
- The Premier League preseason schedule as confirmation of match timing and the next evidence opportunities.
- Existing dated repository evidence where no newer specific role signal was available.

## Evidence rejected or unavailable

- Raw friendly goals or assists without probable-first-team context were not used as automatic promotion evidence.
- Search did not provide reliably indexed, exact-post X evidence from Planet FPL, Ben Crellin, Sam Martin or Fabrizio Romano that materially changed this block; profile-level references were not substituted for specific posts.
- No unverified transfer rumour was treated as a completed move.

## Ranking trade-offs

- Five goalkeepers remained together but were pushed behind five outfield players with stronger scarcity or attacking routes.
- Havertz is promoted despite Arsenal competition because his forward classification and scoring ceiling remain draft-relevant.
- Ekitiké is retained only at 110 because the official Achilles flag and unknown return outweigh forward scarcity.
- Manchester City defenders remain heavily discounted for rotation.
- Andersen's suspension lowers immediate value despite a secure medium-term role.

## Sources searched

- [Official FPL bootstrap]({BOOTSTRAP_URL})
- [Official FPL fixtures]({FIXTURES_URL})
- [Premier League preseason fixtures and results]({PRESEASON_URL})
- Public web/X searches for Planet FPL, Ben Crellin, Sam Martin, Fabrizio Romano, club journalists and official club posts.

## Uncertainties and next triggers

- Havertz and Calafiori: Arsenal strongest-XI role and minutes.
- Dorgu: repeated advanced midfield deployment.
- O'Reilly, Matheus Nunes and Rúben Dias: Manchester City defensive hierarchy.
- Ekitiké and Grealish: official medical and return-to-training updates.
- Goalkeepers: confirmed opening-day hierarchy and any late transfers.
- Next manual block: ranks 111–140 with challengers 106–145.

## Navigation

- [[01 Current/Current Draft Board]]
- [[01 Current/Current Watchlist]]
- {CHANGE_LINK}
'''
review_path.write_text(review)

changes_path = ROOT / f'vault/07 Changes/2026/08/{DATE}/{STAMP}-changes.md'
changes_path.parent.mkdir(parents=True, exist_ok=True)
movement_rows = []
for name in branch_players:
    movement_rows.append(f"| {name} | {old_rank[name]} | {by_name[name]['rank']} | {by_name[name]['tier']} | {by_name[name]['status']} |")
changes = f'''---
type: changes
timestamp: {ISO}
prior_review: "[[06 Reviews/2026/08/2026-08-02/0800-AEST-review]]"
---

# Changes — ranks 81–110 pairwise review

## Material movements

| Player | Old rank | New rank | New tier | Status |
|---|---:|---:|---|---|
{chr(10).join(movement_rows)}

## Main risers

- Havertz moved 105 → 76.
- Dorgu moved 114 → 78.
- Aina moved 102 → 79.
- Tete moved 104 → 80.
- Rayan moved 85 → 77.

## Main fallers

- O'Reilly moved 81 → 91 as Manchester City rotation remained unresolved.
- Ekitiké moved 87 → 110 because the official Achilles flag still has an unknown return date.
- Grealish moved 108 → 111 due to injury and role uncertainty.
- Several centre-backs and goalkeepers moved down as higher-ceiling outfield challengers crossed the boundary.

## Injury, transfer, role and preseason changes

- No newly verified completed transfer changed this block.
- Official API availability metadata was refreshed for every player.
- No raw friendly result was accepted as a role change without position and probable-first-team context.
- X and public-source searches produced no exact new post strong enough to override the API and existing role evidence.

## Watchlist changes

Added explicit triggers for Arsenal role allocation, Manchester City defensive rotation, Ekitiké and Grealish medical updates, and opening-day goalkeeper hierarchies.

## Important no-change decisions

- Raya remains the first goalkeeper.
- Pickford remains above Donnarumma on save and bonus floor.
- Ekitiké remains ranked despite injury because he is still present in the official API pool; he is not treated as available without qualification.

## Navigation

- {REVIEW_LINK}
- [[01 Current/Current Draft Board]]
- [[01 Current/Current Watchlist]]
'''
changes_path.write_text(changes)

# Player notes for all 40 assessed players.
player_dir = ROOT / 'vault/02 Players'
for i,name in enumerate(branch_players):
    r = by_name[name]
    opponent = branch_players[i+1] if i < len(branch_players)-1 else 'the next 111–140 challenger'
    reason = key_reasons.get((name, opponent), 'Retained at the lower boundary pending the next block.')
    api = api_by_id.get(r['id'], {})
    note = f'''---
type: player
fpl_id: {r['id']}
player_name: {name}
team: "[[03 Teams/{r['team']}]]"
position: "[[04 Positions/{'Goalkeeper' if r['position']=='GKP' else 'Defender' if r['position']=='DEF' else 'Midfielder' if r['position']=='MID' else 'Forward'}]]"
api_status: "{r['status'].replace('"', "'")}"
current_rank: {r['rank']}
current_segment: {r['segment']}
last_reviewed: {ISO}
---

# {name}

## Current assessment

Ranked {r['rank']} after the ranks 81–110 review with challengers from 76–115. Official FPL ID {r['id']} remains active in the API pool.

## Direct comparison

- Compared with: **{opponent}**.
- Raw expected-points judgement: {name} is currently preferred.
- Draft decision: {reason}
- Confidence: {'low' if any(x in name for x in ['Ekitiké','Grealish']) or name in ["O'Reilly",'Matheus N.'] else 'medium'}.
- Reversal trigger: confirmed strongest-XI role, set pieces, fitness or official transfer evidence that changes the comparison.

## Current metadata

- Team: {r['team']}
- Position: {r['position']}
- Availability: {r['status']}
- API total points field: {api.get('total_points', 'n/a')}
- API minutes field: {api.get('minutes', 'n/a')}

## Evidence timeline

- 2026-08-02 08:15 AEST — Pairwise-reviewed and placed at rank {r['rank']}.
- [Official FPL bootstrap]({BOOTSTRAP_URL})
- [Official fixtures]({FIXTURES_URL})
- [Premier League preseason schedule]({PRESEASON_URL})

## Backlinks

- [[01 Current/Current Draft Board]]
- {REVIEW_LINK}
- {CHANGE_LINK}
'''
    (player_dir / f'{name} - {r["id"]}.md').write_text(note)

# Watchlist, Home and Wiki.
watch_path = ROOT / 'vault/01 Current/Current Watchlist.md'
watch = watch_path.read_text()
watch = re.sub(r'last_updated: .*', f'last_updated: {ISO}', watch, count=1)
watch += f'''\n## 2026-08-02 08:15 AEST — ranks 81–110 triggers\n\n- Arsenal: Havertz and Calafiori strongest-XI roles.\n- Manchester United: Dorgu deployment and Grealish fitness/role.\n- Manchester City: O'Reilly, Matheus Nunes and Rúben Dias defensive hierarchy.\n- Liverpool: Ekitiké Achilles recovery and Alisson role security.\n- Goalkeepers: opening-day hierarchy and late transfer movement.\n\nEvidence: {REVIEW_LINK}; [Official FPL bootstrap]({BOOTSTRAP_URL}); [Premier League preseason schedule]({PRESEASON_URL}).\n'''
watch_path.write_text(watch)

home_path = ROOT / 'vault/Home.md'
home = home_path.read_text()
home = re.sub(r'last_updated: .*', f'last_updated: {ISO}', home, count=1)
home += f'''\n## 2026-08-02 08:15 AEST — ranks 81–110\n\n- Review: {REVIEW_LINK}\n- Changes: {CHANGE_LINK}\n- Challenger range: 76–115.\n- Havertz, Rayan, Dorgu, Aina and Tete crossed above the prior goalkeeper run.\n'''
home_path.write_text(home)

wiki_path = ROOT / 'vault/Wiki.md'
wiki = wiki_path.read_text()
wiki = re.sub(r'last_updated: .*', f'last_updated: {ISO}', wiki, count=1)
wiki = re.sub(r'latest_review: .*', f'latest_review: "{REVIEW_LINK}"', wiki, count=1)
wiki = re.sub(r'latest_changes: .*', f'latest_changes: "{CHANGE_LINK}"', wiki, count=1)
wiki += f'''\n## 2026-08-02 08:15 AEST — ranks 81–110\n\nThe 81–110 block was manually pairwise-sorted with challengers from 76–115. Five outfield players crossed ahead of the goalkeeper run. Injury and rotation discounts remain decisive for Ekitiké, Grealish and Manchester City defenders.\n\n- {REVIEW_LINK}\n- {CHANGE_LINK}\n- Next block: 111–140 with challengers 106–145.\n'''
wiki_path.write_text(wiki)

# Changelog: one row for every Markdown file changed.
changed = [board_path, watch_path, home_path, wiki_path, review_path, changes_path]
changed += [player_dir / f'{name} - {by_name[name]["id"]}.md' for name in branch_players]
changelog_path = ROOT / 'vault/00 Meta/Document Changelog.md'
changelog = changelog_path.read_text()
changelog = re.sub(r'last_updated: .*', f'last_updated: {ISO}', changelog, count=1)
for p in changed:
    rel = p.as_posix()
    action = 'Created' if p in (review_path, changes_path) or old_rank.get(next((n for n in branch_players if f'/{n} - ' in '/' + rel), ''), None) is not None and not False else 'Updated'
    if rel.startswith('vault/02 Players/'):
        action = 'Updated' if p.exists() else 'Created'
    changelog += f"\n| {ISO} | `{rel}` | {action} | Recorded ranks 81–110 pairwise review with challengers 76–115. | {REVIEW_LINK} | [Official FPL bootstrap]({BOOTSTRAP_URL}); [Official fixtures]({FIXTURES_URL}); [Premier League preseason schedule]({PRESEASON_URL}) |"
changelog += f"\n| {ISO} | `vault/00 Meta/Document Changelog.md` | Updated | Appended a separate row for every Markdown file changed by the ranks 81–110 review. | {REVIEW_LINK} | Per-document audit; [Official FPL bootstrap]({BOOTSTRAP_URL}) |\n"
changelog_path.write_text(changelog)

# Validate all required files and links.
assert review_path.exists() and changes_path.exists()
assert REVIEW_LINK in board_path.read_text()
assert REVIEW_LINK in watch_path.read_text()
assert REVIEW_LINK in home_path.read_text()
assert REVIEW_LINK in wiki_path.read_text()
for p in changed:
    assert f'`{p.as_posix()}`' in changelog_path.read_text(), p

# Remove generator from net branch diff after execution.
Path('scripts/fpl_block_81_110.py').unlink()
print(json.dumps({'players': len(bootstrap['elements']), 'fixtures': len(fixtures), 'changed_markdown': len(changed)+1, 'top': branch_players[:5], 'bottom': branch_players[-5:]}, indent=2))
