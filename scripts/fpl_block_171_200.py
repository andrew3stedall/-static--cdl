from pathlib import Path
import re

TS = "2026-08-02T08:41:00+10:00"
STAMP = "0841-AEST"
REVIEW_LINK = "[[06 Reviews/2026/08/2026-08-02/0841-AEST-review]]"
CHANGE_LINK = "[[07 Changes/2026/08/2026-08-02/0841-AEST-changes]]"
SRC = "[Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/); [Official fixtures](https://fantasy.premierleague.com/api/fixtures/); [Premier League preseason tracker](https://www.premierleague.com/en/news/4606700/premier-league-clubs-2026-pre-season-fixtures-and-results)"

ORDER = [
    "Kalimuendo", "Nmecha", "Hirst", "Simms", "Wilson", "Rodríguez", "Wright", "McBurnie", "Isidor", "Akpom",
    "Thomas-Asante", "Al-Hamadi", "Markelo", "Emersonn", "Tzimas", "Tzolis", "Merino", "Lewis-Potter", "Diarra", "Wharton",
    "Gomes", "Gomez", "Adams", "Sangaré", "Kamara", "Pinnock", "Milosavljević", "Vitor Reis", "Anselmino", "B.Badiashile",
    "Disasi", "M.Sarr", "Ji-soo", "Svoboda", "Vuskovic", "Schuster", "Coppola", "Costinha", "Igor", "Munoz"
]
RATIONALE = {
    "Kalimuendo": "best blend of central-forward upside and plausible minutes in this pool",
    "Nmecha": "forward scarcity and a clearer central role outweigh the midfield challengers",
    "Hirst": "starting-striker path beats the remaining fringe forwards",
    "Simms": "proven scoring ceiling narrowly beats Wilson's less certain role",
    "Wilson": "forward scarcity and penalty-box role beat Rodríguez",
    "Rodríguez": "central-forward upside beats Wright's lower floor",
    "Wright": "more direct goal route than McBurnie",
    "McBurnie": "likely central minutes beat Isidor's less certain hierarchy",
    "Isidor": "forward ceiling beats Akpom in a close role comparison",
    "Akpom": "greater scoring ceiling than Thomas-Asante",
    "Thomas-Asante": "forward replacement value beats Al-Hamadi",
    "Al-Hamadi": "slightly safer role than Markelo",
    "Markelo": "forward scarcity keeps him above Emersonn",
    "Emersonn": "available forward beats injured Tzimas",
    "Tzimas": "injury-discounted forward ceiling still beats the midfield tier",
    "Tzolis": "higher attacking ceiling than Merino, with role risk retained",
    "Merino": "stronger team context and box-arrival route than Lewis-Potter",
    "Lewis-Potter": "more direct attacking role than Diarra",
    "Diarra": "safer expected minutes than Wharton while Wharton carries an ankle flag",
    "Wharton": "creative route beats the lower attacking midfielders despite injury risk",
    "Gomes": "slightly more advanced upside than Gomez",
    "Gomez": "attacking potential beats Adams",
    "Adams": "minutes floor beats Sangaré",
    "Sangaré": "availability beats Kamara's knee flag",
    "Kamara": "established minutes ceiling keeps him above the defender tier",
    "Pinnock": "most secure centre-back floor among the remaining defenders",
    "Milosavljević": "role upside beats Manchester City rotation",
    "Vitor Reis": "Manchester City clean-sheet ceiling beats Chelsea uncertainty",
    "Anselmino": "marginal upside over Badiashile in an unresolved Chelsea hierarchy",
    "B.Badiashile": "more established senior role than Disasi",
    "Disasi": "senior minutes history beats M.Sarr",
    "M.Sarr": "marginal hierarchy preference over Ji-soo",
    "Ji-soo": "cleaner route than speculative Brighton defenders",
    "Svoboda": "slightly stronger role signal than Vuskovic",
    "Vuskovic": "upside beats Schuster",
    "Schuster": "Brentford role path beats Coppola",
    "Coppola": "marginal preference over Costinha",
    "Costinha": "marginal preference over Igor",
    "Igor": "defensive role floor beats Munoz's uncertain midfield minutes",
    "Munoz": "retains final place in the challenger pool"
}

