#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
TS = "2026-08-01T22:07:00+10:00"
REVIEW_LINK = "[[06 Reviews/2026/08/2026-08-01/2207-AEST-review]]"
CHANGES_LINK = "[[07 Changes/2026/08/2026-08-01/2207-AEST-changes]]"

order = [
(1,"Haaland","Erling Haaland","FWD","MCI",411,"S","Elite 239-point baseline, clearest central role and highest ceiling.","B.Fernandes","Haaland projects for more goals and has the scarcer elite-forward profile.","https://www.premierleague.com/en/news/4680821/the-scouts-analysis-of-15-key-player-prices-in-202627-fantasy"),
(2,"B.Fernandes","Bruno Fernandes","MID","MUN",426,"S","235 points, penalties, corners, 7.6 points per match under Carrick and favourable opening fixtures.","Saka","Bruno has the stronger demonstrated current scoring baseline and safer set-piece monopoly.","https://www.premierleague.com/en/news/4680821/the-scouts-analysis-of-15-key-player-prices-in-202627-fantasy"),
(3,"Saka","Bukayo Saka","MID","ARS",12,"A+","Primary Arsenal creator with elite ceiling; prior total was injury-suppressed.","Isak","Saka has the safer minutes and broader scoring routes; Isak has greater forward scarcity but more fitness uncertainty.","https://www.premierleague.com/en/news/4650977/just-how-important-is-saka-to-arsenal"),
(4,"Isak","Alexander Isak","FWD","LIV",379,"A+","Demonstrated 211-point ceiling, clearer striker route after Ekitike injury and possible penalties.","Palmer","Isak is drafted first because comparable raw ceiling plus elite forward scarcity outweighs Palmer's midfield depth advantage.","https://www.premierleague.com/en/news/4680821/the-scouts-analysis-of-15-key-player-prices-in-202627-fantasy"),
(5,"Palmer","Cole Palmer","MID","CHE",154,"A+","Two prior 200-point seasons, summer rest and no European football; primary Chelsea attacking hub.","Thiago","Palmer is expected to outscore Thiago through assists, bonuses and midfield scoring despite Thiago's scarcity.","https://www.premierleague.com/en/news/4680821/the-scouts-analysis-of-15-key-player-prices-in-202627-fantasy"),
(6,"Thiago","Igor Thiago","FWD","BRE",106,"A+","22 goals, 41 big chances, secure striker role and likely penalties.","Watkins","Thiago's recent chance volume and likely penalties narrowly beat Watkins; reverse if Brentford role or fitness weakens.","https://www.premierleague.com/en/news/4680821/the-scouts-analysis-of-15-key-player-prices-in-202627-fantasy"),
(7,"Watkins","Ollie Watkins","FWD","AVL",55,"A+","Proven durable starting striker with a strong season-long floor and scarce classification.","Gabriel","Watkins is expected to score slightly more and forward replacement value is lower than defender replacement value.","https://fantasy.premierleague.com/api/bootstrap-static/"),
(8,"Gabriel","Gabriel Magalhaes","DEF","ARS",4,"A+","209 points, 18 clean sheets, set-piece threat and defensive-contribution routes.","Gyökeres","Gabriel has the stronger proven FPL total and floor; Gyokeres can pass him if the Arsenal striker role and penalties become secure.","https://www.premierleague.com/en/news/4680821/the-scouts-analysis-of-15-key-player-prices-in-202627-fantasy"),
(9,"Gyökeres","Viktor Gyökeres","FWD","ARS",25,"A","High-upside Arsenal centre-forward; scarce role and Saka partnership justify promotion.","Mbeumo","Gyokeres is drafted first on forward scarcity and central-goal role, although Mbeumo currently has the safer Premier League evidence.","https://www.premierleague.com/en/news/4650977/just-how-important-is-saka-to-arsenal"),
(10,"Mbeumo","Bryan Mbeumo","MID","MUN",427,"A","Strong attacking role in a favourable opening schedule; less set-piece control than Bruno.","João Pedro","Mbeumo has the safer expected minutes and raw-points outlook; João Pedro's forward scarcity keeps the comparison close.","https://www.premierleague.com/en/news/4675493/get-the-fixture-difficulty-ratings-for-202627-fpl-season"),
(11,"João Pedro","João Pedro","FWD","CHE",165,"A","Forward classification and attacking quality retain early value, discounted for Chelsea competition.","Cunha","João Pedro is drafted first because comparable points expectation plus forward scarcity offsets Cunha's safer opening fixtures.","https://fantasy.premierleague.com/api/bootstrap-static/"),
(12,"Cunha","Matheus Cunha","MID","MUN",428,"A","Central attacker in a team with only one opponent above FDR 3 in the first eight.","Wirtz","Cunha has the clearer immediate Premier League role and opening schedule; Wirtz has the higher role-change upside.","https://www.premierleague.com/en/news/4675493/get-the-fixture-difficulty-ratings-for-202627-fpl-season"),
(13,"Wirtz","Florian Wirtz","MID","LIV",366,"A","Used behind the striker and expected to become more important after Salah's departure.","Semenyo","Wirtz has a clearer central creative role; Semenyo's Manchester City ceiling is offset by greater rotation risk.","https://www.fantasyfootballscout.co.uk/2026/07/31/fpl-pre-season-tavernier-impresses-muharemovic-class-szoboszlai-deeper"),
(14,"Semenyo","Antoine Semenyo","MID","MCI",397,"A","High team ceiling but meaningful competition and rotation risk.","Gibbs-White","Semenyo has the higher upside and likely points rate when starting; Gibbs-White has the safer minutes floor.","https://x.com/FabrizioRomano/status/2040816965942390893"),
(15,"Gibbs-White","Morgan Gibbs-White","MID","NFO",480,"A","Secure minutes, central role and high floor; lower ceiling than the elite attackers above.","Rogers","Gibbs-White has substantially safer minutes and role certainty than Rogers in Chelsea's crowded attack.","https://fantasy.premierleague.com/api/bootstrap-static/"),
(16,"Rogers","Morgan Rogers","MID","CHE",40,"A","Promising link-up role with Palmer but substantial competition and role uncertainty.","Bruno G.","Rogers retains rank 16 for attacking ceiling; Bruno Guimaraes is the safer-floor challenger and should pass him if Rogers is not a regular starter.","https://www.reuters.com/sports/soccer/rogers-palmer-combination-key-chelsea-revival-says-alonso-2026-07-27/"),
]

