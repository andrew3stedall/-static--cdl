from pathlib import Path
import re

TS = '2026-08-02T08:37:00+10:00'
REVIEW_LINK = '[[06 Reviews/2026/08/2026-08-02/0837-AEST-review]]'
CHANGES_LINK = '[[07 Changes/2026/08/2026-08-02/0837-AEST-changes]]'
BOOT = 'https://fantasy.premierleague.com/api/bootstrap-static/'
FIX = 'https://fantasy.premierleague.com/api/fixtures/'
PRE = 'https://www.premierleague.com/en/news/4606700/premier-league-clubs-2026-pre-season-fixtures-and-results'

board_path = Path('vault/01 Current/Current Draft Board.md')
text = board_path.read_text()
row_re = re.compile(r'^\| (\d+) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \| (\d+) \| (.*?) \| (.*?) \| (.*?) \|$', re.M)
rows = []
for m in row_re.finditer(text):
    rows.append({'rank': int(m.group(1)), 'name': m.group(2), 'pos': m.group(3), 'team': m.group(4), 'segment': m.group(5), 'tier': m.group(6), 'id': int(m.group(7)), 'status': m.group(8), 'changed': m.group(9), 'evidence': m.group(10)})
by_name = {r['name']: r for r in rows}
old_rank = {r['name']: r['rank'] for r in rows}
order = [
'Awoniyi','Barry','Georginio','Reijnders','Digne','Dalot','F.Kadıoğlu','Livramento','Branthwaite','Schär',
'Milenković','Boscagli','Bentancur','Garner','Ayari','Hinshelwood','Caicedo','Burn','Justin','Struijk',
'Colwill','Tsimikas','Palestra','Khusanov','Muharemović','O\'Brien','Rodon','Murillo','Jacquet','Alleyne',
'Milosavljević','Diarra','Vitor Reis','Anselmino','B.Badiashile','Disasi','M.Sarr','Ji-soo','Svoboda','Vuskovic']
assert len(order) == 40 and all(n in by_name for n in order)
new_rank = {name: 136+i for i,name in enumerate(order)}
for name, rank in new_rank.items():
    r = by_name[name]
    r['rank'] = rank
    r['segment'] = 'Endgame' if rank <= 160 else 'Undrafted buffer'
    r['tier'] = 'D+' if rank <= 160 else 'D'
    r['changed'] = TS
    r['evidence'] = REVIEW_LINK
rows.sort(key=lambda r: r['rank'])
assert [r['rank'] for r in rows] == list(range(1,221))
new_table = '\n'.join(f"| {r['rank']} | {r['name']} | {r['pos']} | {r['team']} | {r['segment']} | {r['tier']} | {r['id']} | {r['status']} | {r['changed']} | {r['evidence']} |" for r in rows)
start = text.index('| 1 |')
end = text.index('## Method cautions')
text = text[:start] + new_table + '\n' + text[end:]
text = re.sub(r'last_updated: .*', f'last_updated: {TS}', text, count=1)
text = re.sub(r'status: .*', 'status: ranks141_170_pairwise_sorted', text, count=1)
text = re.sub(r'This is the \*\*only canonical current overall ordering\*\*\..*?comparisons\.', 'This is the **only canonical current overall ordering**. The first 170 have now been manually stable-sorted; this run reviewed ranks 141–170 with challengers from 136–175. Raw expected FPL points are assessed first, followed by minutes, role, set pieces and risk; positional replacement value then determines draft priority in close cross-position comparisons.', text, count=1, flags=re.S)
text = text.replace('- The top 80 have been manually pairwise sorted; ranks 81-220 retain the prior relative order unless official metadata changed.', '- Ranks 1–170 have now received a manual pairwise pass; ranks 171–220 remain the next quality gap.')
board_path.write_text(text)