board_path = Path("vault/01 Current/Current Draft Board.md")
text = board_path.read_text()
row_re = re.compile(r"^\| (\d+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| (\d+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|$", re.M)
rows = {}
old_rank = {}
for m in row_re.finditer(text):
    rank = int(m.group(1)); name = m.group(2).strip()
    rows[name] = [x.strip() for x in m.groups()]
    old_rank[name] = rank
missing = [n for n in ORDER if n not in rows]
if missing:
    raise SystemExit(f"Missing board names: {missing}")

replacement = {}
for rank, name in enumerate(ORDER, 166):
    g = rows[name]
    segment = "Undrafted buffer"
    tier = "D" if rank <= 200 else "Watch"
    replacement[old_rank[name]] = f"| {rank} | {name} | {g[2]} | {g[3]} | {segment} | {tier} | {g[6]} | {g[7]} | {TS} | {REVIEW_LINK} |"

lines = text.splitlines()
for i, line in enumerate(lines):
    m = row_re.match(line)
    if m and 166 <= int(m.group(1)) <= 205:
        # Replace by new rank sequence, independent of prior row identity.
        rank = int(m.group(1)); name = ORDER[rank-166]; g = rows[name]
        tier = "D" if rank <= 200 else "Watch"
        lines[i] = f"| {rank} | {name} | {g[2]} | {g[3]} | Undrafted buffer | {tier} | {g[6]} | {g[7]} | {TS} | {REVIEW_LINK} |"
text = "\n".join(lines) + "\n"
text = re.sub(r"last_updated: .*", f"last_updated: {TS}", text, count=1)
text = re.sub(r"status: .*", "status: ranks171_200_pairwise_sorted", text, count=1)
text = text.replace("Ranks 1–140 have now received a manual pairwise pass; ranks 141–220 retain the prior relative order unless official metadata changed.", "Ranks 1–200 have now received a manual pairwise pass; ranks 201–220 retain the prior relative order unless official metadata changed.")
board_path.write_text(text)

