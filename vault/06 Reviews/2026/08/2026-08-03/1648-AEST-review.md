---
type: review
reviewed_at: 2026-08-03T16:48:00+10:00
position: FWD
block: 1-30
challengers: 31-35
---

# Forward positional review — block 1

## Scope

Insertion-sorted the first 30 forwards and tested the five forwards immediately below the block. Non-forward global slots were preserved; forwards were reassigned only across the existing forward-occupied global slots.

## Sources and reconciliation

- Official player identity, team, position and availability authority: https://fantasy.premierleague.com/api/bootstrap-static/
- Canonical baseline: [[01 Current/Current Draft Board]].
- Team-level conclusions from the latest immutable club reviews were retained unless a direct forward-versus-forward comparison justified movement.
- No inaccessible source was used as evidence. No price, ownership or value-for-money input was used.

## Comparator

For every pair, raw expected season FPL points were assessed first. Expected minutes, tactical role, penalties/set pieces, injury and rotation risk, floor and ceiling followed. Positional scarcity did not distinguish these same-position comparisons.

## Decisive comparisons
- **Haaland vs Isak: Haaland first.** Higher penalty-backed goal ceiling and the strongest secure central role.
- **Isak vs Watkins: Isak first.** Liverpool attack and elite scoring ceiling narrowly outweigh Watkins' safer continuity.
- **Watkins vs Thiago: Watkins first.** Higher raw points expectation in a stronger attack; Thiago's penalties keep it close.
- **Thiago vs Gyökeres: Thiago first.** Premier League role and penalty certainty currently beat adaptation uncertainty.
- **Gyökeres vs João Pedro: Gyökeres first.** Clearer elite-team number-nine ceiling; João Pedro has the broader creative floor.
- **Mateta vs Solanke: Mateta first.** Penalty and focal-point role narrowly beat Solanke's stronger team context.
- **Solanke vs Calvert-Lewin: Solanke first.** Higher expected minutes and stronger attacking environment.
- **Marmoush vs Evanilson: Marmoush first.** Higher ceiling; rotation risk prevents a larger gap.
- **Evanilson vs Šeško: Evanilson first.** Safer current availability and established minutes; Šeško reverses with full fitness and a locked role.
- **Wood vs Wissa: Wood first.** Penalty/focal role and proven floor narrowly win; age and minutes are reversal triggers.
- **Wissa vs Woltemade: Wissa first.** More proven Premier League scoring route.
- **Woltemade vs Richarlison: Woltemade first.** Clearer season-long central role; Richarlison carries heavier competition risk.
- **Richarlison vs Delap: Richarlison first.** Proven per-minute output narrowly wins, but Delap rises above him with confirmed starts.
- **Delap vs Havertz: Delap first.** Clearer direct striker route; Havertz's role remains tactically variable.
- **Brobbey vs Muniz: Brobbey first.** Slightly clearer first-choice route; Muniz has the stronger proven league production.
- **Muniz vs Strand Larsen: Muniz first.** Better combination of raw points ceiling and established Premier League output.
- **Strand Larsen vs Beto: Strand Larsen first.** More complete scoring profile; Beto's penalty/starting role could reverse it.
- **Beto vs Nketiah: Beto first.** Clearer central-forward minutes and aerial route.
- **Nketiah vs Welbeck: Nketiah first.** Higher season-long ceiling; Welbeck has the safer veteran floor when fit.
- **Igor Jesus vs Barry: Igor Jesus first.** Stronger immediate senior-role case.
- **Barry vs Ekitiké: Barry first.** Availability wins while Ekitiké carries an Achilles return-date risk.
- **Ekitiké vs Osula: Ekitiké first.** Much higher ceiling if fit; Osula has a weak minutes path.
- **Kalimuendo vs N.Jackson: Kalimuendo first.** Slightly clearer hierarchy; Jackson's transfer and minutes uncertainty cap him.
- **N.Jackson vs Emegha: N.Jackson first.** More established Premier League production.
- **Emegha vs Isidor: Emegha first.** Higher attacking ceiling despite fitness uncertainty.
- **Isidor vs Wright: Isidor first.** Stronger current top-flight role case.
- **Wright vs Hirst: Wright first.** Penalty potential and broader scoring route.
- **Hirst vs Georginio: Hirst first.** Clearer established central-forward pathway.

## Final positional order for reviewed set

1. Haaland — overall 1
2. Isak — overall 4
3. Watkins — overall 6
4. Thiago — overall 7
5. Gyökeres — overall 9
6. João Pedro — overall 11
7. Mateta — overall 21
8. Solanke — overall 27
9. Calvert-Lewin — overall 34
10. Marmoush — overall 37
11. Evanilson — overall 48
12. Šeško — overall 50
13. Wood — overall 51
14. Wissa — overall 53
15. Woltemade — overall 58
16. Richarlison — overall 62
17. Delap — overall 70
18. Havertz — overall 72
19. Brobbey — overall 73
20. Muniz — overall 74
21. Strand Larsen — overall 81
22. Beto — overall 87
23. Nketiah — overall 90
24. Welbeck — overall 108
25. Igor Jesus — overall 110
26. Barry — overall 135
27. Ekitiké — overall 155
28. Osula — overall 173
29. Kalimuendo — overall 189
30. N.Jackson — overall 193
31. Emegha — overall 195
32. Isidor — overall 196
33. Wright — overall 199
34. Hirst — overall 201
35. Georginio — overall 205

## Evidence adopted

- Current official API classification and availability metadata.
- Previously documented club-role, injury and competition conclusions where still consistent with the current canonical board.

## Evidence rejected

- Team-order rank alone was not treated as proof of cross-team superiority.
- Reputation without a credible minutes path did not justify promotion.
- No movement was manufactured for challengers 31–35 where the comparator did not beat the block boundary.

## Close calls and reversal triggers

- Watkins/Thiago reverses if Thiago retains penalties and Watkins loses meaningful minutes or penalty share.
- Evanilson/Šeško reverses when Šeško is fully fit and confirmed as the regular starter.
- Richarlison/Delap reverses with a sustained Delap starting role or continued Richarlison rotation.
- Brobbey/Muniz is low confidence and should react to competitive starting line-ups and penalty ownership.
- Ekitiké should rise materially once a reliable Achilles return and first-team role are confirmed.

## Validation

- Reviewed positional ranks 1–30 plus challengers 31–35.
- Preserved all non-forward global slots.
- Required complete ranks 1–350 and unique FPL IDs are checked by `scripts/validate_draft_board.py`.
