from pathlib import Path
import re

ROOT = Path('.')
BOARD = ROOT/'vault/01 Current/Current Draft Board.md'
TEAM = ROOT/'vault/03 Teams/MCI.md'
WATCH = ROOT/'vault/01 Current/Current Watchlist.md'
HOME = ROOT/'vault/Home.md'
WIKI = ROOT/'vault/Wiki.md'
CHANGELOG = ROOT/'vault/00 Meta/Document Changelog.md'
STAMP='2026-08-03T00:30:00+10:00'
TAG='0030-AEST'
REVIEW_LINK='[[06 Reviews/2026/08/2026-08-03/0030-AEST-review]]'
CHANGE_LINK='[[07 Changes/2026/08/2026-08-03/0030-AEST-changes]]'
order=[('Haaland',411,'best raw-points ceiling, penalties and elite central-forward role'),('Semenyo',397,'strongest non-Haaland blend of minutes, direct goal threat and midfield scoring'),('Foden',398,'elite attacking ceiling but more rotation risk than Semenyo'),('Cherki',399,'creative and scoring upside narrowly ahead of Marmoush'),('Marmoush',401,'central-forward routes and scarcity, discounted for competition'),('Doku',400,'explosive winger ceiling with major minutes volatility'),('Gvardiol',391,'best defender blend of clean sheets, minutes and attacking upside'),('Guéhi',388,'secure centre-back floor and aerial route'),('Anderson',481,'attacking midfield upside but uncertain role in a crowded squad'),('Donnarumma',384,'starting-goalkeeper floor, discounted for positional replaceability'),("O'Reilly",387,'attacking defender upside with rotation risk'),('Aït-Nouri',392,'high attacking full-back ceiling but uncertain first-choice status'),('Savinho',403,'high per-minute winger upside with substantial rotation risk'),('Reijnders',404,'safer midfield accumulation but less direct FPL output'),('Grealish',238,'creative route heavily discounted by injury and role uncertainty'),('Rúben',390,'secure defensive floor when fit but limited attacking ceiling'),('Matheus N.',389,'defensive classification with role uncertainty'),('Rodrigo',402,'elite real-football role but low FPL ceiling and current back injury'),('N.Gonzalez',405,'minutes floor possible but little direct attacking output'),('Khusanov',393,'centre-back depth with uncertain starts'),('Alleyne',394,'developmental defender with weak current minutes case'),('Vitor Reis',396,'lowest current first-team role certainty in the ranked City pool')]
text=BOARD.read_text()
row_re=re.compile(r'^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|$',re.M)
rows=[]
for m in row_re.finditer(text):
 rows.append({'rank':int(m.group(1)),'player':m.group(2).strip(),'pos':m.group(3).strip(),'team':m.group(4).strip(),'segment':m.group(5).strip(),'tier':m.group(6).strip(),'id':int(m.group(7)),'status':m.group(8).strip(),'changed':m.group(9).strip(),'evidence':m.group(10).strip()})
city=[r for r in rows if r['team']=='MCI']; assert len(city)==22,len(city)
byid={r['id']:r for r in city}; slots=sorted(r['rank'] for r in city); assert set(i for _,i,_ in order)==set(byid)
slot_meta={r['rank']:(r['segment'],r['tier']) for r in rows}; new_by_rank={}; changes=[]
for slot,(name,pid,reason) in zip(slots,order):
 old=byid[pid]; seg,tier=slot_meta[slot]; new=dict(old,rank=slot,segment=seg,tier=tier,changed=STAMP,evidence=REVIEW_LINK); new_by_rank[slot]=new; changes.append((name,old['rank'],slot,reason,seg,tier,pid))
out=[]
for line in text.splitlines():
 m=row_re.match(line)
 if m and m.group(4).strip()=='MCI':
  r=new_by_rank[int(m.group(1))]; line=f"| {r['rank']} | {r['player']} | {r['pos']} | {r['team']} | {r['segment']} | {r['tier']} | {r['id']} | {r['status']} | {r['changed']} | {r['evidence']} |"
 out.append(line)
BOARD.write_text('\n'.join(out)+'\n')
team_text=TEAM.read_text(); entries=[]
for slot in slots:
 r=new_by_rank[slot]; entries.append(f"{slot}. [[02 Players/{r['player']} - {r['id']}|{r['player']}]] — {r['pos']}, MCI; {r['segment']} / {r['tier']}; {r['status']}")