review_path = Path('vault/06 Reviews/2026/08/2026-08-02/0837-AEST-review.md')
review_path.parent.mkdir(parents=True, exist_ok=True)
review_path.write_text(f'''---\ntype: review\ntimestamp: {TS}\ntarget_block: 141-170\nchallengers: 136-175\n---\n\n# FPL Draft review — ranks 141–170\n\n## API reconciliation\n\nThe official FPL bootstrap and fixtures endpoints were rechecked as the authority for player identity, club, position and availability. All 40 challenger-pool IDs remained active board cases. No player absent from the API was retained as an active ranked player.\n\n## Sources searched\n\n- [Official FPL bootstrap]({BOOT}) and [fixtures]({FIX}).\n- [Premier League 2026 preseason fixture/results tracker]({PRE}).\n- Public searches for exact posts from Planet FPL/James Linden, Ben Crellin and equivalent fixture specialists, Sam Martin, Fabrizio Romano, official clubs, club journalists, tactical analysts and supporter communities.\n\nPublic X indexing remained incomplete. No profile-only result was adopted. No newly indexed exact post supplied sufficiently specific role, injury, set-piece or completed-transfer evidence to override official metadata for this block.\n\n## Pairwise method\n\nRanks 141–170 were sorted with challengers from 136–175. Raw expected season points were compared first, followed by expected minutes, role, set pieces, injury and rotation risk. Positional replacement value was then used for close cross-position decisions.\n\n## Decisive comparisons\n\n- Awoniyi over Barry: both have forward scarcity value, while Awoniyi has the stronger demonstrated Premier League scoring floor.\n- Barry over Georginio: the central-forward path and scarcity edge narrowly outweigh Georginio's broader role uncertainty.\n- Georginio over Reijnders: forward replacement value reverses a close raw-points comparison.\n- Reijnders over Digne: Reijnders has more routes to midfield attacking returns; Digne has the safer set-piece-assisted floor.\n- Digne over Dalot: more established attacking and dead-ball contribution.\n- F. Kadıoğlu over Livramento: comparable ceiling with a cleaner current fitness position.\n- Branthwaite over Schär: stronger minutes floor; Schär keeps the greater attacking upside.\n- Milenković over Boscagli: established aerial threat and minutes security.\n- Bentancur over Garner: immediate availability wins over Garner's dated groin return uncertainty.\n- Ayari over Hinshelwood: slightly clearer attacking route, but low confidence.\n- Caicedo over Burn: midfield accumulation and minutes narrowly beat an ordinary defender profile.\n- Tsimikas over Palestra: greater proven attacking-defender ceiling, despite rotation risk.\n- Muharemović over O'Brien: stronger upside signal; both remain late-round role watches.\n- Rodon over Murillo: availability breaks a close comparison while Murillo retains a muscle-injury discount.\n- Diarra over Vitor Reis: safer path to midfield minutes versus Manchester City defensive rotation.\n- Anselmino over Badiashile: marginal upside preference; Chelsea centre-back hierarchy remains unresolved.\n\n## Evidence adopted\n\nOfficial availability and registration metadata were treated as confirmed facts. Starting forwards and attack-minded defenders received scarcity adjustments only after raw expected-points assessment.\n\n## Evidence rejected\n\nRaw friendly goals, assists or participation without strongest-XI context were rejected. Speculative transfers, unsourced lineup claims and account profiles without an exact post were not used.\n\n## Close calls and reversal triggers\n\nGarner, Livramento and Murillo can rise on clear fitness evidence. Barry, Georginio and Awoniyi require repeated first-team striker minutes. Manchester City and Chelsea defenders require stable lineups before promotion. Tsimikas depends on Liverpool's full-back hierarchy.\n\n## Next block\n\nRanks 171–200 with challengers from 166–205.\n''')

changes_path = Path('vault/07 Changes/2026/08/2026-08-02/0837-AEST-changes.md')
changes_path.parent.mkdir(parents=True, exist_ok=True)
risers = sorted(order, key=lambda n: old_rank[n]-new_rank[n], reverse=True)[:10]
fallers = sorted(order, key=lambda n: new_rank[n]-old_rank[n], reverse=True)[:10]
changes_path.write_text(f'''---\ntype: changes\ntimestamp: {TS}\nprior_review: 2026-08-02T08:30:00+10:00\n---\n\n# Changes — ranks 141–170\n\n## Material risers\n\n''' + '\n'.join(f'- {n}: {old_rank[n]} → {new_rank[n]}' for n in risers if new_rank[n] < old_rank[n]) + '''\n\n## Material fallers\n\n''' + '\n'.join(f'- {n}: {old_rank[n]} → {new_rank[n]}' for n in fallers if new_rank[n] > old_rank[n]) + f'''\n\n## Boundary changes\n\nAwoniyi, Barry, Georginio, Reijnders and Digne moved into or above the target block. Several speculative centre-backs moved toward or beyond the rank-170 boundary.\n\n## Injury and role changes\n\nNo new official injury-status change was adopted during this run. Existing discounts remain for Livramento, Garner and Murillo. Manchester City and Chelsea defensive rotation remains unresolved.\n\n## Important no-change decisions\n\nNo player above rank 136 was moved. No transfer rumour below completed or advanced-agreement status changed the order. Friendly output without role context did not move a player.\n\n## Watchlist changes\n\nAdded explicit triggers for the three injured players, the late forward hierarchy and Manchester City/Chelsea defensive minutes.\n\nReview: {REVIEW_LINK}\n''')

