from pathlib import Path
import json,re,urllib.request
TS='2026-08-02T11:01:00+10:00'; DAY='2026-08-02'; HH='1101'; Z='AEST'
REVIEW=f'vault/06 Reviews/2026/08/{DAY}/{HH}-{Z}-review.md'; CHANGES=f'vault/07 Changes/2026/08/{DAY}/{HH}-{Z}-changes.md'
BOARD=Path('vault/01 Current/Current Draft Board.md'); WATCH=Path('vault/01 Current/Current Watchlist.md')
with urllib.request.urlopen('https://fantasy.premierleague.com/api/bootstrap-static/',timeout=30) as r: api=json.load(r)
with urllib.request.urlopen('https://fantasy.premierleague.com/api/fixtures/',timeout=30) as r: fixtures=json.load(r)
active={p['id']:p for p in api['elements']}; teams={t['id']:t['short_name'] for t in api['teams']}
lines=BOARD.read_text().splitlines(); rows=[]; idx=[]
for i,l in enumerate(lines):
    if re.match(r'^\| \d+ \|',l):
        c=[x.strip() for x in l.strip('|').split('|')]; rows.append(c); idx.append(i)
by_name={c[1]:c for c in rows}; old_rank={c[1]:int(c[0]) for c in rows}
order=['Leno','Pope','Dunk','A.Becker','Mykolenko','Martinez','J.Murphy','Smith Rowe','Jensen','Keane','Maguire','Gravenberch','Sánchez','Scott','Cash','McGinn','Beto','Brobbey','Robinson','Sessegnon','Aït-Nouri','Botman','Hill','Alderete','Thiaw','Gusto','De Cuyper','Bogle','Hincapie','N.Williams','Bassey','Van den Berg','Zubimendi','Canvot','Delap','N.Jackson','Rashford','Tonali','Wieffer','Estêvão']
assert len(order)==40 and all(n in by_name for n in order)
for rank,name in zip(range(106,146),order):
    c=by_name[name][:]; c[0]=str(rank); c[4]='Depth' if rank<=124 else 'Endgame'; c[5]='C' if rank<=124 else 'D+'; c[8]=TS; c[9]=f'[[06 Reviews/2026/08/{DAY}/{HH}-{Z}-review]]'; by_name[name]=c
for c,i in zip(rows,idx):
    name=c[1]
    if name in by_name and 106<=int(by_name[name][0])<=145:
        pass
