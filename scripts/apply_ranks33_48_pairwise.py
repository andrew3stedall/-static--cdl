from pathlib import Path
import re

TS='2026-08-01T22:54:00+10:00'
STAMP='2254-AEST'
BRANCH='codex/fpl-review-20260801-2254-ranks33-48'
REVIEW='[[06 Reviews/2026/08/2026-08-01/2254-AEST-review]]'
CHANGES='[[07 Changes/2026/08/2026-08-01/2254-AEST-changes]]'
board_path=Path('vault/01 Current/Current Draft Board.md')
text=board_path.read_text()
lines=text.splitlines()
rows=[]
for i,l in enumerate(lines):
    m=re.match(r'\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|',l)
    if m:
        rows.append((i,int(m.group(1)),[x.strip() for x in m.groups()[1:]]))
by_name={r[2][0]:r for r in rows}
order=['Dewsbury-Hall','Solanke','Richarlison','Cherki','Marmoush','Ndiaye','Schade','Gvardiol','Guéhi','Doku','E.Le Fée','Enzo','Tarkowski','Fernandes','Senesi','Van Hecke','Anderson',"O'Reilly",'Stach','Ampadu']
assert all(n in by_name for n in order), [n for n in order if n not in by_name]
for rank,name in enumerate(order,33):
    idx,old,data=by_name[name]
    player,pos,team,segment,tier,fpl_id,status=data
    segment='Core'
    tier='B' if rank<=48 else 'B-'
    lines[idx]=f'| {rank} | {player} | {pos} | {team} | {segment} | {tier} | {fpl_id} | {status} | {TS} | {REVIEW} |'
lines[0:0]=[]
text='\n'.join(lines)+'\n'
text=re.sub(r'last_updated: .*',f'last_updated: {TS}',text,count=1)
text=re.sub(r'status: .*', 'status: ranks33_48_pairwise_sorted', text, count=1)
text=text.replace('The first 32 have now been stable-sorted in two explicit player-versus-player blocks.','The first 48 have now been stable-sorted in three explicit player-versus-player blocks.')
board_path.write_text(text)

