from pathlib import Path
import re

ROOT = Path('.')
BOARD = ROOT / 'vault/01 Current/Current Draft Board.md'
TEAM = ROOT / 'vault/03 Teams/COV.md'
STAMP = '2026-08-03T08:45:00+10:00'
HHMM = '0845-AEST'
REVIEW_LINK = '[[06 Reviews/2026/08/2026-08-03/0845-AEST-review]]'
CHANGES_LINK = '[[07 Changes/2026/08/2026-08-03/0845-AEST-changes]]'

TARGET = ['Wright', 'Simms', 'van Ewijk', 'Thomas', 'Wilson', 'Thomas-Asante', 'Markelo']
REASONS = {
    'Wright': 'Best combination of central attacking role, penalty potential and forward scarcity; role certainty is the main reversal trigger.',
    'Simms': 'Central-forward ceiling and established scoring route keep him just behind Wright and ahead of the defenders.',
    'van Ewijk': 'Attacking full-back upside and a steadier minutes path make him the leading Coventry defender.',
    'Thomas': 'Centre-back minutes and set-piece threat provide a safer floor than the remaining speculative attackers.',
    'Wilson': 'Starting-goalkeeper floor is useful, but goalkeeper replacement value keeps him behind the leading outfield options.',
    'Thomas-Asante': 'Forward classification preserves upside, but uncertain starts and role competition limit draft priority.',
    'Markelo': 'Lowest current minutes confidence and weakest established FPL route among the ranked Coventry group.'
}

text = BOARD.read_text()
lines = text.splitlines()
row_re = re.compile(r'^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|')
rows = {}
slots = []
for i, line in enumerate(lines):
    m = row_re.match(line)
    if not m:
        continue
    rank = int(m.group(1)); player = m.group(2).strip(); team = m.group(4).strip()
    if team == 'COV':
        rows[player] = (i, line, rank)
        slots.append(rank)

missing = [p for p in TARGET if p not in rows]
if missing or len(rows) != len(TARGET):
    raise SystemExit(f'Coventry player mismatch missing={missing} found={list(rows)}')
slots = sorted(slots)
old_rank = {p: rows[p][2] for p in TARGET}
slot_lines = {rows[p][2]: rows[p][1] for p in TARGET}

# Rebuild each destination row using the chosen player row but destination segment/tier.
def cells(line):
    return [c.strip() for c in line.strip().strip('|').split('|')]
new_rank = {}
for player, rank in zip(TARGET, slots):
    src = cells(rows[player][1])
    dst = cells(slot_lines[rank])
    src[0] = str(rank)
    src[4] = dst[4]
    src[5] = dst[5]
    src[8] = STAMP
    src[9] = REVIEW_LINK
    lines[next(i for i,l in enumerate(lines) if row_re.match(l) and int(row_re.match(l).group(1)) == rank)] = '| ' + ' | '.join(src) + ' |'
    new_rank[player] = rank
BOARD.write_text('\n'.join(lines) + '\n')

# Update team note ranked section.
board_rows = {}
for line in BOARD.read_text().splitlines():
    m = row_re.match(line)
    if m:
        c = cells(line)
        board_rows[c[1]] = c
team_text = TEAM.read_text()
start = team_text.index('<!-- ranked-players:start -->')
end = team_text.index('<!-- ranked-players:end -->') + len('<!-- ranked-players:end -->')
ranked = ['<!-- ranked-players:start -->', '## Players by overall rank', '', 'Players are listed in canonical overall draft rank order.', '']
for p in TARGET:
    c = board_rows[p]
    ranked.append(f"{c[0]}. [[02 Players/{p} - {c[6]}|{p}]] — {c[2]}, COV; {c[4]} / {c[5]}; {c[7]}")
ranked += ['', f'Source: [[01 Current/Current Draft Board]] · generated {STAMP}', '<!-- ranked-players:end -->']
team_text = team_text[:start] + '\n'.join(ranked) + team_text[end:]
team_text = re.sub(r'last_reviewed: .*', f'last_reviewed: {STAMP}', team_text, count=1)
team_text += f"\n\n## {HHMM} team review\n\n- Full Coventry intra-team ordering reviewed.\n- Review: {REVIEW_LINK}.\n"
TEAM.write_text(team_text)