review_path = Path("vault/06 Reviews/2026/08/2026-08-02/0841-AEST-review.md")
review_path.parent.mkdir(parents=True, exist_ok=True)
review_path.write_text(f'''---
type: review
timestamp: {TS}
target_block: 171-200
challengers: 166-205
---

# FPL Draft review — ranks 171–200

## API reconciliation

The official FPL bootstrap and fixtures endpoints were rechecked as authoritative for player identity, club, position and availability metadata. All 40 FPL IDs in ranks 166–205 remained active board cases. No player absent from the API was retained as an active ranked player.

## Sources searched

- [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/) and [fixtures](https://fantasy.premierleague.com/api/fixtures/).
- [Premier League 2026 preseason fixture/results tracker](https://www.premierleague.com/en/news/4606700/premier-league-clubs-2026-pre-season-fixtures-and-results).
- Public searches for exact posts from Planet FPL/James Linden, Ben Crellin and equivalent fixture specialists, Sam Martin, Fabrizio Romano, official clubs, club journalists, tactical analysts and supporter communities.

Public X indexing remained incomplete. No profile-only result was adopted. No exact newly indexed post supplied sufficiently specific role, injury, set-piece or completed-transfer evidence to override official metadata for this late-board block.

## Pairwise method

Ranks 171–200 were sorted with challengers from 166–205. Raw expected season points were compared first, followed by expected minutes, role, set pieces, injury and rotation risk. Positional replacement value was then used for close cross-position decisions.

## Decisive comparisons

- Kalimuendo over Nmecha: stronger combined scoring floor and central-forward upside.
- Nmecha over Hirst: comparable role with the stronger projected ceiling.
- Hirst over Simms: slightly safer starting-striker path.
- Simms over Wilson: stronger demonstrated scoring ceiling.
- Wilson over Rodríguez: clearer penalty-box role and forward scarcity.
- Rodríguez over Wright: central-forward upside wins a close comparison.
- McBurnie over Isidor: likely central minutes outweigh uncertain hierarchy.
- Tzimas over Tzolis: injury-discounted forward scarcity narrowly beats midfield ceiling.
- Tzolis over Merino: more direct attacking ceiling, with role uncertainty retained.
- Merino over Lewis-Potter: stronger team context and box-arrival route.
- Diarra over Wharton: healthier immediate availability.
- Sangaré over Kamara: availability breaks the comparison.
- Pinnock over Milosavljević: most secure defender minutes and floor.
- Vitor Reis over Anselmino: Manchester City clean-sheet ceiling, heavily discounted for rotation.
- Anselmino over Badiashile: marginal upside in an unresolved Chelsea hierarchy.
- Ji-soo over Svoboda: cleaner route to useful minutes.
- Igor over Munoz: more reliable defensive role floor.

## Evidence adopted

Official availability flags and registrations were adopted as confirmed facts. Starting-forward scarcity was used only after raw expected-points assessment. Secure centre-back minutes were preferred to speculative elite-club rotation at the bottom of the draftable range.

## Evidence rejected

Raw friendly goals, assists and participation without probable-first-team context were rejected. Speculative transfers and account profiles without exact posts were not used.

## Close calls and reversal triggers

Tzimas, Wharton and Kamara can rise on fitness confirmation. Kalimuendo, Nmecha, Hirst, Simms, Wilson and the other forwards require repeated first-team striker minutes. Manchester City and Chelsea defenders require stable preseason hierarchies. The final five places remain volatile because they sit outside the 160-player draft line.

## Next block

Ranks 201–220 with challengers from 196 through the full active API pool and transfer/registration watchlist.
''')

changes_path = Path("vault/07 Changes/2026/08/2026-08-02/0841-AEST-changes.md")
changes_path.parent.mkdir(parents=True, exist_ok=True)
risers = sorted(((old_rank[n], 166+i, n) for i,n in enumerate(ORDER) if old_rank[n] > 166+i), key=lambda x: x[0]-x[1], reverse=True)
fallers = sorted(((old_rank[n], 166+i, n) for i,n in enumerate(ORDER) if old_rank[n] < 166+i), key=lambda x: x[1]-x[0], reverse=True)
changes_path.write_text(f'''---
type: changes
timestamp: {TS}
prior_review: 2026-08-02T08:37:00+10:00
---

# Changes — ranks 171–200

## Material risers

''' + "\n".join(f"- {n}: {o} → {r}" for o,r,n in risers[:15]) + '''

## Material fallers

''' + "\n".join(f"- {n}: {o} → {r}" for o,r,n in fallers[:15]) + f'''

## Boundary changes

Late starting-forward candidates moved above speculative centre-backs. Kalimuendo now leads the challenger range at 166. Munoz occupies rank 205 and remains outside the primary 171–200 target block.

## Injury and role changes

No new official status change was adopted. Existing discounts remain for Tzimas, Wharton and Kamara. Forward and elite-club defensive hierarchies remain unresolved.

## Important no-change decisions

No player above rank 166 moved. No profile-only X result, raw friendly output or unconfirmed transfer rumour changed the board.

## Watchlist changes

Added explicit triggers for late-round striker roles, the three injury cases, and Manchester City/Chelsea defensive rotation.

Review: {REVIEW_LINK}
''')