players={
'Dewsbury-Hall':('236','Everton advanced-role potential and probable secure minutes keep him above the more volatile attackers.','Solanke','Dewsbury-Hall has the safer season-long minutes floor; Solanke has the higher forward scarcity upside.','medium','Solanke becomes a nailed, fit penalty-taking starter or Dewsbury-Hall loses the advanced role.'),
'Solanke':('526','Forward scarcity and a plausible central Tottenham role justify the largest promotion in this block.','Richarlison','Solanke is preferred on the cleaner long-term centre-forward profile.','medium-low','Richarlison is clearly first choice or Solanke lacks preseason starts.'),
'Richarlison':('527','A starting Tottenham striker would have strong draft value, but fitness and competition cap confidence.','Cherki','Richarlison wins the close draft comparison through forward scarcity.','low-medium','Cherki secures regular central starts or Richarlison is not first choice.'),
'Cherki':('399','Elite creative upside earns a rise, but Manchester City rotation prevents a top-32 placement.','Marmoush','Cherki has the broader assist and bonus routes when starting.','medium-low','Marmoush establishes a regular central-forward role.'),
'Marmoush':('401','Forward classification and Manchester City goal upside are valuable, offset by major rotation risk.','Ndiaye','Marmoush is drafted first because comparable points upside plus forward scarcity wins the tie.','low-medium','Ndiaye retains penalties and Marmoush is mostly a substitute.'),
'Ndiaye':('237','Secure attacking minutes and possible penalties provide a strong floor in this range.','Schade','Ndiaye has the safer role and set-piece routes.','medium','Schade becomes Brentford’s undisputed high-minute second scorer.'),
'Schade':('94','Direct goal threat and Brentford minutes support a rise into the block.','Gvardiol','Schade is expected to outscore the defender through attacking returns.','medium','His starting place weakens or Gvardiol secures an advanced, rotation-proof role.'),
'Gvardiol':('391','Elite-team clean sheets and attacking upside remain useful, but City defender rotation is material.','Guéhi','Gvardiol has the higher ceiling; Guéhi has the safer minutes.','low-medium','Guéhi is fully nailed while Gvardiol rotates heavily.'),
'Guéhi':('388','Likely strong clean-sheet environment and centre-back security keep him draftable, though attacking upside is limited.','Doku','Guéhi wins on minutes floor and season reliability.','medium-low','Doku becomes a regular starter.'),
'Doku':('400','Explosive points-per-start upside is discounted heavily for minutes volatility.','E.Le Fée','Doku’s ceiling narrowly beats Le Fée’s safer role.','low','Doku remains a bench option or Le Fée gains penalties.'),
'E.Le Fée':('542','Creative responsibility and secure Sunderland minutes provide a stable mid-round profile.','Enzo','Le Fée has the clearer attacking responsibility.','medium','Enzo is consistently deployed as Chelsea’s advanced midfielder.'),
'Enzo':('155','Chelsea team strength helps, but role and attacking-minute uncertainty keep him in the lower half.','Tarkowski','Enzo has the higher attacking ceiling; Tarkowski the safer floor.','low-medium','Enzo plays deep or Tarkowski retains exceptional defensive-contribution scoring.'),
'Tarkowski':('229','Nailed minutes and multiple defensive scoring routes offer floor, but defender replacement is deep.','Fernandes','Tarkowski’s role certainty narrowly wins.','medium','Fernandes secures an advanced Tottenham role.'),
'Fernandes':('525','Tottenham attacking upside exists, but exact role and minutes remain unclear.','Senesi','Fernandes has the higher attacking ceiling.','low','He is used deeper or is not first choice.'),
'Senesi':('498','Set-piece threat and probable starts retain value, although team and role changes require caution.','Van Hecke','Senesi has slightly greater attacking upside.','low-medium','Van Hecke proves more secure in a stronger defence.'),
'Van Hecke':('112','Minutes security and defensive-contribution routes earn the final place in the block.','Anderson','Van Hecke wins on role certainty and reliable defensive scoring.','medium','Anderson secures a regular advanced Manchester City role.'),
'Anderson':('481','Manchester City upside is outweighed by unresolved role and rotation risk.','Van Hecke','Falls outside the block because minutes uncertainty overwhelms team strength.','low','Regular advanced starts are demonstrated.'),
"O'Reilly":('387','Versatility and team quality are useful, but Manchester City rotation makes the current rank fragile.','Anderson','Placed below Anderson because both are uncertain and the defender pool is more replaceable.','low','A first-choice advanced full-back role is established.'),
'Stach':('335','Leeds minutes may be secure, but direct attacking routes appear weaker than the players above.','O\'Reilly','Stach has the safer floor but insufficient ceiling to enter the block.','medium-low','Set pieces or an advanced role are confirmed.'),
'Ampadu':('338','Strong minutes floor but limited attacking ceiling leaves him outside the top 48.','Stach','Stach is preferred for slightly stronger attacking routes.','medium','Ampadu gains set pieces or a more advanced role.')}
team_links={'236':'EVE','526':'TOT','527':'TOT','399':'MCI','401':'MCI','237':'EVE','94':'BRE','391':'MCI','388':'MCI','400':'MCI','542':'SUN','155':'CHE','229':'EVE','525':'TOT','498':'TOT','112':'TOT','481':'MCI','387':'MCI','335':'LEE','338':'LEE'}
pos_map={n:by_name[n][2][1] for n in order}
name_file={n:n for n in order}
for rank,name in enumerate(order,33):
    fid,assessment,comp,decision,confidence,trigger=players[name]
    path=Path(f'vault/02 Players/{name} - {fid}.md')
    pos=pos_map[name]
    position={'MID':'Midfielder','FWD':'Forward','DEF':'Defender','GKP':'Goalkeeper'}[pos]
    content=f'''---\ntype: player\nfpl_id: {fid}\nplayer_name: {name}\nteam: "[[03 Teams/{team_links[fid]}]]"\nposition: "[[04 Positions/{position}]]"\napi_status: available\ncurrent_rank: {rank}\ncurrent_segment: Core\nlast_reviewed: {TS}\n---\n\n# {name}\n\n## Current assessment\n\n{assessment}\n\n## Pairwise placement\n\n- Compared with: **{comp}**.\n- Decision: {decision}\n- Confidence: {confidence}.\n- Reversal trigger: {trigger}\n\n## Evidence timeline\n\n- 2026-08-01 22:54 AEST — Pairwise-sorted to rank {rank} in the ranks 33–48 review.\n- [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/)\n- [Official fixtures](https://fantasy.premierleague.com/api/fixtures/)\n- [PL key-player analysis](https://www.premierleague.com/en/news/4680821/the-scouts-analysis-of-15-key-player-prices-in-202627-fantasy)\n- [PL FDR](https://www.premierleague.com/en/news/4675493/get-the-fixture-difficulty-ratings-for-202627-fpl-season)\n- [FFScout preseason report](https://www.fantasyfootballscout.co.uk/2026/07/31/fpl-pre-season-tavernier-impresses-muharemovic-class-szoboszlai-deeper)\n\n## Backlinks\n\n- [[01 Current/Current Draft Board]]\n- {REVIEW}\n- {CHANGES}\n'''
    path.parent.mkdir(parents=True,exist_ok=True); path.write_text(content)

