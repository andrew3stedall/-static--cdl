---
type: changes
changed_at: 2026-08-01T17:38:00+10:00
prior_review: "[[06 Reviews/2026/08/2026-08-01/1254-AEST-repository-foundation]]"
current_review: "[[06 Reviews/2026/08/2026-08-01/1738-AEST-review]]"
---

# Changes — first FPL Draft board

## Summary

This is the first player-ranking iteration, so there is no prior player order to compare. The principal change is from an empty canonical board to a complete, provisional top-220 board linked to official FPL IDs.

| Change | Previous | Current | Reason | Confidence | Evidence |
|---|---|---|---|---|---|
| Player pool | Not reconciled | 564 players, 20 teams | First official API retrieval | Confirmed | [FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/) |
| Fixtures | Not reconciled | 380 fixtures | First official fixtures retrieval | Confirmed | [FPL fixtures](https://fantasy.premierleague.com/api/fixtures/) |
| Draft board | Empty | 220 ranked players | Establish baseline beyond the 160 drafted players | Strong baseline, low exact-rank confidence | [[01 Current/Current Draft Board]] |
| Stable identity | None | Every row has an official FPL ID | Prevent name/team ambiguity | Confirmed | [[09 Data/2026-08-01-official-api-snapshot]] |
| Goalkeeper treatment | No rule applied | Presumed backups demoted | External model overvalued uncertain backups | Informed inference | [[06 Reviews/2026/08/2026-08-01/1738-AEST-review]] |
| Source collection | Named seed accounts only | Source-graph approach adopted | Expand into cited/followed club and FPL accounts | Confirmed method change | [[05 Sources/X Source Graph]] |

## Initial franchise segment

| New rank | Player | Position | Team | Confidence | Important caveat |
|---:|---|---|---|---|---|
| 1 | Haaland | FWD | Manchester City | High | None material at this stage. |
| 2 | Bruno Fernandes | MID | Manchester United | High | Confirm final tactical role and penalties in preseason. |
| 3 | Gabriel | DEF | Arsenal | Low | External scarcity model may overstate elite-defender value. |
| 4 | João Pedro | FWD | Chelsea | Medium-low | Crowded attack and new-manager role uncertainty. |
| 5 | Igor Thiago | FWD | Brentford | Medium | Starting role and preseason fitness need confirmation. |
| 6 | Semenyo | MID | Manchester City | Medium-low | Major rotation risk despite team upside. |
| 7 | Bruno Guimarães | MID | Newcastle | Medium | Monitor transfer reporting; ignore weak links. |
| 8 | Watkins | FWD | Aston Villa | High | Verify team role after Rogers' departure. |

## Material preseason and availability items

| Player/team | Change | Board effect this run | Next trigger | Evidence |
|---|---|---|---|---|
| Eli Junior Kroupi | Foot surgery confirmed | Retained only in undrafted buffer with injury flag | Return-to-training date | [FFScout roundup](https://www.fantasyfootballscout.co.uk/2026/07/31/fpl-pre-season-tavernier-impresses-muharemovic-class-szoboszlai-deeper) |
| Marcus Tavernier | Consecutive preseason returns | Positive watch item; no large manual jump | Starts with probable first XI | [FFScout roundup](https://www.fantasyfootballscout.co.uk/2026/07/31/fpl-pre-season-tavernier-impresses-muharemovic-class-szoboszlai-deeper) |
| Justin Kluivert | Possible No. 10 opportunity after Kroupi injury | Positive watch item | Repeated central starts | [FFScout roundup](https://www.fantasyfootballscout.co.uk/2026/07/31/fpl-pre-season-tavernier-impresses-muharemovic-class-szoboszlai-deeper) |
| Florian Wirtz | Used behind Liverpool striker | Positive role signal | Strong-XI repetition and set pieces | [FFScout roundup](https://www.fantasyfootballscout.co.uk/2026/07/31/fpl-pre-season-tavernier-impresses-muharemovic-class-szoboszlai-deeper) |
| Dominik Szoboszlai | Deeper role but continuing returns | Mixed signal; no forced movement | Final midfield structure | [FFScout roundup](https://www.fantasyfootballscout.co.uk/2026/07/31/fpl-pre-season-tavernier-impresses-muharemovic-class-szoboszlai-deeper) |
| Liverpool defence | Joe Gomez muscle injury; thin centre-back depth | Added risk caveat | Gomez/Van Dijk/Jacquet availability | [FFScout roundup](https://www.fantasyfootballscout.co.uk/2026/07/31/fpl-pre-season-tavernier-impresses-muharemovic-class-szoboszlai-deeper) |

## Transfer and role changes

| Player | Current team | Interpretation | Confidence | Evidence |
|---|---|---|---|---|
| Morgan Rogers | Chelsea | Alonso publicly described a plan for Rogers and Palmer to combine; role is promising but attack is crowded. | Strong report | [Reuters](https://www.reuters.com/sports/soccer/rogers-palmer-combination-key-chelsea-revival-says-alonso-2026-07-27/) |
| Antoine Semenyo | Manchester City | Higher team ceiling offset by increased rotation risk. | Confirmed team; role uncertain | [FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/), [Romano post](https://x.com/FabrizioRomano/status/2040816965942390893) |
| Elliot Anderson | Manchester City | Higher team ceiling offset by increased rotation risk. | Confirmed team; role uncertain | [FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/) |

## Important non-movements

- No player received a large discretionary rise solely for one friendly return.
- Manchester City signings were not automatically promoted for moving to a stronger club.
- Bruno Guimarães was not moved on weak transfer links.
- The model's controversial exact top-eight sequence was preserved as a transparent baseline rather than silently rewritten without enough comparative evidence.
- No complete X following graph was claimed because public indexing is incomplete.

## Next-run focus

The next review should manually reassess the top 80 using the expanded source graph, with particular attention to starting security, penalties, central roles and positional replacement value.
