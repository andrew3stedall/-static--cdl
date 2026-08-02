---
type: review
timestamp: 2026-08-02T17:58:00+10:00
scope: Arsenal internal ordering
---

# Arsenal internal team review

## API reconciliation

The live official FPL bootstrap endpoint was fetched during generation. All 21 Arsenal players on the canonical board retained stable IDs present in the active API pool. The canonical board remained exactly 350 physically ordered ranks with 350 unique FPL IDs.

## Method

Every Arsenal player was insertion-compared within the club. Each comparison considered raw expected season points first, then expected minutes, tactical role, penalties and set pieces, injury and rotation risk, floor and ceiling. Positional replacement value was applied only after the raw-points assessment. The Arsenal players were reassigned only across the club's existing overall-rank slots, preserving every non-Arsenal player's rank.

## Final Arsenal order

1. **Saka** — overall rank 3
2. **Gabriel** — overall rank 8
3. **Gyökeres** — overall rank 9
4. **Eze** — overall rank 19
5. **Ødegaard** — overall rank 20
6. **Rice** — overall rank 31
7. **Havertz** — overall rank 70
8. **Martinelli** — overall rank 71
9. **Raya** — overall rank 76
10. **Calafiori** — overall rank 82
11. **Saliba** — overall rank 85
12. **J.Timber** — overall rank 91
13. **Hincapie** — overall rank 134
14. **Zubimendi** — overall rank 137
15. **Merino** — overall rank 190
16. **Tzolis** — overall rank 228
17. **Madueke** — overall rank 239
18. **White** — overall rank 264
19. **G.Jesus** — overall rank 316
20. **Lewis-Skelly** — overall rank 334
21. **Mosquera** — overall rank 343

## Decisive comparisons

- **Saka over Gabriel:** Saka projects for more raw points through elite attacking volume, penalties and set pieces; draft Saka first.
- **Gabriel over Gyökeres:** Gyökeres may edge raw attacking points, but Gabriel's elite minutes, clean sheets, aerial threat and defender scarcity keep Gabriel narrowly ahead in this league.
- **Gyökeres over Eze:** Gyökeres has the clearer central-goal role and forward scarcity; Eze has more rotation and set-piece uncertainty.
- **Eze over Ødegaard:** Eze carries the higher direct goal ceiling; Ødegaard has the steadier creative floor. Draft Eze first, close confidence.
- **Ødegaard over Rice:** Ødegaard's advanced role gives him the higher attacking ceiling, while Rice's set pieces and defensive contributions give the safer floor.
- **Rice over Havertz:** Rice projects for more secure minutes and repeatable accumulation; Havertz's forward scarcity narrows but does not reverse the order.
- **Havertz over Martinelli:** Havertz's forward classification and central-role routes beat Martinelli's winger rotation risk, despite a close raw-points case.
- **Martinelli over Raya:** Martinelli's attacking ceiling should be drafted before a replaceable goalkeeper even with rotation risk.
- **Raya over Calafiori:** Raya has the safer season-long minutes floor; Calafiori has more attacking upside but greater availability and rotation risk.
- **Calafiori over Saliba:** Calafiori's attacking routes narrowly beat Saliba while Saliba carries an unknown-return back injury; reverse when Saliba is fully fit and starting.
- **Saliba over J.Timber:** Saliba's established centre-back minutes floor beats Timber's groin recovery and wider rotation possibilities.
- **J.Timber over Hincapie:** Timber has the stronger proven Arsenal role and attacking full-back ceiling when fit; Hincapie remains a hierarchy watch.
- **Hincapie over Zubimendi:** Hincapie's clean-sheet access and defensive scarcity edge Zubimendi's low attacking ceiling.
- **Zubimendi over Merino:** Zubimendi has the clearer minutes floor; Merino needs a repeatable advanced or emergency-forward role to reverse it.
- **Merino over Tzolis:** Merino's established minutes path beats Tzolis's high-upside but uncertain winger role.
- **Tzolis over Madueke:** Tzolis has the stronger recent production profile, but this is a low-confidence rotation comparison.
- **Madueke over White:** Madueke's attacking ceiling beats White's uncertain starting role; White would reverse with confirmed first-choice full-back minutes.
- **White over G.Jesus:** White has a more credible path to usable minutes; Jesus remains a role and fitness watch despite forward scarcity.
- **G.Jesus over Lewis-Skelly:** Jesus retains greater per-start scoring upside and forward scarcity, while Lewis-Skelly's FPL midfield role limits clean-sheet value.
- **Lewis-Skelly over Mosquera:** Lewis-Skelly offers more attacking upside; Mosquera is primarily centre-back depth with a lower ceiling.

## Evidence adopted

- https://fantasy.premierleague.com/api/bootstrap-static/
- https://www.premierleague.com/en/news/4430457/who-are-the-best-arsenal-picks-in-fantasy
- https://www.premierleague.com/en/news/4681056/fpl-prices-revealed-for-arsenal-winger-tzolis-and-two-other-signings
- https://www.premierleague.com/en/news/4650977/just-how-important-is-saka-to-arsenal
- https://www.premierleague.com/en/news/4655472/who-are-the-best-arsenal-players-to-own-for-gameweek-37

## Evidence rejected or limited

- Price and ownership were not used as draft value.
- Historical single-Gameweek recommendations were used only for role and scoring-route context, not copied as a season ranking.
- Tzolis's Belgian production was treated as ceiling evidence, not proof of Arsenal minutes.
- Injury flags from the live API were retained, but unknown return dates were not converted into false recovery probabilities.

## Close calls and reversal triggers

- Gabriel versus Gyökeres reverses if Gyökeres secures penalties and an uninterrupted central-forward role while Gabriel's minutes become managed.
- Eze versus Ødegaard remains close and reverses if Ødegaard reclaims a clearly more advanced role or a larger set-piece share.
- Havertz versus Martinelli reverses if Martinelli becomes the repeated first-choice left winger and Havertz loses central minutes.
- Calafiori versus Saliba reverses immediately when Saliba is fully fit and starting regularly.
- Tzolis versus Madueke depends on repeated probable-first-team starts and set-piece evidence.

## Next triggers

Monitor the next strongest-XI friendly, penalty and corner duties, Saliba and Timber training status, the left-wing hierarchy, and Havertz's central minutes.