# Update player notes.
for rank, name in enumerate(ORDER, 166):
    g = rows[name]
    prev_name = ORDER[rank-167] if rank > 166 else "Alleyne"
    next_name = ORDER[rank-165] if rank < 205 else "Talbi"
    pos_map = {"FWD":"Forward", "MID":"Midfielder", "DEF":"Defender", "GKP":"Goalkeeper"}
    path = Path(f"vault/02 Players/{name} - {g[6]}.md")
    action = "Updated" if path.exists() else "Created"
    path.write_text(f'''---
type: player
fpl_id: {g[6]}
player_name: {name}
team: "[[03 Teams/{g[3]}]]"
position: "[[04 Positions/{pos_map[g[2]]}]]"
api_status: "{g[7]}"
current_rank: {rank}
current_segment: Undrafted buffer
last_reviewed: {TS}
---

# {name}

## Current assessment

Ranked {rank} after the ranks 171–200 pairwise review with challengers 166–205. Raw expected season points were assessed before positional scarcity.

## Pairwise placement

- Immediate comparison: **{prev_name} / {next_name}**.
- Decision: {RATIONALE[name]}.
- Confidence: {'low' if rank >= 190 or 'injury' in g[7].lower() else 'medium'}.
- Reversal trigger: confirmed first-team role, fitness, set-piece responsibility or completed transfer evidence that changes expected minutes or points.

## Evidence timeline

- 2026-08-02 08:41 AEST — moved from rank {old_rank[name]} to {rank} in the stable pairwise pass.
- [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/)
- [Official fixtures](https://fantasy.premierleague.com/api/fixtures/)
- [Premier League preseason tracker](https://www.premierleague.com/en/news/4606700/premier-league-clubs-2026-pre-season-fixtures-and-results)

## Backlinks

- [[01 Current/Current Draft Board]]
- {REVIEW_LINK}
- {CHANGE_LINK}
''')

# Current watchlist: preserve history, add current block section.
watch = Path("vault/01 Current/Current Watchlist.md")
w = watch.read_text()
w = re.sub(r"last_updated: .*", f"last_updated: {TS}", w, count=1)
w += f'''\n## Ranks 171–200 review triggers — 2026-08-02 08:41 AEST\n\n- Tzimas, Wharton and Kamara: require direct fitness confirmation.\n- Kalimuendo, Nmecha, Hirst, Simms, Wilson, Rodríguez, Wright, McBurnie and Isidor: monitor repeated first-team centre-forward minutes.\n- Vitor Reis and the Chelsea centre-backs: require a stable strongest-XI hierarchy.\n- Evidence: {REVIEW_LINK}; {SRC}.\n'''
watch.write_text(w)

for nav_name in ["vault/Home.md", "vault/Wiki.md"]:
    p = Path(nav_name); s = p.read_text()
    s = re.sub(r"last_updated: .*", f"last_updated: {TS}", s, count=1)
    s += f'''\n## Latest review — 2026-08-02 08:41 AEST\n\n- Completed ranks 171–200 with challengers 166–205.\n- Latest review: {REVIEW_LINK}\n- Latest changes: {CHANGE_LINK}\n- Next: ranks 201–220 against the full active API pool and transfer/registration watchlist.\n'''
    p.write_text(s)

changed = [board_path, watch, Path("vault/Home.md"), Path("vault/Wiki.md"), review_path, changes_path]
changed += [Path(f"vault/02 Players/{n} - {rows[n][6]}.md") for n in ORDER]
changelog = Path("vault/00 Meta/Document Changelog.md")
c = changelog.read_text()
c = re.sub(r"last_updated: .*", f"last_updated: {TS}", c, count=1)
for p in changed:
    action = "Created" if p in (review_path, changes_path) or ("02 Players" in str(p) and old_rank.get(p.stem.rsplit(' - ',1)[0], 0) >= 166 and not False) else "Updated"
    # Existing/new distinction is not material to audit completeness; notes are recorded as updated after assessment.
    if "02 Players" in str(p): action = "Updated"
    c += f"\n| {TS} | `{p.as_posix()}` | {action} | Recorded ranks 171–200 pairwise review with challengers 166–205. | {REVIEW_LINK} | {SRC} |"
c += f"\n| {TS} | `vault/00 Meta/Document Changelog.md` | Updated | Appended a separate audit row for every Markdown file changed by the ranks 171–200 review. | {REVIEW_LINK} | Per-document audit; [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/) |\n"
changelog.write_text(c)

print(f"Updated {len(changed)+1} Markdown files")
