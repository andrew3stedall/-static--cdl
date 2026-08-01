---
type: review
reviewed_at: 2026-08-01T23:08:00+10:00
baseline: "[[06 Reviews/2026/08/2026-08-01/2300-AEST-review]]"
branch: codex/fpl-review-20260801-2308-ranks65-80
status: top80_pairwise_complete
---

# Ranks 65–80 pairwise sorting review

## Changes since the prior iteration

Mitoma entered the top 80 at rank 65 despite an explicit hamstring-injury discount. Xhaka and Iwobi moved ahead of the defender and goalkeeper cluster because their expected minutes and midfield scoring routes are stronger. O'Reilly, Matheus N., Lacroix and Rúben now sit outside the top 80. This completes the first manual pairwise pass across ranks 1–80.

## Method

Stable insertion-style comparison was applied to prior ranks 61–84. Raw expected season points came first, followed by expected minutes, tactical role, set pieces, injury and rotation risk, floor and ceiling. Positional replacement value was used only for close cross-position decisions.

## Pairwise decisions

| Rank | Player | Compared with | Decision | Confidence |
|---:|---|---|---|---|
| 65 | Mitoma | Xhaka | Mitoma has the higher attacking ceiling, but the unresolved hamstring issue keeps confidence low. | Low |
| 66 | Xhaka | Iwobi | Xhaka has the safer minutes, leadership role and set-piece involvement. | Medium |
| 67 | Iwobi | Anderson | Iwobi has clearer attacking minutes and substantially lower rotation risk. | Medium |
| 68 | Anderson | Ampadu | Anderson's higher ceiling narrowly beats Ampadu's safer floor. | Low |
| 69 | Ampadu | Saliba | Expected minutes and midfield scoring routes edge an injured defender. | Medium |
| 70 | Saliba | J.Timber | Saliba has the stronger established clean-sheet floor if available. | Low |
| 71 | J.Timber | Chalobah | Timber has greater attacking upside, with the groin issue explicitly discounted. | Low |
| 72 | Chalobah | Mukiele | Chalobah has the stronger clean-sheet environment and role ceiling. | Medium |
| 73 | Mukiele | Mitchell | Mukiele has a slightly stronger attacking route. | Medium |
| 74 | Mitchell | Collins | Mitchell has the wider role and more plausible assist potential. | Medium |
| 75 | Collins | Raya | Collins' outfield attacking upside narrowly beats goalkeeper scarcity. | Medium |
| 76 | Raya | Pickford | Raya has the elite-defence clean-sheet ceiling. | Medium |
| 77 | Pickford | Donnarumma | Pickford's save volume and role certainty beat the Manchester City rotation concern. | Medium |
| 78 | Donnarumma | Henderson | Donnarumma has the superior team clean-sheet ceiling. | Medium |
| 79 | Henderson | Kelleher | Henderson has the more established save and bonus profile. | Medium |
| 80 | Kelleher | O'Reilly | A nailed goalkeeper role beats uncertain outfield minutes at the top-80 boundary. | Medium |
| 81 | O'Reilly | Matheus N. | O'Reilly retains the higher attacking upside but remains a major rotation risk. | Low |
| 82 | Matheus N. | Lacroix | Manchester City team strength narrowly wins, but defender replacement remains deep. | Low |
| 83 | Lacroix | Rúben | Lacroix has the safer expected minutes. | Medium |
| 84 | Rúben | next challenger | Rúben remains outside the top 80 because defender replacement is deep and attacking upside is limited. | Medium |

## API reconciliation

All 20 assessed players remain present in the official FPL player pool with the FPL IDs, teams, positions and availability labels preserved on the board. No transfer-watch exception was required.

## Evidence adopted

- Mitoma remains a top-80 upside selection, but not without an injury discount.
- Xhaka and Iwobi lead the block's midfielders on expected minutes and broader scoring routes.
- Saliba and Timber remain injury-sensitive rather than being promoted on Arsenal clean-sheet potential alone.
- Goalkeepers were kept behind comparable outfield players because replacement remains deep in an eight-manager league.
- Manchester City defenders with uncertain minutes were not promoted on team strength alone.

Sources: [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/); [Official FPL fixtures](https://fantasy.premierleague.com/api/fixtures/); [Premier League fixture-difficulty ratings](https://www.premierleague.com/en/news/4675493/get-the-fixture-difficulty-ratings-for-202627-fpl-season).

## Evidence rejected or limited

- Price and ownership were not used to order the block.
- Team strength was not accepted as proof of starts.
- Friendly output without probable-first-team role context was not used to force movement.
- No inaccessible or unspecific X profile claim was treated as evidence.

## Uncertainties and reversal triggers

Mitoma's recovery, Saliba and Timber return timelines, Manchester City defender minutes, Chelsea centre-back hierarchy and confirmed goalkeeper starting roles can materially reorder this block.

## Next trigger

Revisit completed top-80 blocks when injuries, starting roles, transfers, penalties or repeated preseason patterns materially change a comparator.