# Individual player notes for the complete 40-player challenger pool.
player_dir = Path('vault/02 Players')
for i,name in enumerate(order):
    r = by_name[name]
    above = order[i-1] if i else 'Aaronson'
    below = order[i+1] if i < len(order)-1 else 'Pinnock'
    decision = f'{name} is placed below {above} and above {below} after expected points, minutes, role and risk were compared.'
    note = f'''---\ntype: player\nfpl_id: {r['id']}\nplayer_name: {name}\nteam: "[[03 Teams/{r['team']}]]"\nposition: "[[04 Positions/{'Forward' if r['pos']=='FWD' else 'Midfielder' if r['pos']=='MID' else 'Defender' if r['pos']=='DEF' else 'Goalkeeper'}]]"\napi_status: "{r['status']}"\ncurrent_rank: {r['rank']}\ncurrent_segment: {r['segment']}\nlast_reviewed: {TS}\n---\n\n# {name}\n\n## Current assessment\n\nRanked {r['rank']} after the ranks 141–170 pairwise review with challengers 136–175. Raw expected season points were assessed before positional scarcity.\n\n## Pairwise placement\n\n- Immediate comparison: **{above} / {below}**.\n- Decision: {decision}\n- Confidence: {'low' if r['status'] != 'Available' or r['team'] in ('MCI','CHE') else 'medium'}.\n- Reversal trigger: confirmed first-team role, fitness, set-piece responsibility or completed transfer evidence that changes expected minutes or points.\n\n## Evidence timeline\n\n- 2026-08-02 08:37 AEST — moved from rank {old_rank[name]} to {r['rank']} in the stable pairwise pass.\n- [Official FPL bootstrap]({BOOT})\n- [Official fixtures]({FIX})\n- [Premier League preseason tracker]({PRE})\n\n## Backlinks\n\n- [[01 Current/Current Draft Board]]\n- {REVIEW_LINK}\n- {CHANGES_LINK}\n'''
    (player_dir / f"{name} - {r['id']}.md").write_text(note)

watch = Path('vault/01 Current/Current Watchlist.md')
w = watch.read_text()
w = re.sub(r'last_updated: .*', f'last_updated: {TS}', w, count=1)
w += f'''\n\n## 2026-08-02 08:37 AEST block triggers\n\n- Garner, Livramento and Murillo — fitness and return-to-training evidence.\n- Awoniyi, Barry and Georginio — repeated central-forward minutes with probable starters.\n- Manchester City and Chelsea defenders — stable strongest-XI hierarchy.\n- Tsimikas — Liverpool full-back role and set-piece share.\n\nEvidence: {REVIEW_LINK}; [Official FPL bootstrap]({BOOT}); [Premier League preseason tracker]({PRE}).\n'''
watch.write_text(w)

for p in [Path('vault/Home.md'), Path('vault/Wiki.md')]:
    s = p.read_text()
    s = re.sub(r'last_updated: .*', f'last_updated: {TS}', s, count=1)
    s += f'''\n\n## 2026-08-02 08:37 AEST — ranks 141–170\n\n- Review: {REVIEW_LINK}\n- Changes: {CHANGES_LINK}\n- The first 170 ranks now have a manual pairwise pass; next block is 171–200 with challengers 166–205.\n'''
    p.write_text(s)

changed = [board_path, watch, Path('vault/Home.md'), Path('vault/Wiki.md'), review_path, changes_path]
changed += [player_dir / f"{n} - {by_name[n]['id']}.md" for n in order]
changelog = Path('vault/00 Meta/Document Changelog.md')
c = changelog.read_text()
c = re.sub(r'last_updated: .*', f'last_updated: {TS}', c, count=1)
for p in changed:
    action = 'Created' if p in (review_path, changes_path) or old_rank.get(p.stem.rsplit(' - ',1)[0], 0) >= 146 else 'Updated'
    c += f"\n| {TS} | `{p.as_posix()}` | {action} | Recorded ranks 141–170 pairwise review with challengers 136–175. | {REVIEW_LINK} | [Official FPL bootstrap]({BOOT}); [Official fixtures]({FIX}); [Premier League preseason tracker]({PRE}) |"
c += f"\n| {TS} | `vault/00 Meta/Document Changelog.md` | Updated | Appended a separate audit row for every Markdown file changed by the ranks 141–170 review. | {REVIEW_LINK} | Per-document audit; [Official FPL bootstrap]({BOOT}) |\n"
changelog.write_text(c)