# Update each player note.
changed_md = [BOARD, TEAM]
for p in TARGET:
    fid = board_rows[p][6]
    path = ROOT / f'vault/02 Players/{p} - {fid}.md'
    if not path.exists():
        raise SystemExit(f'Missing player note: {path}')
    body = path.read_text()
    body += f"\n\n## {HHMM} Coventry comparison\n\n- Coventry order: **{TARGET.index(p)+1} of {len(TARGET)}**; overall rank **{new_rank[p]}**.\n- Decision: {REASONS[p]}\n- Evidence: {REVIEW_LINK}.\n"
    path.write_text(body)
    changed_md.append(path)

review_path = ROOT / 'vault/06 Reviews/2026/08/2026-08-03/0845-AEST-review.md'
review_path.parent.mkdir(parents=True, exist_ok=True)
comparisons = [
    ('Wright','Simms','Wright','Close: Wright is preferred for the broader scoring and penalty route; a clear Simms starting-striker role would reverse it.'),
    ('Simms','van Ewijk','Simms','Raw attacking points and forward scarcity outweigh van Ewijk’s safer defensive minutes.'),
    ('van Ewijk','Thomas','van Ewijk','Attacking full-back route beats the centre-back floor.'),
    ('Thomas','Wilson','Thomas','Outfield clean-sheet and set-piece upside beats a replaceable goalkeeper.'),
    ('Wilson','Thomas-Asante','Wilson','Safer season-long minutes floor; regular starts for Thomas-Asante would reverse it.'),
    ('Thomas-Asante','Markelo','Thomas-Asante','More established senior scoring profile and clearer forward route.')
]
review = [f'---\ntype: review\nreviewed_at: {STAMP}\nteam: COV\n---', '', '# Coventry City team ordering review', '', '## Scope', '', 'Reviewed all seven Coventry players currently ranked on the canonical 350-player board. West Ham was skipped because it is absent from the current canonical FPL team pool and vault.', '', '## Comparator method', '', 'Raw expected FPL points were considered first, then minutes, role, set pieces, injury/rotation risk, floor and ceiling. Positional replacement value was applied only afterward.', '', '## Decisive comparisons', '']
for a,b,w,why in comparisons:
    review.append(f'- **{a} vs {b}: {w} first.** {why}')
review += ['', '## Final Coventry order', ''] + [f'{i+1}. {p} — overall {new_rank[p]}' for i,p in enumerate(TARGET)]
review += ['', '## Uncertainties and reversal triggers', '', '- Coventry attacking hierarchy and penalty ownership require confirmation from competitive first-team minutes.', '- Any player missing from the current official FPL pool must be removed or relabelled rather than retained as an active rank.', '- The bottom three remain watch-level rather than reliable draft selections.', '', '## Validation', '', '- Only Coventry occupied rank slots were reassigned.', '- Non-Coventry ranks were preserved.', '- The canonical board validator must confirm ranks 1–350 are complete and FPL IDs unique.']
review_path.write_text('\n'.join(review) + '\n')
changed_md.append(review_path)

changes_path = ROOT / 'vault/07 Changes/2026/08/2026-08-03/0845-AEST-changes.md'
changes_path.parent.mkdir(parents=True, exist_ok=True)
changes = [f'---\ntype: changes\nchanged_at: {STAMP}\nteam: COV\n---', '', '# Coventry City ordering changes — 0845-AEST', '']
for p in TARGET:
    changes.append(f"- {p}: **{old_rank[p]}{' → ' + str(new_rank[p]) if old_rank[p] != new_rank[p] else ', unchanged'}**")
changes += ['', 'No non-Coventry player rank changed. West Ham was not reviewed because it is absent from the current canonical FPL team pool. The board remains 350 unique, physically ordered ranks.']
changes_path.write_text('\n'.join(changes) + '\n')
changed_md.append(changes_path)

# Update Home and Wiki latest-run links.
for rel in ['vault/Home.md', 'vault/Wiki.md']:
    path = ROOT / rel
    body = path.read_text()
    body += f"\n\n- Latest team review: {REVIEW_LINK} · changes: {CHANGES_LINK}\n"
    path.write_text(body)
    changed_md.append(path)

# Append one changelog row for every Markdown file changed or created.
cl = ROOT / 'vault/00 Meta/Document Changelog.md'
cl_body = cl.read_text()
for path in changed_md:
    rel = path.as_posix()
    action = 'Created' if path in (review_path, changes_path) else 'Updated'
    cl_body += f"\n| {STAMP} | `{rel}` | {action} | Coventry intra-team review and rank reconciliation | {REVIEW_LINK} | {REVIEW_LINK}; {CHANGES_LINK} |"
cl.write_text(cl_body)
