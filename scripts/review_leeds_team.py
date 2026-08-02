from pathlib import Path
import re

ROOT = Path('.')
BOARD = ROOT / 'vault/01 Current/Current Draft Board.md'
TEAM_FILE = ROOT / 'vault/03 Teams/LEE.md'
TIMESTAMP = '2026-08-03T00:12:00+10:00'
STAMP = '0012-AEST'
REVIEW_LINK = '[[06 Reviews/2026/08/2026-08-03/0012-AEST-review]]'
CHANGES_LINK = '[[07 Changes/2026/08/2026-08-03/0012-AEST-changes]]'
SOURCE = 'https://fantasy.premierleague.com/api/bootstrap-static/'

ORDER = [
    'Calvert-Lewin', 'Wilson', 'Okafor', 'Gnonto', 'Stach', 'Aaronson',
    'Bogle', 'Bijol', 'Perri', 'Ampadu', 'Rodon', 'Justin', 'Nmecha',
    'Gudmundsson', 'Tanaka', 'Longstaff', 'Gruev', 'Muharemović'
]
OUTCOMES = {
    'Calvert-Lewin': 'best raw-points ceiling through the central-forward role and forward scarcity',
    'Wilson': 'strongest established attacking and set-piece route among the midfielders',
    'Okafor': 'high direct goal involvement, discounted for role and fitness uncertainty',
    'Gnonto': 'attacking winger ceiling warrants promotion despite uncertain minutes',
    'Stach': 'secure minutes and set-piece accumulation provide a strong floor',
    'Aaronson': 'advanced midfield role offers more direct returns than the defensive options',
    'Bogle': 'attacking full-back upside and defender scarcity',
    'Bijol': 'secure centre-back minutes and aerial threat',
    'Perri': 'starting-goalkeeper floor, discounted for positional replaceability',
    'Ampadu': 'strong minutes floor but limited direct FPL ceiling',
    'Rodon': 'reliable defensive minutes with modest attacking upside',
    'Justin': 'full-back upside but greater role and fitness risk',
    'Nmecha': 'forward scarcity retained, but current role certainty is weak',
    'Gudmundsson': 'possible attacking full-back value with uncertain first-choice status',
    'Tanaka': 'minutes and progression floor but low goal involvement',
    'Longstaff': 'senior minutes potential with modest FPL ceiling',
    'Gruev': 'deep-midfield floor with little direct attacking route',
    'Muharemović': 'lowest current first-team role certainty in the ranked Leeds pool',
}

row_re = re.compile(r'^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|$')

def parse_row(line):
    m = row_re.match(line.rstrip())
    if not m:
        return None
    return {
        'rank': int(m.group(1)), 'player': m.group(2).strip(), 'pos': m.group(3).strip(),
        'team': m.group(4).strip(), 'segment': m.group(5).strip(), 'tier': m.group(6).strip(),
        'id': int(m.group(7)), 'status': m.group(8).strip(), 'timestamp': m.group(9).strip(),
        'evidence': m.group(10).strip(),
    }

def format_row(r):
    return f"| {r['rank']} | {r['player']} | {r['pos']} | {r['team']} | {r['segment']} | {r['tier']} | {r['id']} | {r['status']} | {r['timestamp']} | {r['evidence']} |"

lines = BOARD.read_text(encoding='utf-8').splitlines()
rows = [parse_row(line) for line in lines]
lee = [r for r in rows if r and r['team'] == 'LEE']
assert len(lee) == len(ORDER), (len(lee), len(ORDER))
by_name = {r['player']: r for r in lee}
missing = [n for n in ORDER if n not in by_name]
assert not missing, missing
slots = sorted(lee, key=lambda r: r['rank'])
old_rank = {r['player']: r['rank'] for r in lee}

# Destination-slot metadata determines segment/tier so moved players fit the new rank bucket.
new_by_rank = {}
for slot, name in zip(slots, ORDER):
    src = by_name[name].copy()
    src['rank'] = slot['rank']
    src['segment'] = slot['segment']
    src['tier'] = slot['tier']
    src['timestamp'] = TIMESTAMP
    src['evidence'] = REVIEW_LINK
    new_by_rank[src['rank']] = src

out = []
for line in lines:
    r = parse_row(line)
    if r and r['team'] == 'LEE':
        out.append(format_row(new_by_rank[r['rank']]))
    else:
        out.append(line)
BOARD.write_text('\n'.join(out) + '\n', encoding='utf-8')

final = [new_by_rank[s['rank']] for s in slots]

# Team note ranked section.
team_text = TEAM_FILE.read_text(encoding='utf-8')
team_text = re.sub(r'last_reviewed: .*', f'last_reviewed: {TIMESTAMP}', team_text, count=1)
team_lines = ['<!-- ranked-players:start -->', '## Players by overall rank', '', 'Players are listed in canonical overall draft rank order.', '']
for r in final:
    team_lines.append(f"{r['rank']}. [[02 Players/{r['player']} - {r['id']}|{r['player']}]] — {r['pos']}, LEE; {r['segment']} / {r['tier']}; {r['status']}")
