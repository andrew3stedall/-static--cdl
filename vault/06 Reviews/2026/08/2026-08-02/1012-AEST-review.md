---
type: review
timestamp: 2026-08-02T10:12:00+10:00
scope: unranked players challenging top 140
---

# FPL Draft review — unranked top-140 screen

## API reconciliation

The official FPL endpoints returned 564 active players, 20 teams and 380 fixtures. The 240 ranked IDs were reconciled against the active pool before screening all omitted players.

## Screening method

The full omitted pool was first triaged using current FPL metadata and prior-season minutes/points only as a discovery aid. Candidates were then assessed for expected minutes, role, set pieces, attacking or clean-sheet routes, injury and rotation risk, floor, ceiling and positional replacement value. Raw screening score did not determine final rank.

## Players inserted into the top 140

- **Frimpong → 78** (DEF, LIV) — compared with Dorgu; elite-team attacking full-back ceiling outweighs rotation risk.
- **Martinelli → 85** (MID, ARS) — compared with Hall; higher direct goal ceiling than the goalkeeper/defender cluster, but role risk prevents a Core placement.
- **Vicario → 96** (GKP, TOT) — compared with Petrović; secure starting-goalkeeper floor belongs with the established goalkeeper cluster.
- **Dunk → 108** (DEF, BHA) — compared with Keane; durable minutes and aerial/clean-sheet floor beat lower-certainty centre-backs.
- **Mykolenko → 110** (DEF, EVE) — compared with Dunk; secure full-back minutes and attacking routes justify Depth placement.
- **J.Murphy → 114** (MID, NEW) — compared with Beto; direct attacking role and proven returns beat lower-ceiling midfield depth.
- **Smith Rowe → 118** (MID, FUL) — compared with N.Jackson; creative and goal routes merit a Depth slot, discounted for competition.
- **Jensen → 123** (MID, BRE) — compared with Tonali; set-piece and creative accumulation beat lower-ceiling central midfielders.
- **Robinson → 129** (DEF, FUL) — compared with Konsa; attacking full-back upside beats ordinary centre-back replacement value.
- **Delap → 132** (FWD, CHE) — compared with Gusto; forward scarcity and scoring ceiling merit late top-140 inclusion despite Chelsea competition.
- **Gusto → 134** (DEF, CHE) — compared with De Cuyper; attacking Chelsea full-back upside narrowly beats the late defensive cluster.
- **De Cuyper → 136** (DEF, BHA) — compared with Bogle; attacking role and Brighton clean-sheet potential justify Endgame placement.
- **Bogle → 138** (DEF, LEE) — compared with Estêvão; secure attacking full-back minutes beat speculative defenders.
- **Estêvão → 140** (MID, CHE) — compared with Spence; elite attacking ceiling earns the final top-140 slot, heavily rotation-discounted.

## High-profile rejects

- **Xavi:** unknown-return knee injury and uncertain role prevented promotion.
- **Rodri:** unknown-return back injury and defensive-midfield scoring profile prevented promotion.
- **Tielemans:** hamstring flag and uncertain advanced/set-piece share prevented promotion.
- **Mainoo, Joelinton, Kamada, Lerma and similar central midfielders:** useful minutes floors but insufficient attacking ceiling versus the existing top-140 boundary.
- **Robertson, Maatsen, Yoro and other defenders:** retained outside the top 140 because current role certainty or attacking upside was weaker than the selected entrants.

## Evidence adopted

Official identity, team, position, availability, prior minutes and prior points were treated as confirmed API metadata. Team strength, likely role and draft scarcity were explicit inferences.

## Evidence rejected

Price, ownership and the triage score were not used as ranking evidence. Profile-only social results, unsupported lineup claims and raw friendly output were rejected.

## Uncertainty and reversal triggers

Frimpong, Martinelli, Gusto, Estêvão and Delap can move sharply with confirmed strongest-XI roles. Vicario, Dunk and Mykolenko have safer floors. A clear role loss, transfer, injury or set-piece change can reverse any insertion.

## Sources

- [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/)
- [Official fixtures](https://fantasy.premierleague.com/api/fixtures/)
- [Premier League preseason tracker](https://www.premierleague.com/en/news/4606700/premier-league-clubs-2026-pre-season-fixtures-and-results)
