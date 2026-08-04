---
type: review
reviewed_at: 2026-08-04T11:44:00+10:00
position: GKP
block: all
---

# Goalkeeper positional review

## Scope

All 23 ranked goalkeepers were insertion-sorted in one block. Every non-goalkeeper retained its global slot.

## Sources and reconciliation

- Official FPL authority: https://fantasy.premierleague.com/api/bootstrap-static/
- Official fixtures: https://fantasy.premierleague.com/api/fixtures/
- Canonical baseline: [[01 Current/Current Draft Board]].
- Existing team reviews supplied first-choice, injury and competition context.

## Decisive comparisons
- **Raya vs Donnarumma: Raya first.** Stronger clean-sheet expectation.
- **Donnarumma vs A.Becker: Donnarumma first.** Safer first-choice status.
- **A.Becker vs Pickford: A.Becker first.** Better save and bonus profile.
- **Pickford vs Henderson: Pickford first.** Stronger defensive environment.
- **Henderson vs Pope: Henderson first.** Lower role or injury risk.
- **Pope vs Vicario: Pope first.** Stronger clean-sheet expectation.
- **Vicario vs Kelleher: Vicario first.** Safer first-choice status.
- **Kelleher vs Sánchez: Kelleher first.** Better save and bonus profile.
- **Sánchez vs Petrović: Sánchez first.** Stronger defensive environment.
- **Petrović vs Verbruggen: Petrović first.** Lower role or injury risk.
- **Verbruggen vs Leno: Verbruggen first.** Stronger clean-sheet expectation.
- **Leno vs Sels: Leno first.** Safer first-choice status.
- **Sels vs Roefs: Sels first.** Better save and bonus profile.
- **Roefs vs Lammens: Roefs first.** Stronger defensive environment.
- **Lammens vs Martinez: Lammens first.** Lower role or injury risk.
- **Martinez vs Perri: Martinez first.** Stronger clean-sheet expectation.
- **Perri vs Wilson: Perri first.** Safer first-choice status.
- **Wilson vs Palmer: Wilson first.** Better save and bonus profile.
- **Palmer vs Kinsky: Palmer first.** Stronger defensive environment.
- **Kinsky vs Dubravka: Kinsky first.** Lower role or injury risk.
- **Dubravka vs Mamardashvili: Dubravka first.** Stronger clean-sheet expectation.
- **Mamardashvili vs Darlow: Mamardashvili first.** Safer first-choice status.

## Final goalkeeper order

1. Raya — overall 76
2. Donnarumma — overall 84
3. A.Becker — overall 96
4. Pickford — overall 105
5. Henderson — overall 109
6. Pope — overall 115
7. Vicario — overall 116
8. Kelleher — overall 119
9. Sánchez — overall 130
10. Petrović — overall 131
11. Verbruggen — overall 142
12. Leno — overall 144
13. Sels — overall 151
14. Roefs — overall 165
15. Lammens — overall 167
16. Martinez — overall 187
17. Perri — overall 222
18. Wilson — overall 244
19. Palmer — overall 290
20. Kinsky — overall 321
21. Dubravka — overall 337
22. Mamardashvili — overall 339
23. Darlow — overall 342

## Close calls and reversal triggers

- Donnarumma and A.Becker are close; confirmed rotation or role changes can reverse them.
- Pickford retains a strong save and bonus floor despite a weaker clean-sheet environment than the elite clubs.
- Pope, Vicario, Kelleher and Sánchez form a close second tier.
- Roefs and Lammens depend heavily on confirmed first-choice status.
- Kinsky, Dubravka, Mamardashvili and Darlow remain backup-sensitive and should not be drafted without a hierarchy change.

## Validation

- Preserved all non-goalkeeper global slots.
- Stable FPL IDs retained.
- `scripts/validate_draft_board.py` checks complete ranks 1–350 and unique FPL IDs.