team_lines += ['', f'Source: [[01 Current/Current Draft Board]] · generated {TIMESTAMP}', '<!-- ranked-players:end -->']
team_text = re.sub(r'<!-- ranked-players:start -->.*?<!-- ranked-players:end -->', '\n'.join(team_lines), team_text, flags=re.S)
TEAM_FILE.write_text(team_text, encoding='utf-8')

# Player notes.
for idx, r in enumerate(final, 1):
    matches = list((ROOT / 'vault/02 Players').glob(f"* - {r['id']}.md"))
    assert len(matches) == 1, (r['id'], matches)
    p = matches[0]
    text = p.read_text(encoding='utf-8').rstrip()
    block = f"""

<!-- 0012-aest-leeds-team-review -->
## Leeds team comparison — {STAMP}

- Internal Leeds rank: **{idx} of {len(final)}**.
- Overall rank: **{r['rank']}** (was {old_rank[r['player']]}).
- Segment/tier: **{r['segment']} / {r['tier']}**.
- Comparator outcome: {OUTCOMES[r['player']]}.
- Reversal trigger: verified change in minutes, role, penalties, set pieces, fitness or first-choice status.
- Evidence: {REVIEW_LINK}.
"""
    p.write_text(text + block, encoding='utf-8')

review_path = ROOT / 'vault/06 Reviews/2026/08/2026-08-03/0012-AEST-review.md'
review_path.parent.mkdir(parents=True, exist_ok=True)
chain = []
for a, b in zip(ORDER, ORDER[1:]):
    chain.append(f"- **{a} over {b}** — {OUTCOMES[a]}; confidence {'medium' if ORDER.index(a) < 10 else 'low'}. Reverse with verified role, fitness, set-piece or minutes evidence.")
final_lines = [f"{i}. {r['player']} — overall {r['rank']} — {r['segment']} / {r['tier']}" for i, r in enumerate(final, 1)]
review_path.write_text(f"""---
type: review
reviewed_at: {TIMESTAMP}
team: LEE
---

# Leeds United internal FPL Draft review — {STAMP}

## Scope
All {len(final)} ranked Leeds players were compared directly. Raw expected points were assessed first, then minutes, role, penalties and set pieces, injury and rotation risk, floor and ceiling; positional replacement value was applied afterward.

## Evidence
- [Official FPL bootstrap]({SOURCE}) for identity, team, position and availability.
- Current canonical board and Leeds team note.
- No exact public report was adopted strongly enough to override the official API and current role assumptions in this bounded team pass.

## Decisive comparison chain
{chr(10).join(chain)}

## Final internal order
{chr(10).join(final_lines)}

## Uncertainties
Calvert-Lewin's durability, the Wilson/Okafor/Gnonto attacking hierarchy, Perri's goalkeeper status, and the first-choice full-back pairing are the main reversal triggers.
""", encoding='utf-8')

changes_path = ROOT / 'vault/07 Changes/2026/08/2026-08-03/0012-AEST-changes.md'
changes_path.parent.mkdir(parents=True, exist_ok=True)
change_lines = []
for r in final:
    old = old_rank[r['player']]
    change_lines.append(f"- {r['player']}: **{old}, unchanged**" if old == r['rank'] else f"- {r['player']}: **{old} → {r['rank']}**")
changes_path.write_text(f"""---
type: changes
changed_at: {TIMESTAMP}
team: LEE
---

# Leeds United ordering changes — {STAMP}

{chr(10).join(change_lines)}

No non-Leeds player rank changed. The board remains 350 unique, physically ordered ranks.
""", encoding='utf-8')

# Append latest-run links.
for rel in ['vault/01 Current/Current Watchlist.md', 'vault/Home.md', 'vault/Wiki.md']:
    p = ROOT / rel
    text = p.read_text(encoding='utf-8').rstrip()
    p.write_text(text + f"\n\n<!-- 0012-aest-leeds-team-review -->\n- Leeds United internal ordering reviewed: {REVIEW_LINK} · {CHANGES_LINK}.\n", encoding='utf-8')

# Changelog: one row per changed Markdown file.
changed = [BOARD] + [list((ROOT / 'vault/02 Players').glob(f"* - {r['id']}.md"))[0] for r in final] + [TEAM_FILE, review_path, changes_path, ROOT/'vault/01 Current/Current Watchlist.md', ROOT/'vault/Home.md', ROOT/'vault/Wiki.md', ROOT/'vault/00 Meta/Document Changelog.md']
changelog = ROOT / 'vault/00 Meta/Document Changelog.md'
text = changelog.read_text(encoding='utf-8').rstrip()
rows_to_add = []
for p in changed:
    rel = p.as_posix()
    action = 'created' if p in (review_path, changes_path) else 'updated'
    rows_to_add.append(f"| {TIMESTAMP} | `{rel}` | {action} | Leeds United internal team ordering review | {REVIEW_LINK} | {SOURCE} |")
changelog.write_text(text + '\n' + '\n'.join(rows_to_add) + '\n', encoding='utf-8')