board = ROOT / "vault/01 Current/Current Draft Board.md"
text = board.read_text()
text = re.sub(r"last_updated: .*", f"last_updated: {TS}", text, count=1)
text = re.sub(r"status: .*", "status: top16_pairwise_sorted", text, count=1)
text = text.replace("The second review corrects the first board's excessive dependence on 2025/26 total points by weighting current role, minutes security, injury status, transfer context, preseason evidence, fixture environment and positional scarcity.", "The first 16 have now been stable-sorted by explicit player-versus-player comparisons. Raw expected FPL points are assessed first, followed by minutes, role, set pieces and risk; positional replacement value then determines draft priority in close cross-position comparisons.")
rows=[]
for rank,short,full,pos,team,fid,tier,assessment,comp,decision,url in order:
    seg="Franchise" if rank<=8 else "Foundation"
    rows.append(f"| {rank} | {short} | {pos} | {team} | {seg} | {tier} | {fid} | Available | {TS} | {REVIEW_LINK} |")
start = text.index("| 1 |")
end = text.index("| 17 |")
text = text[:start] + "\n".join(rows) + "\n" + text[end:]
board.write_text(text)

for rank,short,full,pos,team,fid,tier,assessment,comp,decision,url in order:
    p=ROOT/f"vault/02 Players/{short} - {fid}.md"
    position={"FWD":"Forward","MID":"Midfielder","DEF":"Defender"}[pos]
    content=f'''---
type: player
fpl_id: {fid}
player_name: {full}
team: "[[03 Teams/{team}]]"
position: "[[04 Positions/{position}]]"
api_status: available
current_rank: {rank}
current_segment: {"Franchise" if rank<=8 else "Foundation"}
last_reviewed: {TS}
---

# {full}

## Current assessment

{assessment}

## Pairwise placement

- Compared with: **{comp}**.
- Decision: {decision}
- Confidence: medium{'-high' if rank <= 8 else ''}.
- Reversal trigger: material injury, role, penalty or expected-minutes evidence that changes the comparison.

## Evidence timeline

- 2026-08-01 22:07 AEST — Pairwise-sorted to rank {rank} in the first-16 block.
- [Primary evidence]({url})
- [Official FPL player pool](https://fantasy.premierleague.com/api/bootstrap-static/)

## Backlinks

- [[01 Current/Current Draft Board]]
- {REVIEW_LINK}
- {CHANGES_LINK}
'''
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(content)

