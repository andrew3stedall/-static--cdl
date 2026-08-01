---
type: review
reviewed_at: 2026-08-01T22:07:00+10:00
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
| 1 | Haaland | B.Fernandes | Haaland projects for more goals and has the scarcer elite-forward profile. |
| 2 | B.Fernandes | Saka | Bruno has the stronger demonstrated current scoring baseline and safer set-piece monopoly. |
| 3 | Saka | Isak | Saka has the safer minutes and broader scoring routes; Isak has greater forward scarcity but more fitness uncertainty. |
| 4 | Isak | Palmer | Isak is drafted first because comparable raw ceiling plus elite forward scarcity outweighs Palmer's midfield depth advantage. |
| 5 | Palmer | Thiago | Palmer is expected to outscore Thiago through assists, bonuses and midfield scoring despite Thiago's scarcity. |
| 6 | Thiago | Watkins | Thiago's recent chance volume and likely penalties narrowly beat Watkins; reverse if Brentford role or fitness weakens. |
| 7 | Watkins | Gabriel | Watkins is expected to score slightly more and forward replacement value is lower than defender replacement value. |
| 8 | Gabriel | Gyökeres | Gabriel has the stronger proven FPL total and floor; Gyokeres can pass him if the Arsenal striker role and penalties become secure. |
| 9 | Gyökeres | Mbeumo | Gyokeres is drafted first on forward scarcity and central-goal role, although Mbeumo currently has the safer Premier League evidence. |
| 10 | Mbeumo | João Pedro | Mbeumo has the safer expected minutes and raw-points outlook; João Pedro's forward scarcity keeps the comparison close. |
| 11 | João Pedro | Cunha | João Pedro is drafted first because comparable points expectation plus forward scarcity offsets Cunha's safer opening fixtures. |
| 12 | Cunha | Wirtz | Cunha has the clearer immediate Premier League role and opening schedule; Wirtz has the higher role-change upside. |
| 13 | Wirtz | Semenyo | Wirtz has a clearer central creative role; Semenyo's Manchester City ceiling is offset by greater rotation risk. |
| 14 | Semenyo | Gibbs-White | Semenyo has the higher upside and likely points rate when starting; Gibbs-White has the safer minutes floor. |
| 15 | Gibbs-White | Rogers | Gibbs-White has substantially safer minutes and role certainty than Rogers in Chelsea's crowded attack. |
| 16 | Rogers | Bruno G. | Rogers retains rank 16 for attacking ceiling; Bruno Guimaraes is the safer-floor challenger and should pass him if Rogers is not a regular starter. |

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
