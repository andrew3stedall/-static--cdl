---
type: source_graph
platform: X
last_reviewed: 2026-08-01T17:38:00+10:00
coverage: partial_public_index
---

# X Source Graph

## Purpose

Build a high-signal discovery network rather than repeatedly searching only a fixed list of large FPL creators. The graph begins with trusted seed accounts and expands through accounts they cite, mention, repost, interview or use as club correspondents.

A follow, mention or repost is a **discovery edge**, not evidence that the linked account is accurate.

## Seed accounts

| Account | Handle | Primary use | Treatment |
|---|---|---|---|
| Planet FPL | [@PlanetFPLPod](https://x.com/PlanetFPLPod) | Tactical discussion, club correspondents, manager tendencies | Preferred high-signal seed; extract underlying facts and James's judgement separately. |
| James Richardson / Planet FPL network | Planet FPL ecosystem | Broad club knowledge and correspondent discovery | High-value discovery node; do not assume every contributor is equally reliable. |
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

## Discovery procedure

For every seed account:

1. inspect publicly indexed recent posts and replies;
2. record accounts repeatedly cited, interviewed, mentioned or reposted;
3. classify discovered accounts as official, club correspondent, tactical analyst, fan observer, injury specialist, transfer reporter, fixture specialist, statistical model or aggregator;
4. inspect the discovered account directly before relying on it;
5. save the exact material post URL and timestamp;
6. identify whether multiple posts originate from the same underlying report;
7. add high-value club-specific accounts to the active graph.

## Reliability rules

- Official club statements and direct manager comments outrank commentary.
- Club correspondents are evaluated by club and topic; reliability is not universal.
- Fan accounts can reveal tactical observations or likely line-ups but need corroboration for material ranking moves.
- Aggregators do not create independent corroboration.
- Follower count is not a reliability score.
- Accounts followed by a trusted seed are candidates for inspection, not automatically trusted sources.
- A creator's opinion and the factual inputs behind it are recorded separately.

## Current material post

| Source | Post | Affected entities | Use |
|---|---|---|---|
| Fabrizio Romano | [Semenyo commenting on Cherki at Manchester City](https://x.com/FabrizioRomano/status/2040816965942390893) | Semenyo, Cherki, Manchester City | Early integration signal only; not proof of starting security. |

## Public-access limitation

The public web does not provide a complete, dependable export of every seed account's full following list. X pages may be inaccessible, stale, partially indexed or expose only profile metadata. Consequently:

- this file does not claim exhaustive network coverage;
- accounts are added only when actually discovered through public evidence;
- inaccessible follow relationships are recorded as unavailable rather than guessed;
- future runs should expand the graph incrementally and preserve discovery provenance.

## Next expansion priorities

- Planet FPL's club correspondent network across all 20 clubs.
- Accounts repeatedly cited by James for tactical or manager-role information.
- Reliable local reporters for Manchester City, Chelsea, Liverpool, Arsenal and promoted clubs.
- Goalkeeper hierarchy specialists.
- Injury reporters and direct training-ground sources.
- Concise Draft-specific accounts that focus on role and minutes rather than price.