review=Path('vault/06 Reviews/2026/08/2026-08-01/2254-AEST-review.md'); review.parent.mkdir(parents=True,exist_ok=True)
review.write_text(f'''---\ntype: review\nreviewed_at: {TS}\nbaseline: "[[06 Reviews/2026/08/2026-08-01/2243-AEST-review]]"\nbranch: {BRANCH}\nstatus: ranks33_48_pairwise_complete\n---\n\n# Ranks 33–48 pairwise sorting review\n\n## Changes since the prior iteration\n\nSolanke rose from 52 to 34, Cherki 43 to 36, Marmoush 45 to 37, Ndiaye 48 to 38 and Schade 49 to 39. Anderson, O'Reilly, Stach and Ampadu were displaced below rank 48. Dewsbury-Hall retained rank 33 after comparison with Solanke.\n\n## Method\n\nStable insertion-style comparison was applied to prior ranks 29–52. Raw expected season points came first, followed by minutes, role, set pieces, injury and rotation risk, floor and ceiling. Positional replacement value was used only for close cross-position decisions.\n\n## Pairwise decisions\n\n| Rank | Player | Compared with | Decision | Confidence |\n|---:|---|---|---|---|\n'''+''.join(f'| {r} | {n} | {players[n][2]} | {players[n][3]} | {players[n][4]} |\n' for r,n in enumerate(order,33))+'''\n## Evidence adopted\n\n- Solanke and Richarlison received forward-scarcity adjustments, but both remain role-sensitive.\n- Cherki, Marmoush and Doku retain elite-team upside with substantial rotation discounts.\n- Ndiaye and Schade rise on clearer expected minutes and direct attacking roles.\n- Gvardiol and Guéhi remain the leading defenders in the block, but deep defender replacement prevents aggressive promotion.\n- Anderson and O'Reilly fall outside the block because team strength does not overcome unresolved minutes.\n\nSources: [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/); [Official fixtures](https://fantasy.premierleague.com/api/fixtures/); [PL key-player analysis](https://www.premierleague.com/en/news/4680821/the-scouts-analysis-of-15-key-player-prices-in-202627-fantasy); [PL FDR](https://www.premierleague.com/en/news/4675493/get-the-fixture-difficulty-ratings-for-202627-fpl-season); [FFScout preseason report](https://www.fantasyfootballscout.co.uk/2026/07/31/fpl-pre-season-tavernier-impresses-muharemovic-class-szoboszlai-deeper).\n\n## Evidence rejected or limited\n\n- Team strength alone was not accepted as proof of minutes.\n- Friendly output without first-team role context was not used to force movement.\n- No player was moved on an inaccessible or unspecific X profile claim.\n- Exact penalty ownership for Tottenham, Everton and promoted teams remains uncertain.\n\n## Uncertainties and reversal triggers\n\nTottenham striker hierarchy, Manchester City attacking rotation, Everton set pieces, Chelsea midfield deployment and the exact roles of Anderson and O'Reilly can materially reorder this block.\n\n## Next block\n\nSort ranks 49–64 with challengers from ranks 45–68.\n''')
changes=Path('vault/07 Changes/2026/08/2026-08-01/2254-AEST-changes.md'); changes.parent.mkdir(parents=True,exist_ok=True)
changes.write_text(f'''---\ntype: changes\nchanged_at: {TS}\nbaseline: "[[07 Changes/2026/08/2026-08-01/2243-AEST-changes]]"\nreview: "{REVIEW}"\n---\n\n# Changes — ranks 33–48 pairwise review\n\n| Player | Old | New | Change |\n|---|---:|---:|---:|\n'''+''.join(f'| {n} | {by_name[n][1]} | {r} | {r-by_name[n][1]:+d} |\n' for r,n in enumerate(order,33))+'''\n## Entrants to ranks 33–48\n\nSolanke, Cherki, Marmoush, Ndiaye and Schade entered or materially improved within the block.\n\n## Displaced below 48\n\nAnderson, O'Reilly, Stach and Ampadu moved below the block after direct comparison.\n\n## No-change decisions\n\nDewsbury-Hall retained rank 33. No official API identity, team, position or availability changes were found for the assessed pool.\n''')