block='<!-- ranked-players:start -->\n## Players by overall rank\n\nPlayers are listed in canonical overall draft rank order.\n\n'+'\n'.join(entries)+f"\n\nSource: [[01 Current/Current Draft Board]] · generated {STAMP}\n<!-- ranked-players:end -->"
team_text=re.sub(r'<!-- ranked-players:start -->.*?<!-- ranked-players:end -->',block,team_text,flags=re.S); team_text=re.sub(r'last_reviewed: .*',f'last_reviewed: {STAMP}',team_text); TEAM.write_text(team_text)
for idx,(name,old,new,reason,seg,tier,pid) in enumerate(changes,1):
 p=ROOT/f'vault/02 Players/{name} - {pid}.md'; s=p.read_text(); marker='<!-- 0030-aest-man-city-team-review -->'; section=f"\n\n{marker}\n## Manchester City team comparison — {TAG}\n\n- Internal City rank: **{idx} of 22**.\n- Overall rank: **{new}** (was {old}).\n- Segment/tier: **{seg} / {tier}**.\n- Comparator outcome: {reason}.\n- Reversal trigger: verified change in minutes, role, penalties, set pieces, fitness or first-choice status.\n- Evidence: {REVIEW_LINK}.\n"; p.write_text(s.rstrip()+section+'\n')
review=ROOT/'vault/06 Reviews/2026/08/2026-08-03/0030-AEST-review.md'; review.parent.mkdir(parents=True,exist_ok=True)
chain='\n'.join([f"- **{order[i][0]} over {order[i+1][0]}** — {order[i][2]}; confidence {'medium' if i<13 else 'low'}. Reverse with verified role, fitness, set-piece or minutes evidence." for i in range(len(order)-1)])
final='\n'.join([f"{i}. {name} — overall {new} — {seg} / {tier}" for i,(name,old,new,reason,seg,tier,pid) in enumerate(changes,1)])
review.write_text(f"---\ntype: review\nreviewed_at: {STAMP}\nteam: MCI\n---\n\n# Manchester City internal FPL Draft review — {TAG}\n\n## Scope\nAll 22 ranked Manchester City players were compared directly. Raw expected points were assessed first, then minutes, role, penalties and set pieces, injury and rotation risk, floor and ceiling; positional replacement value was applied afterward.\n\n## Evidence\n- [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/) for identity, team, position and availability.\n- Current canonical board and Manchester City team note.\n- Existing exact source note: [Fabrizio Romano on Semenyo and Cherki](https://x.com/FabrizioRomano/status/2040816965942390893).\n\n## Decisive comparison chain\n{chain}\n\n## Final internal order\n{final}\n\n## Uncertainties\nThe winger and attacking-midfield rotation, full-back hierarchy, Rodri fitness, and whether O'Reilly or Aït-Nouri receives the stronger first-choice role are the main reversal triggers.\n")
changes_file=ROOT/'vault/07 Changes/2026/08/2026-08-03/0030-AEST-changes.md'; changes_file.parent.mkdir(parents=True,exist_ok=True); change_lines='\n'.join([f"- {name}: **{old}, unchanged**" if old==new else f"- {name}: **{old} → {new}**" for name,old,new,*_ in changes]); changes_file.write_text(f"---\ntype: changes\nchanged_at: {STAMP}\nteam: MCI\n---\n\n# Manchester City ordering changes — {TAG}\n\n{change_lines}\n\nNo non-Manchester City player rank changed. The board remains 350 unique, physically ordered ranks.\n")
for path in (WATCH,HOME,WIKI):
 s=path.read_text(); marker='<!-- 0030-aest-man-city-team-review -->'; path.write_text(s.rstrip()+f"\n\n{marker}\n- Manchester City internal ordering reviewed: {REVIEW_LINK} · {CHANGE_LINK}.\n")
changed_paths=[str(BOARD),*[f'vault/02 Players/{name} - {pid}.md' for name,old,new,reason,seg,tier,pid in changes],str(TEAM),str(review),str(changes_file),str(WATCH),str(HOME),str(WIKI),str(CHANGELOG)]
cl=CHANGELOG.read_text().rstrip()+'\n'
for path in changed_paths:
 action='created' if '06 Reviews/' in path or '07 Changes/' in path else 'updated'; cl+=f"| {STAMP} | `{path}` | {action} | Manchester City internal team ordering review | {REVIEW_LINK} | https://fantasy.premierleague.com/api/bootstrap-static/ ; https://x.com/FabrizioRomano/status/2040816965942390893 |\n"
CHANGELOG.write_text(cl)