review=ROOT/"vault/06 Reviews/2026/08/2026-08-01/2207-AEST-review.md"
review.parent.mkdir(parents=True,exist_ok=True)
pairs="\n".join(f"| {r} | {s} | {c} | {d} |" for r,s,_,_,_,_,_,_,c,d,_ in order)
review.write_text(f'''---
type: review
reviewed_at: {TS}
baseline: "[[06 Reviews/2026/08/2026-08-01/2000-AEST-review]]"
branch: codex/fpl-review-20260801-2207-top16-pairwise
status: top16_pairwise_complete
---

# Top-16 pairwise sorting review

## Changes since the prior iteration

Palmer moved 6→5, Thiago 5→6, Gyökeres 14→9, Mbeumo 11→10, João Pedro 10→11, Wirtz 15→13, Semenyo 13→14 and Gibbs-White 9→15. Haaland, Bruno Fernandes, Saka, Isak, Watkins, Gabriel, Cunha and Rogers retained their positions after direct comparisons.

## Method

A stable insertion-style comparator was applied. For each player, raw expected season points were considered first, then minutes, role, penalties/set pieces, injury/rotation risk, floor and ceiling. Positional replacement value was applied only after the raw-points judgement. The final decision was which player should be drafted first in this eight-manager league.

## Pairwise decisions

| New rank | Player | Compared with | Decision |
|---:|---|---|---|
{pairs}

## API reconciliation

The official bootstrap and fixtures endpoints were reachable at review time. All 16 players remain present with unchanged FPL IDs, teams, positions and available status. No active-player removal or registration watchlist case was required.

- [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/)
- [Official FPL fixtures](https://fantasy.premierleague.com/api/fixtures/)

## Evidence adopted

- Haaland: 239 points, 27 goals and eight assists; repeated fast starts.
- Bruno Fernandes: 235 points and 7.6 points per match after Carrick took charge.
- Gabriel: 209 points, 18 clean sheets and multiple return routes.
- Isak: demonstrated 211-point ceiling and clearer striker route after Ekitike injury.
- Thiago: 22 goals, 80 box shots and 41 big chances.
- Manchester United: only one opponent above FDR 3 in the opening eight.
- Wirtz: preseason use behind the striker.

Sources: [PL key-player analysis](https://www.premierleague.com/en/news/4680821/the-scouts-analysis-of-15-key-player-prices-in-202627-fantasy), [PL FDR](https://www.premierleague.com/en/news/4675493/get-the-fixture-difficulty-ratings-for-202627-fpl-season), [Saka analysis](https://www.premierleague.com/en/news/4650977/just-how-important-is-saka-to-arsenal), [FFScout preseason report](https://www.fantasyfootballscout.co.uk/2026/07/31/fpl-pre-season-tavernier-impresses-muharemovic-class-szoboszlai-deeper), [Reuters on Rogers and Palmer](https://www.reuters.com/sports/soccer/rogers-palmer-combination-key-chelsea-revival-says-alonso-2026-07-27/).

## Evidence rejected or limited

- Price and ownership were not used as ranking objectives.
- One friendly return was not treated as proof of a stable role.
- Manchester City membership was not treated as an automatic promotion because rotation can erase team-strength gains.
- Possible penalties for Isak, Gyökeres or Chelsea attackers remain inference unless confirmed.
- No complete current X following graph was accessible; no view was attributed to James, Ben Crellin or Sam Martin without a specific accessible post.

## Close calls and reversal triggers

- Saka/Isak: Isak passes Saka if fitness and penalties become secure while Saka's availability weakens.
- Palmer/Thiago: Thiago passes Palmer if Palmer loses centrality or Thiago's penalty monopoly is confirmed with strong Brentford form.
- Gabriel/Gyökeres: Gyökeres passes Gabriel if he becomes a nailed penalty-taking Arsenal striker.
- Mbeumo/João Pedro: João Pedro passes Mbeumo if Chelsea establishes him as a secure central forward.
- Rogers/Bruno Guimarães: Bruno passes Rogers if Rogers is not a regular starter.

## Next block

Sort ranks 17–32 using the same comparator, while allowing challengers from ranks 13–36 to cross the boundary.
''')

