---
type: source_graph
platform: X
last_reviewed: 2026-08-01T18:48:00+10:00
coverage: partial_public_index
---

# X Source Graph

## Purpose

Build a high-signal discovery network rather than repeatedly searching only a fixed list of large FPL creators. The graph begins with trusted seed accounts and expands through accounts they follow, cite, mention, repost, interview or use as club correspondents.

A follow, mention or repost is a **discovery edge**, not evidence that the linked account is accurate.

## Seed accounts

| Account | Handle | Primary use | Treatment |
|---|---|---|---|
| Planet FPL | [@PlanetFPLPod](https://x.com/PlanetFPLPod) | Tactical discussion, club correspondents, manager tendencies | Preferred high-signal seed; extract underlying facts and James's judgement separately. |
| James Linden / Planet FPL network | [Planet FPL podcast listing](https://podcasts.apple.com/au/podcast/planet-fpl-the-fantasy-football-podcast/id1280497332) | Broad club knowledge and correspondent discovery | High-value discovery node; do not assume every contributor is equally reliable. |
| Suj | [@sujanshah](https://x.com/sujanshah) | Planet FPL discussion and West Ham perspective | Supporting seed. |
| Clayton | [@claytsAFC](https://x.com/claytsAFC) | Arsenal and Planet FPL network | Supporting seed. |
| Planet FPL Hunter | [@PlanetFPLHunter](https://x.com/PlanetFPLHunter) | Planet FPL network | Supporting seed. |
| Ben Crellin | [@BenCrellin](https://x.com/BenCrellin) | Fixture structure, postponements, blanks and doubles | High authority for fixture mechanics; not used as a universal player ranker. |
| Fabrizio Romano | [@FabrizioRomano](https://x.com/FabrizioRomano) | Transfer probability and squad knock-on effects | Confidence-weighted; exact post wording retained. |
| Official FPL | [@OfficialFPL](https://x.com/OfficialFPL) | Official game announcements and scoring | Authoritative for game rules, not team football news. |
| FPL Status | [@FPLStatus](https://x.com/FPLStatus) | Official scoring and status aggregation | Useful verification layer; trace back to official source. |
| FPL Draft | [@FplDraft](https://x.com/FplDraft) | Draft-specific discussion | Discovery and consensus check. |
| FML FPL | [@FMLFPL](https://x.com/FMLFPL) | Draft-specific strategy and player discussion | Useful counterweight to classic-game creators. |
| Rob T | [@robtFPL](https://x.com/robtFPL) | Draft/FPL analysis and source discovery | Secondary analytical node. |
| FPL Marcello | [@FPL_Marcello](https://x.com/FPL_Marcello) | FPL data and discussion | Secondary discovery node. |
| disFPL | [@dis_fpl](https://x.com/dis_fpl) | FPL information | Secondary discovery node. |
| FPL Osama | [@FPLOsama](https://x.com/FPLOsama) | FPL information | Secondary discovery node. |
| FPL Gameweek | [@FPLGameweek](https://x.com/FPLGameweek) | News and discussion | Secondary discovery node. |
| FPL Form | [@fplform](https://x.com/fplform) | Form/data discussion | Secondary model check. |

## Accounts added through the official expert network

The Premier League's 2026/27 expert panel provided a reliable discovery route into several established analysts. The panel article is evidence that these accounts were consulted by the official game; it does not make every future opinion authoritative.

| Account/person | Handle | Strength exposed by source | Current use |
|---|---|---|---|
| Pras | [@PrasFPL](https://x.com/PrasFPL) | Broad elite-player and team uncertainty assessment | Context and consensus; inspect underlying facts. |
| Utkarsh Dalmia / Zophar | [@ZopharFPL](https://x.com/ZopharFPL) | Role, penalties and set pieces | Bruno Fernandes role evidence and wider tactical discovery. |
| Lee and Sam Bonfield / FPL Family | [@FPLFamily](https://x.com/FPLFamily) | Player workload, role and system importance | Palmer and Wirtz evidence; source-discovery node. |
| Pranil Sheth / Lateriser | [@Lateriser12](https://x.com/Lateriser12) | Talisman roles and tactical upside | Thiago and Muñoz assessment; separate opinion from facts. |
| Ben Crabtree | [@FC_Crabdogg](https://x.com/FC_Crabdogg) | Player expectation and historical performance | Secondary player-value and role context. |
| Az Phillips / FPL BlackBox | [@FPLBlackbox](https://x.com/FPLBlackbox) | Data-led role and defensive-contribution analysis | Anderson and midfield-model checks. |
| Tom Johnson / Fantasy Football Scout | [@FFScout_Tom](https://x.com/FFScout_Tom) | Minutes, role and player-price analysis | Kroupi, Gabriel and broader preseason discovery. |
| The FPL Wire | [@TheFPLWire](https://x.com/TheFPLWire) | Network joining Lateriser, Zophar and Pras | Efficient cross-check of the panel network, not independent corroboration when the same hosts repeat a claim. |

Discovery evidence: [Premier League expert panel](https://www.premierleague.com/en/news/4672877/fpl-experts-price-predictions-for-202627).

## Discovery procedure

For every seed or discovered account:

1. inspect publicly indexed recent posts and replies;
2. inspect the account's public following list when accessible, but record when it is incomplete or blocked;
3. record accounts repeatedly cited, interviewed, mentioned or reposted;
4. classify discovered accounts as official, club correspondent, tactical analyst, fan observer, injury specialist, transfer reporter, fixture specialist, statistical model or aggregator;
5. inspect the discovered account directly before relying on it;
6. save the exact material post URL and timestamp;
7. identify whether multiple posts originate from the same underlying report;
8. add high-value club-specific accounts to the active graph.

## Reliability rules

- Official club statements and direct manager comments outrank commentary.
- Club correspondents are evaluated by club and topic; reliability is not universal.
- Fan accounts can reveal tactical observations or likely line-ups but need corroboration for material ranking moves.
- Aggregators do not create independent corroboration.
- Follower count is not a reliability score.
- Accounts followed by a trusted seed are candidates for inspection, not automatically trusted sources.
- A creator's opinion and the factual inputs behind it are recorded separately.
- Multiple accounts from the same podcast or panel are not treated as independent evidence when repeating the same underlying information.

## Material posts and articles retained

| Source | Evidence | Affected entities | Use |
|---|---|---|---|
| Fabrizio Romano | [Semenyo commenting on Cherki at Manchester City](https://x.com/FabrizioRomano/status/2040816965942390893) | Semenyo, Cherki, Manchester City | Early integration signal only; not proof of starting security. |
| Official PL expert panel | [2026/27 predictions and role comments](https://www.premierleague.com/en/news/4672877/fpl-experts-price-predictions-for-202627) | Bruno, Palmer, Thiago, Wirtz, Anderson, Gabriel, Kroupi, Muñoz | Source-network discovery and role evidence. |
| FML FPL | [2026/27 preseason launch episode](https://podcasts.apple.com/us/podcast/fpl-is-back-2026-27-fpl-preseason-launch/id1024068765?i=1000778160164) | Arsenal, Brentford, Chelsea, Liverpool, City, Spurs and others | Draft-community counterpoint; opinions were not adopted automatically. |

## Findings from this review

- Publicly indexed Planet FPL material confirmed the correspondent-style network but did not expose a sufficiently current, detailed James ranking to move individual players directly.
- The official expert panel materially expanded the analyst network and supplied concise role observations suitable for the user's preference for facts over long explanations.
- FML FPL expressed limited enthusiasm for Thiago, but this was retained as a dissenting opinion rather than used to overrule official production, minutes and penalty-role evidence.
- No newly indexed Fabrizio Romano report between the 17:38 and 18:48 reviews reached the confidence threshold for a transfer-driven ranking change.

## Public-access limitation

The public web does not provide a complete, dependable export of every seed account's full following list. X pages may be inaccessible, stale, partially indexed or expose only profile metadata. Consequently:

- this file does not claim exhaustive network coverage;
- accounts are added only when actually discovered through public evidence;
- inaccessible follow relationships are recorded as unavailable rather than guessed;
- future runs should expand the graph incrementally and preserve discovery provenance.

## Correction history

- 2026-08-01T18:09:00+10:00 — Corrected the Planet FPL host from “James Richardson” to **James Linden** after checking the current Apple Podcasts host listing. See [[07 Changes/2026/08/2026-08-01/1809-AEST-source-name-correction]].

## Next expansion priorities

- Planet FPL's club correspondent network across all 20 clubs.
- Accounts repeatedly cited or followed by James for tactical or manager-role information.
- Reliable local reporters for Manchester City, Chelsea, Liverpool, Arsenal and promoted clubs.
- Goalkeeper hierarchy specialists.
- Injury reporters and direct training-ground sources.
- Concise Draft-specific accounts that focus on role and minutes rather than price.

Backlinks: [[06 Reviews/2026/08/2026-08-01/1848-AEST-review]], [[07 Changes/2026/08/2026-08-01/1848-AEST-changes]].
