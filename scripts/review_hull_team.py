from pathlib import Path

TS='2026-08-03T09:03:00+10:00'
STAMP='0903-AEST'
review='06 Reviews/2026/08/2026-08-03/0903-AEST-review'
changes='07 Changes/2026/08/2026-08-03/0903-AEST-changes'
root=Path('vault')

review_text=f'''---
type: review
reviewed_at: {TS}
team: HUL
---

# Hull City team ordering review

## Scope

Reviewed every Hull City player on the canonical 350-player draft board. Only McBurnie is currently ranked, so there was no intra-team pairwise boundary to reorder.

## Comparator outcome

- **McBurnie remains Hull rank 1 and overall rank 216.** His forward classification, probable central role and aerial goal threat preserve speculative draft value, but uncertain Premier League minutes, limited set-piece ownership and team-strength risk keep him in the undrafted buffer.
- No second ranked Hull player exists to justify a direct promotion or demotion within the club.

## Confidence and reversal triggers

Confidence is low. Reassess immediately for confirmed starting status, penalties, repeated first-team minutes, a competing striker signing, injury, suspension, or official FPL pool changes.

## Validation

- No rank was changed or manufactured.
- Non-Hull players were untouched.
- The canonical validator confirmed ranks 1–350 are complete and FPL IDs unique.
'''
changes_text=f'''---
type: changes
changed_at: {TS}
team: HUL
---

# Hull City ordering changes — {STAMP}

- McBurnie: **216, unchanged**

Hull has only one ranked player, so no intra-team rank swap was possible. No non-Hull player changed. The board remains 350 unique, physically ordered ranks.
'''
(root/review).with_suffix('.md').parent.mkdir(parents=True,exist_ok=True)
(root/review).with_suffix('.md').write_text(review_text)
(root/changes).with_suffix('.md').parent.mkdir(parents=True,exist_ok=True)
(root/changes).with_suffix('.md').write_text(changes_text)

team=root/'03 Teams/HUL.md'
t=team.read_text()
t=t.replace('last_reviewed: 2026-08-02T18:10:00+10:00',f'last_reviewed: {TS}')
t=t.replace('generated 2026-08-02T18:10:00+10:00',f'generated {TS}')
t += f'\n\n## {STAMP} team review\n\n- Hull has one ranked player; McBurnie remains first internally and 216 overall.\n- Review: [[{review}]].\n'
team.write_text(t)

player=root/'02 Players/McBurnie - 295.md'
p=player.read_text()
p=p.replace('last_reviewed: 2026-08-02T12:59:00+10:00',f'last_reviewed: {TS}')
p += f'''\n\n## {STAMP} Hull comparison\n\n- Hull order: **1 of 1**; overall rank **216**, unchanged.\n- Decision: No same-team challenger exists; retain as a low-confidence forward watch option.\n- Evidence: [[{review}]].\n'''
player.write_text(p)

for name in ['Home.md','Wiki.md']:
    f=root/name
    s=f.read_text()
    s += f'\n\n<!-- 0903-aest-hull-team-review -->\n- Hull City internal ordering reviewed: [[{review}]] · [[{changes}]].\n'
    f.write_text(s)

changed=[
'vault/02 Players/McBurnie - 295.md','vault/03 Teams/HUL.md',
'vault/06 Reviews/2026/08/2026-08-03/0903-AEST-review.md',
'vault/07 Changes/2026/08/2026-08-03/0903-AEST-changes.md','vault/Home.md','vault/Wiki.md']
cl=root/'00 Meta/Document Changelog.md'
s=cl.read_text()
for path in changed:
    action='Created' if '/06 Reviews/' in path or '/07 Changes/' in path else 'Updated'
    s += f'\n| {TS} | `{path}` | {action} | Hull City single-player team review | [[{review}]] | https://fantasy.premierleague.com/api/bootstrap-static/ |'
s += f'\n| {TS} | `vault/00 Meta/Document Changelog.md` | Updated | Hull City single-player team review | [[{review}]] | https://fantasy.premierleague.com/api/bootstrap-static/ |\n'
cl.write_text(s)
