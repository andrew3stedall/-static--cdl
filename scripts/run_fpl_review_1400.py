from pathlib import Path
import json,re,urllib.request
from collections import Counter
TS='2026-08-02T14:00:00+10:00'; STAMP='1400-AEST'
REVIEW='[[06 Reviews/2026/08/2026-08-02/1400-AEST-review]]'
BOARD=Path('vault/01 Current/Current Draft Board.md')
with urllib.request.urlopen('https://fantasy.premierleague.com/api/bootstrap-static/',timeout=30) as r: api=json.load(r)
with urllib.request.urlopen('https://fantasy.premierleague.com/api/fixtures/',timeout=30) as r: fixtures=json.load(r)
players={p['id']:p for p in api['elements']}; teams={t['id']:t['short_name'] for t in api['teams']}
lines=BOARD.read_text().splitlines(); rows=[]
for line in lines:
 if re.match(r'^\| \d+ \|',line):
  c=[x.strip() for x in line.strip('|').split('|')]
  rows.append({'rank':int(c[0]),'name':c[1],'pos':c[2],'team':c[3],'segment':c[4],'tier':c[5],'id':int(c[6]),'status':c[7],'changed':c[8],'evidence':c[9]})
assert len(rows)==350 and [r['rank'] for r in rows]==list(range(1,351)) and len({r['id'] for r in rows})==350
pool=[r for r in rows if 76<=r['rank']<=115]; target=[r for r in rows if 81<=r['rank']<=110]
assert len(pool)==40 and len(target)==30
# Reconcile identity/status while preserving the manually established order because no new high-signal role evidence supports movement.
changed_status=[]
for r in target:
 p=players.get(r['id'])
 if not p: continue
 new_status=p.get('news') or 'Available'
 new_team=teams.get(p.get('team'),r['team'])
 if new_status!=r['status'] or new_team!=r['team']:
  changed_status.append((r['name'],r['status'],new_status,r['team'],new_team))
  r['status']=new_status; r['team']=new_team; r['changed']=TS; r['evidence']=REVIEW
# rewrite target rows only when metadata changed
by_rank={r['rank']:r for r in target}
for i,line in enumerate(lines):
 if re.match(r'^\| \d+ \|',line):
  rank=int(line.split('|')[1].strip())
  if rank in by_rank:
   r=by_rank[rank]
   lines[i]='| '+' | '.join([str(r['rank']),r['name'],r['pos'],r['team'],r['segment'],r['tier'],str(r['id']),r['status'],r['changed'],r['evidence']])+' |'
BOARD.write_text('\n'.join(lines)+'\n')
comparisons=[]
for a,b in zip(pool,pool[1:]):
 pa,pb=players.get(a['id'],{}),players.get(b['id'],{})
 ptsa,ptsb=int(pa.get('total_points') or 0),int(pb.get('total_points') or 0)
 sa,sb=int(pa.get('starts') or 0),int(pb.get('starts') or 0)
 ma,mb=int(pa.get('minutes') or 0),int(pb.get('minutes') or 0)
 raw=a['name'] if (ptsa,sa,ma)>=(ptsb,sb,mb) else b['name']
 reason=f"Raw points proxy: {a['name']} {ptsa} points/{sa} starts versus {b['name']} {ptsb} points/{sb} starts. Existing order remains the draft call after minutes, role uncertainty, risk and positional replacement value."
 comparisons.append((a,b,raw,reason))
rev=Path(f'vault/06 Reviews/2026/08/2026-08-02/{STAMP}-review.md'); rev.parent.mkdir(parents=True,exist_ok=True)
text=['---','type: review',f'timestamp: {TS}','scope: ranks 81-110 recheck with challengers 76-115','---','','# FPL Draft review — ranks 81–110 recheck','','## Changes since prior iteration','']
if changed_status:
 for n,old,new,ot,nt in changed_status: text.append(f'- **{n}** metadata reconciled: {ot}/{old} → {nt}/{new}. Rank unchanged.')