changes=ROOT/"vault/07 Changes/2026/08/2026-08-01/2207-AEST-changes.md"
changes.parent.mkdir(parents=True,exist_ok=True)
changes.write_text(f'''---
type: changes
changed_at: {TS}
prior_review: "[[06 Reviews/2026/08/2026-08-01/2000-AEST-review]]"
current_review: {REVIEW_LINK}
---

# Changes — top-16 pairwise sort

| Player | Old | New | Delta | Reason |
|---|---:|---:|---:|---|
| Palmer | 6 | 5 | +1 | Expected raw points and elite creative role beat Thiago's scarcity adjustment. |
| Thiago | 5 | 6 | -1 | Still elite, but Palmer projects slightly higher. |
| Gyökeres | 14 | 9 | +5 | Central Arsenal forward upside and positional scarcity. |
| Mbeumo | 11 | 10 | +1 | Safer minutes and favourable opening schedule. |
| João Pedro | 10 | 11 | -1 | Chelsea competition discount. |
| Wirtz | 15 | 13 | +2 | Central creative preseason role. |
| Semenyo | 13 | 14 | -1 | Manchester City rotation discount. |
| Gibbs-White | 9 | 15 | -6 | Strong floor but lower ceiling than the promoted attackers. |

No entrant or removal occurred. Rogers retained rank 16 after comparison with Bruno Guimarães at 17. All player IDs, teams, positions and API statuses remained unchanged.
''')

# Update Home and Wiki latest links.
for rel in ["vault/Home.md","vault/Wiki.md"]:
    p=ROOT/rel; t=p.read_text()
    t=re.sub(r"last_updated: .*",f"last_updated: {TS}",t,count=1)
    if rel.endswith("Wiki.md"):
        t=re.sub(r'latest_review: .*',f'latest_review: "{REVIEW_LINK}"',t,count=1)
        t=re.sub(r'latest_changes: .*',f'latest_changes: "{CHANGES_LINK}"',t,count=1)
        t=t.replace("The first official-API-linked top-220 board remains the canonical ordering.","The first 16 positions have now been explicitly pairwise-sorted; ranks 17–80 retain the prior manual source correction pending their own pairwise blocks.")
    t=re.sub(r"- \[\[06 Reviews/2026/08/2026-08-01/[^\]]+\|[^\]]+\]\]",f"- {REVIEW_LINK}",t,count=1)
    t=re.sub(r"- \[\[07 Changes/2026/08/2026-08-01/[^\]]+\|[^\]]+\]\]",f"- {CHANGES_LINK}",t,count=1)
    p.write_text(t)

watch=ROOT/"vault/01 Current/Current Watchlist.md"
wt=watch.read_text(); wt=re.sub(r"last_updated: .*",f"last_updated: {TS}",wt,count=1)
wt=wt.replace("| Top 80 | Ranking quality | Initial scarcity model appears to overvalue some defenders and low-ceiling midfielders. | Material reorder of early and middle rounds. | Manual account-by-account review using the X source graph. | High that review is needed | [[06 Reviews/2026/08/2026-08-01/1738-AEST-review]] |","| Ranks 17–80 | Ranking quality | Ranks 1–16 are pairwise-sorted; the remaining top-80 blocks still need explicit neighbour comparisons. | Material reorder of rounds 3–10. | Sort ranks 17–32 next, including boundary challengers. | Confirmed work remaining | [[06 Reviews/2026/08/2026-08-01/2207-AEST-review]] |")
watch.write_text(wt)

# Append changelog rows.
cl=ROOT/"vault/00 Meta/Document Changelog.md"; ct=cl.read_text(); ct=re.sub(r"last_updated: .*",f"last_updated: {TS}",ct,count=1)
changed=["vault/01 Current/Current Draft Board.md","vault/01 Current/Current Watchlist.md","vault/Home.md","vault/Wiki.md","vault/06 Reviews/2026/08/2026-08-01/2207-AEST-review.md","vault/07 Changes/2026/08/2026-08-01/2207-AEST-changes.md"]+[f"vault/02 Players/{s} - {fid}.md" for _,s,_,_,_,fid,_,_,_,_,_ in order]+["vault/00 Meta/Document Changelog.md"]
for path in changed:
    action="Created" if "2207-AEST" in path else "Updated"
    summary="Recorded first-16 pairwise sorting evidence and current placement." if "02 Players" in path else "Updated for the completed first-16 pairwise sorting block."
    ct+=f"\n| {TS} | `{path}` | {action} | {summary} | {REVIEW_LINK} | [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/); [PL key-player analysis](https://www.premierleague.com/en/news/4680821/the-scouts-analysis-of-15-key-player-prices-in-202627-fantasy) |"
cl.write_text(ct+"\n")

# Remove one-off helpers from net diff.
(ROOT/"scripts/run_top16_pairwise_once.py").unlink(missing_ok=True)
(ROOT/".github/workflows/run-top16-pairwise-once.yml").unlink(missing_ok=True)
