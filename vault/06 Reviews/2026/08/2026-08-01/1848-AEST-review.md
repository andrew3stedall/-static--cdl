---
type: review
reviewed_at: 2026-08-01T18:48:00+10:00
baseline: "[[06 Reviews/2026/08/2026-08-01/1738-AEST-review]]"
branch: codex/fpl-review-20260801-1848-top80-source-correction
status: top80_source_corrected
---

# Second 2026/27 FPL Draft review — top-80 source correction

## Scope

This run corrects the first 80 positions of the initial 220-player board for an eight-manager, 20-round FPL Draft league.

The first review established a complete official-ID baseline, but explicitly warned that the precise order was not mature. This review investigated that weakness rather than simply refreshing the same ranking.

The run prioritised:

1. reconciling the official FPL player pool and availability metadata;
2. identifying the actual construction of the first external baseline;
3. manually re-ranking the top 80 using current role, expected minutes, injuries, transfers, preseason evidence, fixture environment and positional scarcity;
4. expanding the public X/source network through Planet FPL, the official FPL expert panel, FML FPL and associated analysts;
5. recording every material rise, fall, rejected conclusion and remaining uncertainty.

## Executive conclusion

The first board was materially biased toward **2025/26 total points**. The external page used as a ranking input states that its current pre-draft order is based on last season's real points until live August rankings are released. That explains several implausible results, including Gabriel third, Palmer 35th, Wirtz 77th and Isak 96th.