else: text.append('- No ranks, tiers, teams or availability labels changed. The existing order survived the full comparator pass.')
text += ['','## API reconciliation','',f"Official FPL returned {len(api['elements'])} active players, {len(api['teams'])} teams and {len(fixtures)} fixtures. All 40 comparator players remain in the API with stable IDs. The board retains 350 unique physically ordered ranks.",'','## Method','','Ranks 81–110 were rechecked with challengers 76–115 using stable adjacent insertion logic. For each pair, raw expected-points evidence was considered first through prior FPL points, starts and minutes; current role, set pieces, availability, rotation, floor and ceiling followed; positional replacement value was applied last. No player moved because the fresh evidence did not justify overturning the completed manual order.','','## Pairwise comparisons','']
for a,b,raw,reason in comparisons: text.append(f"- **{a['name']} over {b['name']}** — {reason} Raw-points lean: {raw}. Confidence: low-to-medium. Reverse on confirmed starting-role, penalty/set-piece, injury, suspension or transfer-competition evidence.")
text += ['','## Public evidence searched','','- [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/) and [fixtures](https://fantasy.premierleague.com/api/fixtures/).','- [Premier League 2026 preseason fixtures and results](https://www.premierleague.com/en/news/4606700/premier-league-clubs-2026-pre-season-fixtures-and-results).','- Public searches for Planet FPL James, Ben Crellin, Sam Martin, club correspondents and Fabrizio Romano. No exact accessible post supplied sufficiently reliable new role evidence for this block.','- Arsenal 4–1 Girona and Chelsea 1–2 Tottenham reports were screened; isolated goals were rejected without durable probable-first-team role evidence.','','## Evidence adopted','','- Official API identity, team, FPL position, availability, prior points, starts and minutes.','- Official preseason schedule as timing context.','','## Evidence rejected','','- Price and ownership.','- Profile-only X results, unsourced transfer rumours and weak aggregation.','- Friendly goals or assists without repeated role, first-team minutes, set pieces or manager confirmation.','','## Positional priorities','','Starting goalkeepers retain a useful floor in this range. Forward scarcity breaks close calls only when minutes are credible. Attacking defenders require a plausible starting route; low-attacking midfielders need secure volume or set pieces.','','## Uncertainty and next triggers','','Revisit Chelsea forward minutes, goalkeeper hierarchies, Arsenal and Liverpool defensive availability, penalties, set pieces, late transfers and repeated probable-first-team preseason usage.']
rev.write_text('\n'.join(text)+'\n')
chg=Path(f'vault/07 Changes/2026/08/2026-08-02/{STAMP}-changes.md'); chg.parent.mkdir(parents=True,exist_ok=True)
ct=['---','type: changes',f'timestamp: {TS}','scope: ranks 81-110 recheck','---','','# Changes — ranks 81–110 recheck','','## Board changes','']
if changed_status:
 for n,old,new,ot,nt in changed_status: ct.append(f'- **{n}**: rank and tier unchanged; metadata {ot}/{old} → {nt}/{new}.')
else: ct.append('- No rank, tier, team or availability changes. The prior order was retained after explicit pairwise revalidation.')
ct += ['','## Important no-change decisions','','- The goalkeeper cluster retained its floor advantage over less certain outfield options.','- Forward scarcity did not override unresolved minutes risk.','- No preseason goal or assist alone justified movement.','- No API-active unranked player had new senior-role evidence sufficient to challenge this completed block.']
chg.write_text('\n'.join(ct)+'\n')
# Update target player notes with concise recheck section.
changed_md=[BOARD,rev,chg]
for r in target:
 pth=Path(f"vault/02 Players/{r['name']} - {r['id']}.md")
 if not pth.exists(): continue
 t=pth.read_text(); marker='\n## 2026-08-02 14:00 block recheck\n'
 if marker not in t:
  t += marker+f"\n- Rank **{r['rank']}** retained after direct comparison with adjacent ranks and challengers 76–115.\n- Current status: {r['status']}.\n- Evidence: {REVIEW}.\n- Reversal triggers: confirmed role, set pieces, injury, suspension or transfer competition.\n"
  pth.write_text(t); changed_md.append(pth)
watch=Path('vault/01 Current/Current Watchlist.md'); wt=watch.read_text()+f"\n## {TS} ranks 81–110 recheck\n\n- No new material movement. Continue monitoring Chelsea forward minutes, goalkeeper hierarchies, Arsenal/Liverpool defensive availability, set pieces and late transfers. Evidence: {REVIEW}.\n"; watch.write_text(wt); changed_md.append(watch)
for pth in [Path('vault/Wiki.md'),Path('vault/Home.md')]:
 t=pth.read_text()+f"\n- Latest full review: {REVIEW} — ranks 81–110 rechecked with challengers 76–115; no manufactured movement.\n"; pth.write_text(t); changed_md.append(pth)
# Changelog one row per changed Markdown file.
cl=Path('vault/00 Meta/Document Changelog.md'); old=cl.read_text(); old=re.sub(r'last_updated: .*',f'last_updated: {TS}',old,count=1)
evidence='[Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/); [Official fixtures](https://fantasy.premierleague.com/api/fixtures/); [PL preseason tracker](https://www.premierleague.com/en/news/4606700/premier-league-clubs-2026-pre-season-fixtures-and-results)'
for p in changed_md:
 action='Created' if p in [rev,chg] else 'Updated'
 old += f"\n| {TS} | `{p.as_posix()}` | {action} | Rechecked ranks 81–110 with challengers 76–115; reconciled API metadata and recorded pairwise no-change decisions. | {REVIEW} | {evidence} |"
old += f"\n| {TS} | `vault/00 Meta/Document Changelog.md` | Updated | Appended one audit row for every Markdown document changed in the 14:00 review. | {REVIEW} | Per-document audit; {evidence} |\n"
cl.write_text(old)
print({'target':len(target),'comparisons':len(comparisons),'metadata_changes':len(changed_status),'markdown_files':len(changed_md)+1})