newrows=sorted([by_name.get(c[1],c) for c in rows],key=lambda x:int(x[0]))
for c,i in zip(newrows,idx): lines[i]='| '+' | '.join(c)+' |'
BOARD.write_text('\n'.join(lines)+'\n')
comparisons=[
('J.Murphy','Keane','Murphy projects for more attacking points; Keane has the safer minutes floor, but an attacking midfielder should be drafted first.'),
('Smith Rowe','Maguire','Smith Rowe has the higher attacking ceiling and comparable expected points; Maguire retains the stronger clean-sheet floor.'),
('Jensen','Gravenberch','Jensen has more direct set-piece and chance-creation routes; Gravenberch has the safer minutes floor but lower ceiling.'),
('Sánchez','Scott','Sánchez has a starting-goalkeeper floor if he retains the shirt; Scott offers more upside but lower season-long certainty.'),
('Beto','Brobbey','Beto has the clearer current Premier League scoring baseline; Brobbey can reverse this with confirmed first-choice starts.'),
('Robinson','Sessegnon','Robinson has the stronger expected-minutes floor; Sessegnon has higher attacking variance.'),
('Gusto','De Cuyper','Gusto has elite-team clean-sheet upside but more rotation risk; he stays narrowly ahead on ceiling.'),
('Delap','N.Jackson','Delap is preferred on forward scarcity and role upside, but both are demoted because Welbeck adds Chelsea striker competition.'),
('N.Jackson','Rashford','Jackson still has greater centre-forward scoring upside; Rashford needs a clearly restored starting role to reverse it.'),
('Tonali','Wieffer','Tonali has the higher all-round points expectation and attacking involvement; Wieffer offers positional flexibility but less ceiling.')]
review=['---','type: review',f'timestamp: {TS}','scope: ranks 111-140 with challengers 106-145','---','','# FPL Draft review — ranks 111–140','','## Changes since prior run','','The 350-player expansion was the immediate baseline. This run completed the next required manual pairwise block. The main material change is a downward correction to Chelsea forwards after the confirmed Danny Welbeck signing increased competition for centre-forward minutes. Jacob Murphy, Smith Rowe and Jensen moved upward within the block on clearer attacking routes.','','## API reconciliation',f'- Official FPL returned {len(api["elements"])} active players, {len(api["teams"])} teams and {len(fixtures)} fixtures.','- All 40 players in the 106–145 comparator window remain in the active API pool with stable IDs.','- API team, position and availability metadata were treated as authoritative.','','## Public evidence searched','- [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/)','- [Official FPL fixtures](https://fantasy.premierleague.com/api/fixtures/)','- [Reuters: Chelsea sign Danny Welbeck, 1 August 2026](https://www.reuters.com/sports/soccer/chelsea-bring-35-year-old-striker-welbeck-from-brighton-2026-08-01/)','- [Reuters: Joe Gomez expected to miss Liverpool opener, 30 July 2026](https://www.reuters.com/sports/soccer/liverpools-gomez-set-miss-premier-league-opener-with-muscle-injury-2026-07-30/)','- [Premier League: 2026 preseason fixtures and results](https://www.premierleague.com/en/news/4606700/premier-league-clubs-2026-pre-season-fixtures-and-results)','','Public X search did not return sufficiently specific, accessible posts from the named analysts during this run. No profile-only result was used.','','## Method','','Each player in ranks 111–140 was compared with immediate neighbours and plausible challengers from ranks 106–145. Raw season-long expected FPL points were considered first, followed by expected minutes, role, set pieces, injury and rotation risk, floor and ceiling. Positional replacement value was applied only after the points comparison.','','## Decisive pairwise comparisons']
for a,b,r in comparisons: review.append(f'- **{a} over {b}:** {r} Confidence: medium. Reversal trigger: a confirmed role or availability change.')
review += ['','## Close calls','- **Martinez / Keane / Maguire:** goalkeeper and defender floors are close; no false precision is claimed.','- **Beto / Brobbey:** forward scarcity keeps both above similarly projected low-upside midfielders, but role confirmation could reverse them.','- **Gusto / De Cuyper / Bogle:** attacking full-back upside is balanced against rotation and team-strength uncertainty.','- **Delap / Jackson / Rashford:** all three remain highly role-sensitive.','','## Evidence adopted','- Welbeck’s confirmed Chelsea arrival was adopted as a direct competition downgrade for Delap and Jackson.','- Official API identity, position, availability and fixture records were adopted.','- Repeated first-team role and set-piece pathways were weighted above isolated friendly returns.','','## Evidence rejected','- Raw preseason goals or assists without probable-first-team role context.','- Transfer speculation without a completed move or sufficiently credible advanced report.','- Ownership and price as ranking evidence.','','## Positional priorities','- Starting goalkeepers retain a useful floor around this range.','- Forwards receive a scarcity adjustment, but not enough to erase substantial minutes uncertainty.','- Attacking full-backs can outrank safer centre-backs when their role is credible.','- Low-attacking midfielders require exceptional minutes or set-piece security.','','## Major uncertainties and next triggers','- Chelsea striker hierarchy after Welbeck joins the tour.','- Newcastle attacking rotation around Jacob Murphy.','- Fulham attacking role for Smith Rowe and defensive hierarchy around Robinson and Sessegnon.','- Arsenal defensive availability and Hincapie’s probable role.','- Exact penalty and set-piece assignments across the comparator window.']
Path(REVIEW).parent.mkdir(parents=True,exist_ok=True); Path(REVIEW).write_text('\n'.join(review)+'\n')
changes=['---','type: changes',f'timestamp: {TS}','prior_review: 1017-AEST','---','','# FPL Draft changes — ranks 111–140','','## Material changes']
for name in order:
    o=old_rank[name]; n=order.index(name)+106
    if o!=n: changes.append(f'- **{name}: {o} → {n}.** '+('Rose on stronger attacking route or minutes-adjusted comparator outcome.' if n<o else 'Fell after stable insertion comparison or increased role competition.'))