for p in [Path('vault/Home.md'),Path('vault/Wiki.md')]:
    s=p.read_text(); s=re.sub(r'latest_review: .*',f'latest_review: "{REVIEW}"',s,count=1) if 'latest_review:' in s else s
    s=re.sub(r'latest_changes: .*',f'latest_changes: "{CHANGES}"',s,count=1) if 'latest_changes:' in s else s
    s += f'\n## 2026-08-01 22:54 AEST — ranks 33–48\n\n- Review: {REVIEW}\n- Changes: {CHANGES}\n- Solanke, Cherki, Marmoush, Ndiaye and Schade rose; Anderson, O\'Reilly, Stach and Ampadu fell below 48.\n'
    p.write_text(s)
watch=Path('vault/01 Current/Current Watchlist.md'); ws=watch.read_text(); ws += f'''\n## 2026-08-01 22:54 AEST block triggers\n\n- Tottenham striker hierarchy: Solanke versus Richarlison.\n- Manchester City attacking starts: Cherki, Marmoush, Doku, Anderson and O'Reilly.\n- Everton advanced roles and set pieces: Dewsbury-Hall and Ndiaye.\n- Chelsea midfield deployment: Enzo.\n\nEvidence: {REVIEW}; [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/).\n'''; watch.write_text(ws)

changed=[board_path,watch,Path('vault/Home.md'),Path('vault/Wiki.md'),review,changes]+[Path(f'vault/02 Players/{n} - {players[n][0]}.md') for n in order]
cl=Path('vault/00 Meta/Document Changelog.md'); cs=cl.read_text(); cs=re.sub(r'last_updated: .*',f'last_updated: {TS}',cs,count=1); cs+='\n'
for p in changed:
    action='Created' if p in [review,changes] or ('vault/02 Players/' in str(p) and not False) else 'Updated'
    cs+=f'| {TS} | `{p}` | {action} | Recorded ranks 33–48 pairwise review evidence and placement. | {REVIEW} | [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/); [Official fixtures](https://fantasy.premierleague.com/api/fixtures/); [PL FDR](https://www.premierleague.com/en/news/4675493/get-the-fixture-difficulty-ratings-for-202627-fpl-season) |\n'
cs+=f'| {TS} | `vault/00 Meta/Document Changelog.md` | Updated | Appended a separate audit row for every Markdown file changed by the ranks 33–48 review. | {REVIEW} | Per-document audit; [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/) |\n'
cl.write_text(cs)