Source: [Waiver FPL 2026/27 draft board](https://waiverfpl.com/draft).

The second board is therefore not a routine update. It is a methodological correction.

The clearest revised anchors are:

| Rank | Player | Position | Team | Previous rank | Core reason |
|---:|---|---|---|---:|---|
| 1 | Haaland | FWD | Manchester City | 1 | Elite ceiling, secure central role and proven fast starts. |
| 2 | Bruno Fernandes | MID | Manchester United | 2 | Attacking role, penalties, corners, elite recent production and favourable opening fixtures. |
| 3 | Saka | MID | Arsenal | 11 | Elite attacking role was understated by an injury-affected prior-season total. |
| 4 | Isak | FWD | Liverpool | 96 | Ekitiké injury creates a clearer striker route; penalties are plausible after Salah's departure. |
| 5 | Igor Thiago | FWD | Brentford | 5 | 22 goals, elite chance volume, nailed striker and likely penalty role. |
| 6 | Palmer | MID | Chelsea | 35 | Demonstrated 200-point ceiling, rest and no European football; last season's total was a poor forward projection. |
| 7 | Watkins | FWD | Aston Villa | 8 | Proven starting forward with strong scarcity value. |
| 8 | Gabriel | DEF | Arsenal | 3 | Still an exceptional defender, but no longer placed ahead of the strongest healthy attackers by default. |

See [[01 Current/Current Draft Board]] and [[07 Changes/2026/08/2026-08-01/1848-AEST-changes]].

## Official FPL reconciliation

The official endpoints returned:

| Item | Previous review | Current review | Change |
|---|---:|---:|---:|
| Players | 564 | 564 | 0 |
| Teams | 20 | 20 | 0 |
| Fixtures | 380 | 380 | 0 |
| Published board rows | 220 | 220 | 0 |
| Reviewed top rows | Baseline only | 80 | +80 manually assessed |
| Missing reviewed FPL IDs | 0 | 0 | 0 |

Sources:

- [Official FPL bootstrap-static endpoint](https://fantasy.premierleague.com/api/bootstrap-static/)
- [Official FPL fixtures endpoint](https://fantasy.premierleague.com/api/fixtures/)
- [[09 Data/2026-08-01-1848-official-api-snapshot]]

The official FPL ID remains the stable player key. Team, position and availability are refreshed from the API rather than retained from secondary sources.

## Method correction

### What was wrong with the first ordering

The first review used an external board as a quantitative starting point and correctly labelled it provisional. Further inspection found that a prominent draft board page was not a true 2026/27 projection at this point in preseason. It stated:

- every player was ranked by last season's real points;
- live 2026/27 ranks would arrive in August;
- the displayed table was primarily a comparison between prior FPL rank and prior actual finish.

Source: [Waiver FPL draft board](https://waiverfpl.com/draft).

This creates predictable errors:

- players returning from injury are suppressed;
- players changing clubs or roles are evaluated in their old environment;
- high prior-season defensive-contribution scorers are elevated even when their new role is uncertain;
- new tactical structures and departures are ignored;
- goalkeeper and defender points can crowd out higher-upside attackers without considering replacement level.

### Replacement method

The top 80 were manually ordered using:

1. official FPL identity, position and availability;
2. expected starting role and minutes;
3. penalties, corners and central attacking role;
4. current team and manager context;
5. injury and transfer uncertainty;
6. preseason role and form, weighted more heavily than raw friendly goals;
7. opening fixture environment;
8. positional scarcity and replacement level in an eight-manager draft;
9. source reliability and independence.

The reviewed order is stored as official FPL IDs in `scripts/apply_top80_source_review.py`. Ranks 81–220 retain their previous relative order unless displaced by the top-80 correction or changed official metadata. This is transparent technical debt for the next review, not a claim that all 220 positions are now equally validated.

## Material risers

### Alexander Isak: 96 → 4

The first rank primarily reflected an injury-hit 2025/26 total. Official Premier League analysis notes:

- his 2024/25 Newcastle season produced 23 goals, six assists and 211 points;
- Hugo Ekitiké has a long-term injury;
- Isak should have a clearer centre-forward route under Andoni Iraola;
- he may take penalties after Mohamed Salah's departure.

Source: [Premier League key-player analysis](https://www.premierleague.com/en/news/4680821/the-scouts-analysis-of-15-key-player-prices-in-202627-fantasy).

This is the largest justified early-round correction. The fourth rank still assumes adequate fitness and should fall if preseason availability is weak.

### Cody Gakpo: 101 → 24

The first model treated his prior total as the principal signal. Liverpool's post-Salah attack, new manager and strong early team investment case increase the value of likely attacking starters. Gakpo's exact role is less secure than Isak or Wirtz, so he remains outside the first three rounds.

Sources:

- [Premier League Liverpool investment analysis](https://www.premierleague.com/en/news/4676404/best-teams-to-invest-in-for-202627-fantasy-liverpool)
- [Official FPL API](https://fantasy.premierleague.com/api/bootstrap-static/)

### Florian Wirtz: 77 → 15

Official-panel evidence expects Wirtz to become increasingly important after Salah's departure. Preseason evidence also placed him behind the striker. This is a stronger forward-looking role signal than his first-season total.

Sources:

- [Premier League expert panel](https://www.premierleague.com/en/news/4672877/fpl-experts-price-predictions-for-202627)
- [FFScout preseason roundup](https://www.fantasyfootballscout.co.uk/2026/07/31/fpl-pre-season-tavernier-impresses-muharemovic-class-szoboszlai-deeper)

### Phil Foden: 66 → 23

Foden's prior rank was too low for his ceiling, but Manchester City's depth prevents a more aggressive promotion. The new rank reflects high upside with a major rotation discount.

Evidence type: informed inference from the current official squad and [[05 Sources/X Source Graph]].

### Marcus Tavernier: 61 → 27

Tavernier produced a goal and assist after assisting in the previous friendly. His role and repeated returns are more informative than one isolated friendly event. He is not promoted further because Bournemouth have the hardest opening six fixtures by official FDR.

Sources:

- [FFScout preseason roundup](https://www.fantasyfootballscout.co.uk/2026/07/31/fpl-pre-season-tavernier-impresses-muharemovic-class-szoboszlai-deeper)
- [Premier League FDR](https://www.premierleague.com/en/news/4675493/get-the-fixture-difficulty-ratings-for-202627-fpl-season)

### Cole Palmer: 35 → 6

Palmer's 114-point 2025/26 season was a weak predictor of his broader ceiling. Official analysis highlights:

- back-to-back 200+ point seasons before 2025/26;
- a previous 22-goal, 13-assist campaign;
- summer rest;
- no European football for Chelsea, lowering rotation pressure.

Source: [Premier League key-player analysis](https://www.premierleague.com/en/news/4680821/the-scouts-analysis-of-15-key-player-prices-in-202627-fantasy).

Chelsea's crowded attack stops Palmer from ranking above the top five at this stage.

### Matheus Cunha: 38 → 12 and Bryan Mbeumo: 29 → 11

Manchester United face only one opponent rated above FDR 3 in their first eight fixtures. Both receive a schedule and team-role promotion, although their relative share of returns remains uncertain behind Bruno Fernandes.

Sources:

- [Premier League FDR](https://www.premierleague.com/en/news/4675493/get-the-fixture-difficulty-ratings-for-202627-fpl-season)
- [Premier League opening-player analysis](https://www.premierleague.com/en/news/4675553/why-fernandes-and-haaland-look-like-must-haves-to-start-202627-fpl)

### Bukayo Saka: 11 → 3

The prior ordering over-weighted an injury-affected season. Premier League tactical analysis found Arsenal's win rate rose from 53.8 per cent without Saka in the matchday squad to 71.7 per cent when he featured, and described his central role in chance creation and the Gyökeres partnership.

Source: [Premier League Saka analysis](https://www.premierleague.com/en/news/4650977/just-how-important-is-saka-to-arsenal).

The third rank is an informed season-outlook inference rather than a claim that recent points exceeded Gabriel's.

## Material fallers

### Gabriel: 3 → 8

Gabriel remains a first-round selection. His 209 points, 18 clean sheets, set-piece threat and defensive-contribution routes support an elite defender rank. The change is cross-position, not a negative reassessment of Gabriel: elite healthy attackers and scarce forwards should not be suppressed solely by a prior-season points table.

Source: [Premier League key-player analysis](https://www.premierleague.com/en/news/4680821/the-scouts-analysis-of-15-key-player-prices-in-202627-fantasy).

### João Pedro: 4 → 10

His production and forward classification remain attractive. The first ranking assumed too much certainty within a Chelsea attack containing Palmer, Rogers and multiple central/wide options. The revised position retains first-two-round value while applying a competition discount.

Sources:

- [Official FPL API](https://fantasy.premierleague.com/api/bootstrap-static/)
- [Reuters on Rogers and Palmer](https://www.reuters.com/sports/soccer/rogers-palmer-combination-key-chelsea-revival-says-alonso-2026-07-27/)

### Antoine Semenyo: 6 → 13

Moving to Manchester City raises team ceiling but lowers expected-minutes certainty. The first rank treated the club change as almost entirely positive. The revised rank preserves first-two-round upside but discounts competition with Foden, Cherki, Doku, Marmoush and others.

Sources:

- [Official FPL API](https://fantasy.premierleague.com/api/bootstrap-static/)
- [Fabrizio Romano post concerning Semenyo and Cherki](https://x.com/FabrizioRomano/status/2040816965942390893)

### Bruno Guimarães: 7 → 17

His secure Newcastle minutes remain valuable, but the first ranking was inflated by prior points and defensive contributions relative to more attacking options. No new high-confidence transfer event was found in this short interval.

Evidence type: informed cross-position correction; transfer status remains on [[01 Current/Current Watchlist]].

### Declan Rice: 10 → 19

Rice remains a strong all-round asset, but Saka, Palmer, Wirtz, Mbeumo, Cunha and scarce forwards have greater attacking ceilings. This is another correction of prior-season outcome bias rather than a negative role event.

### Nico O'Reilly: 14 → 40; Marcos Senesi: 15 → 41; Mukiele: 16 → 69

These defenders were elevated by prior points and/or defensive contribution without sufficient current-role certainty. Manchester City rotation and Tottenham role changes require substantial discounts. Mukiele remains draftable but no longer receives an early-round placement based mainly on a prior-season output environment.

Sources:

- [Official FPL API](https://fantasy.premierleague.com/api/bootstrap-static/)
- [Premier League expert panel](https://www.premierleague.com/en/news/4672877/fpl-experts-price-predictions-for-202627)

## Position-specific conclusions

See [[04 Positions/2026-27 Top-80 Correction]].

### Forwards

Forward scarcity remains real. Isak, Thiago, Watkins, João Pedro and Gyökeres all move or remain above many defenders and defensive midfielders. Uncertain starters are not promoted purely because of classification.

### Midfielders

The position is deep, but the elite attacking roles are not replaceable. Bruno, Saka, Palmer, Mbeumo, Cunha and Wirtz should not sit behind numerous prior-season defensive-contribution scorers.

### Defenders

Gabriel remains exceptional. The rest of the defender pool is more replaceable and contains greater role uncertainty than the first board suggested.

### Goalkeepers

No goalkeeper appears inside the top 72. In an eight-manager league, the position can usually be delayed because 16 drafted goalkeepers still leave several starters undrafted.

## Preseason evidence

Evidence retained from the 31 July roundup:

- Tavernier has consecutive attacking returns.
- Evanilson scored his first preseason goal.
- Kroupi underwent foot surgery.
- Kroupi's absence may create a No. 10 opportunity for Kluivert.
- Wirtz was used behind the striker.
- Szoboszlai was used deeper but continued to return.
- Joe Gomez sustained a muscle injury.

Source: [FFScout preseason roundup](https://www.fantasyfootballscout.co.uk/2026/07/31/fpl-pre-season-tavernier-impresses-muharemovic-class-szoboszlai-deeper).

The Fantasy Football Scout preseason hub was also inspected as a club-by-club index. It is a useful navigation source, but individual role claims should cite the underlying friendly note rather than the hub alone.

Source: [FFScout 2026/27 preseason guide](https://www.fantasyfootballscout.co.uk/fpl-2026-27-the-ultimate-pre-season-guide-tips-more).

## Injury validation

The generated board was checked against current official FPL news.

A validation pass found Kaoru Mitoma listed with a hamstring injury and unknown return date. He was removed from the reviewed top 80 and replaced by available Brighton forward Danny Welbeck at rank 54. This prevents reputation from overriding current availability metadata.

Source: [Official FPL API](https://fantasy.premierleague.com/api/bootstrap-static/).

Other active flags include Saliba, Timber, Šeško and several players below the top 80. The API flag is authoritative for board status, but a precise medical prognosis requires club or reliable reporter evidence.

## X and public-source network review

The user requested research beyond the named accounts into their following and citation networks.

### Planet FPL

Publicly indexed Planet FPL material confirmed James Linden, Suj and the wider correspondent network. It did not expose a sufficiently current and detailed James player ranking during this run. No player was moved on an invented Planet FPL view.

The network remains a high-priority discovery source, particularly for club correspondents and manager tendencies.

### Official expert panel expansion

The Premier League expert panel added the following inspectable accounts to the source graph:

- Pras — `@PrasFPL`
- Utkarsh Dalmia — `@ZopharFPL`
- Lee and Sam Bonfield — `@FPLFamily`
- Pranil Sheth — `@Lateriser12`
- Ben Crabtree — `@FC_Crabdogg`
- Az Phillips — `@FPLBlackbox`
- Tom Johnson — `@FFScout_Tom`
- The FPL Wire — `@TheFPLWire`, connecting Lateriser, Zophar and Pras

Source: [Premier League expert panel](https://www.premierleague.com/en/news/4672877/fpl-experts-price-predictions-for-202627).

The panel supplied concise information aligned with the user's preference:

- Bruno: attacking role, penalties and corners.
- Palmer: rest and no European football.
- Thiago: nailed starter, penalties and talisman role.
- Wirtz: increased importance after Salah.
- Anderson: defensive-contribution strength, but now at Manchester City.
- Gabriel: exceptional prior output.
- Kroupi: uncertain minutes even before the surgery evidence.
- Muñoz: potential loss of wing-back attacking role.

### FML FPL

The launch episode discussed Arsenal, Brentford, Chelsea, Liverpool, Manchester City, Spurs and numerous players. Its stated lack of enthusiasm for Thiago was retained as dissenting draft-community opinion, but it did not outweigh his official production, role and penalty evidence.

Source: [FML FPL preseason launch](https://podcasts.apple.com/us/podcast/fpl-is-back-2026-27-fpl-preseason-launch/id1024068765?i=1000778160164).

### Fabrizio Romano and transfers

No newly indexed high-confidence Fabrizio Romano development between the 17:38 and 18:48 reviews justified a transfer-specific board change. Existing club changes were incorporated through the official FPL player pool and prior cited reporting.

This is an important no-change conclusion: the review did not manufacture transfer movement simply because transfer monitoring was requested.

### Following-list limitation

Public X pages do not expose a complete, reliable following graph. This run inspected accounts discovered through official panels, podcast networks, citations and indexed profiles. A followed account is treated as a candidate source, not an endorsed authority.

See [[05 Sources/X Source Graph]].

## Evidence considered but not adopted

- The exact 2025/26 points order was rejected as a 2026/27 draft sequence.
- FML FPL's limited enthusiasm for Thiago was not adopted over stronger role and production evidence.
- A transfer to Manchester City was not treated as an automatic rise; Semenyo and Anderson received rotation discounts.
- Friendly goals and assists were not treated as sufficient without role/minutes context.
- Mitoma's name recognition was not used to ignore an unknown-return injury flag.
- Price was not used as a Draft value constraint; it was used only as a signal of official or expert expectation.
- Public follower counts were not used as reliability scores.
- Multiple experts appearing on the same podcast or repeating the same report were not treated as independent corroboration.

## Important unchanged conclusions

- Haaland remains first.
- Bruno Fernandes remains second.
- Igor Thiago remains fifth.
- Watkins remains inside the first round.
- Goalkeepers remain delayable.
- Kroupi remains outside the drafted 160 pending recovery clarity.
- Manchester City and Chelsea remain the largest high-upside rotation problems.

## Reproducibility

The branch adds `scripts/apply_top80_source_review.py`, which:

- fetches current official FPL player and fixture data;
- applies the reviewed top 80 using stable FPL IDs;
- preserves the remaining prior relative order;
- refreshes official team, position and availability metadata;
- records old/new ranks in a machine-readable movement file;
- writes the canonical board and API snapshot.

Generated records:

- [[09 Data/2026-08-01-1848-official-api-snapshot]]
- `vault/09 Data/2026-08-01-1848-top80-movements.json`

## Remaining weaknesses

- Ranks 81–160 have not yet received the same source-by-source correction.
- Public X following-list coverage remains partial.
- Many teams have not played enough strongest-XI preseason minutes to settle roles.
- Manchester City and Chelsea assets can still move by multiple rounds.
- The top 80 are an informed board, not a projection model with calibrated expected points.
- No personalised pick sequence is possible until the user's draft slot is known.

## Next review priorities

1. Manually correct ranks 81–160 and the drafted/undrafted boundary.
2. Expand club-correspondent coverage for all 20 teams through the Planet FPL network and discovered accounts.
3. Verify Manchester City and Chelsea strongest-XI patterns.
4. Track Isak fitness, penalties and Liverpool's front four.
5. Track Arsenal injuries and set pieces among Saka, Gyökeres, Eze, Ødegaard and Rice.
6. Verify goalkeeper hierarchies without allowing a goalkeeper run to distort the overall board.
7. Track every material transfer through official announcements and confidence-weighted Fabrizio Romano reporting.

## Conclusion

This review materially improves the board because it fixes the source of the first ordering error rather than merely making cosmetic moves. The top 16 are now substantially more plausible for a Draft setting. Confidence remains lower from ranks 17–80, and ranks 81–160 are the correct target for the next iteration.

Backlinks: [[01 Current/Current Draft Board]], [[01 Current/Current Watchlist]], [[04 Positions/2026-27 Top-80 Correction]], [[05 Sources/X Source Graph]], [[07 Changes/2026/08/2026-08-01/1848-AEST-changes]].