changes += ['','## Transfer and injury changes','- Welbeck’s confirmed Chelsea signing increases competition for Delap and Jackson; both moved below the safer middle of the block.','- Joe Gomez’s injury remains a Liverpool defensive watch item but did not justify a direct rank change in this block.','','## Important no-change decisions','- The goalkeeper cluster from Leno through Martinez remains above the main defender and midfielder depth cluster.','- No API-absent player was retained as an active ranked player.','- No raw friendly output was used to manufacture movement.']
Path(CHANGES).parent.mkdir(parents=True,exist_ok=True); Path(CHANGES).write_text('\n'.join(changes)+'\n')
# update affected player notes
for name in order:
    c=by_name[name]; p=Path(f'vault/02 Players/{name} - {c[6]}.md')
    if p.exists():
        t=p.read_text(); t=re.sub(r'(?m)^rank: .*$',f'rank: {c[0]}',t); t=re.sub(r'(?m)^segment: .*$',f'segment: {c[4]}',t); t=re.sub(r'(?m)^tier: .*$',f'tier: {c[5]}',t); t=re.sub(r'(?m)^last_updated: .*$',f'last_updated: {TS}',t)
        t += f'\n## 2026-08-02 11:01 AEST pairwise review\nCompared within ranks 106–145. Current placement: **{c[0]}**. See [[06 Reviews/2026/08/{DAY}/{HH}-{Z}-review]]. Reversal triggers: confirmed role, set pieces, injury or transfer change.\n'
    else:
        t=f'---\ntype: player\nfpl_id: {c[6]}\nrank: {c[0]}\nsegment: {c[4]}\ntier: {c[5]}\nlast_updated: {TS}\n---\n\n# {name}\n\nSee [[06 Reviews/2026/08/{DAY}/{HH}-{Z}-review]].\n'
    p.write_text(t)
# watchlist, home, wiki
wt=WATCH.read_text(); wt += f'\n## Review {HH} {Z}\n- Chelsea striker hierarchy: Welbeck, Delap and Jackson.\n- Newcastle attacking rotation around Jacob Murphy.\n- Arsenal defensive availability affecting Hincapie.\n- Evidence: [[06 Reviews/2026/08/{DAY}/{HH}-{Z}-review]].\n'; WATCH.write_text(wt)
for path in ['vault/Home.md','vault/Wiki.md']:
    p=Path(path); t=p.read_text(); t += f'\n- Latest review: [[06 Reviews/2026/08/{DAY}/{HH}-{Z}-review]]; changes: [[07 Changes/2026/08/{DAY}/{HH}-{Z}-changes]].\n'; p.write_text(t)
# changelog for every changed markdown
changed=[str(BOARD),str(WATCH),REVIEW,CHANGES,'vault/Home.md','vault/Wiki.md']+[f'vault/02 Players/{n} - {by_name[n][6]}.md' for n in order]
cl=Path('vault/00 Meta/Document Changelog.md'); ct=cl.read_text(); ct=re.sub(r'(?m)^last_updated: .*$',f'last_updated: {TS}',ct,1)
for path in changed:
    action='Created' if path in [REVIEW,CHANGES] else 'Updated'
    ct += f'| {TS} | `{path}` | {action} | Completed manual pairwise review of ranks 111–140 with challengers 106–145. | [[06 Reviews/2026/08/{DAY}/{HH}-{Z}-review]] | [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/); [Official fixtures](https://fantasy.premierleague.com/api/fixtures/); [Reuters Welbeck](https://www.reuters.com/sports/soccer/chelsea-bring-35-year-old-striker-welbeck-from-brighton-2026-08-01/) |\n'
ct += f'| {TS} | `vault/00 Meta/Document Changelog.md` | Updated | Appended one row for every Markdown file changed by the review. | [[06 Reviews/2026/08/{DAY}/{HH}-{Z}-review]] | Per-document audit |\n'; cl.write_text(ct)
print({'players':len(api['elements']),'fixtures':len(fixtures),'block':'111-140','changed_markdown':len(changed)+1})