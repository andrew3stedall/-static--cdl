---
type: review
reviewed_at: 2026-08-01T17:38:00+10:00
baseline: none
branch: codex/fpl-review-20260801-1738-initial-board
status: provisional_initial_board
---

# First 2026/27 FPL Draft review

## Scope

This run establishes the first evidence-based player pool and top-220 board for an eight-manager league with 20 selections per manager. It is an initial baseline, not a claim that the exact ordering is mature.

The review prioritised:

1. official FPL identity, team, position, availability and fixtures;
2. a complete draft-scarcity ordering deep enough for 160 selections;
3. current transfers and preseason role evidence;
4. the first public-X source graph for future iterations;
5. explicit documentation of weaknesses and rejected conclusions.

## Official FPL reconciliation

The official endpoints returned:

| Item | Count |
|---|---:|
| Players | 564 |
| Teams | 20 |
| Fixtures | 380 |
| External draft rows matched to official FPL IDs | 240/240 |
| Rows published to the current board | 220 |

Sources:

- [Official FPL bootstrap-static endpoint](https://fantasy.premierleague.com/api/bootstrap-static/)
- [Official FPL fixtures endpoint](https://fantasy.premierleague.com/api/fixtures/)
- [[09 Data/2026-08-01-official-api-snapshot]]

The official FPL ID is retained as the stable player key. There were no unresolved mappings.

## Ranking construction

The live [Draft Fantasy cheat sheet](https://www.draftfantasy.com/fpl/draft-cheat-sheet) supplied the initial quantitative scarcity order. It was joined to the official FPL pool by team, position and player identity. The resulting board is stored at [[01 Current/Current Draft Board]].

The external board is useful because it explicitly models value above replacement and provides more than the 160 players required by this league. It is not accepted as authoritative. The following weaknesses were found:

- defenders and defensive-contribution profiles appear unusually aggressive at the top of the order;
- several low-ceiling midfielders rank above established attacking players;
- backup goalkeepers were materially overvalued when starting status was unresolved;
- exact rankings depend heavily on the model's season projections, which are not independently reproducible from the page;
- transfer and tactical uncertainty is sometimes treated as settled.

The generator therefore demoted presumed backup goalkeepers. Other questionable rankings remain visible but are labelled provisional so later evidence can move them transparently rather than silently replacing the baseline.

## Initial top tier

| Rank | Player | Position | Team | Assessment |
|---:|---|---|---|---|
| 1 | Haaland | FWD | Manchester City | Clear elite ceiling and scarce forward profile. |
| 2 | Bruno Fernandes | MID | Manchester United | High-minute, central attacking and set-piece role. |
| 3 | Gabriel | DEF | Arsenal | Model strongly rewards elite defence and defensive contributions; exact rank is low confidence. |
| 4 | João Pedro | FWD | Chelsea | Strong projected role, but competition and Chelsea's new structure require monitoring. |
| 5 | Igor Thiago | FWD | Brentford | Scarce starting-forward profile; needs preseason role confirmation. |
| 6 | Semenyo | MID | Manchester City | Team upgrade increases ceiling, but City rotation materially lowers confidence. |
| 7 | Bruno Guimarães | MID | Newcastle | Strong durable minutes profile; transfer reporting remains a watch item. |
| 8 | Watkins | FWD | Aston Villa | Proven starting forward; early baseline remains strong. |

Critical judgement: the numerical order from ranks 3–8 should not yet be treated as a recommended first-round sequence. Haaland and Bruno Fernandes are the two clearest initial anchors. The remainder require more source-specific review.

## Transfer and role evidence

### Morgan Rogers

The official FPL pool lists Rogers at Chelsea. Reuters reported that Chelsea bought him from Aston Villa and quoted Xabi Alonso describing a plan for Rogers and Palmer to link together. This is positive evidence for attacking involvement, but Chelsea's crowded attacking squad creates uncertainty over exact position, set pieces and minutes.

- [Reuters: Rogers and Palmer combination key to Chelsea revival](https://www.reuters.com/sports/soccer/rogers-palmer-combination-key-chelsea-revival-says-alonso-2026-07-27/)
- [Official FPL bootstrap-static endpoint](https://fantasy.premierleague.com/api/bootstrap-static/)

### Manchester City additions

The official FPL pool currently lists Antoine Semenyo and Elliot Anderson at Manchester City. The moves increase team-strength upside but also introduce Guardiola rotation risk. Neither player should automatically rise solely because of the club change.

Fabrizio Romano's public post showed Semenyo praising Rayan Cherki after joining City. This supports early integration but is not evidence of secure league minutes.

- [Fabrizio Romano post concerning Semenyo and Cherki](https://x.com/FabrizioRomano/status/2040816965942390893)
- [Official FPL bootstrap-static endpoint](https://fantasy.premierleague.com/api/bootstrap-static/)

## Preseason evidence considered

Fantasy Football Scout's 31 July roundup supplied the most concentrated current role and injury evidence:

- Marcus Tavernier recorded a goal and assist after assisting in the prior friendly.
- Evanilson scored his first preseason goal.
- Alex Tóth and Ben Gannon-Doak produced another attacking return.
- Eli Junior Kroupi underwent foot surgery and faces time out.
- Kroupi's absence may increase Justin Kluivert's opportunities as a No. 10.
- Liverpool used Florian Wirtz behind the striker.
- Dominik Szoboszlai was used deeper but continued to return.
- Joe Gomez sustained a muscle injury, increasing concern about Liverpool centre-back depth.
- Jaka Bijol had a knee injury concern.
- Brian Brobbey's short appearance was planned rather than an injury withdrawal.

Source: [Fantasy Football Scout preseason roundup, 31 July 2026](https://www.fantasyfootballscout.co.uk/2026/07/31/fpl-pre-season-tavernier-impresses-muharemovic-class-szoboszlai-deeper)

Ranking treatment:

- Kroupi is retained only in the undrafted buffer with an injury flag.
- Tavernier, Kluivert, Wirtz and Szoboszlai are positive watch items, but isolated friendlies did not justify large manual jumps in this baseline.
- Liverpool defensive assets carry an additional depth/availability caveat.

## X source graph

The user requested that research extend beyond named creators into the accounts they follow, cite or amplify. The first source graph is stored at [[05 Sources/X Source Graph]].

Seed accounts include:

- Planet FPL / James;
- Ben Crellin;
- Fabrizio Romano;
- Sam Martin and concise FPL information accounts where publicly discoverable;
- Official FPL;
- Draft-specific communities;
- club correspondents and informed supporter accounts discovered through mentions, reposts and repeated citations.

Important limitation: public web indexing does not expose a complete, reliable export of every account's following list. This run therefore does **not** claim exhaustive coverage. It records accounts actually inspected and discovery links, then expands breadth iteratively.

## Sources searched but not fully usable

- X following lists: incomplete without authenticated/API access; public indexing exposes profiles, posts and some network clues but not a dependable full graph.
- Some X posts: indexed without readable body text.
- Planet FPL current detailed opinions: the public podcast catalogue established the correspondent network, but this run did not extract a complete current ranking from James.
- Ben Crellin: profile and fixture-specialist role were confirmed, but no material fixture distortion was applied because the full league schedule is already present and there are no blank/double-gameweek effects before the season.
- The official FPL Draft interface was in seasonal update state, so the standard FPL API supplied the authoritative player identity layer.

## Evidence considered but not adopted

- A transfer to a stronger club was **not** treated as an automatic promotion because rotation can offset team strength.
- Preseason goals or assists against weak opposition were **not** treated as sufficient for major ranking movement.
- Draft Fantasy's exact ordering was **not** treated as consensus or expert truth.
- Social engagement, follower count and repeated aggregator reposts were **not** treated as corroboration.
- Vague transfer interest was not used to move players.

## Position and scarcity observations

- Forward scarcity is real in an eight-manager league, but uncertain starters should not be elevated solely because they are classified as forwards.
- Goalkeepers are deep enough that backup goalkeepers should generally remain outside the drafted 160.
- Elite defenders gain importance under defensive-contribution scoring, but the initial model may overstate the gap over high-ceiling attackers.
- Midfield is deepest in raw numbers, making secure role, penalties and attacking centrality more important than name recognition.

See [[04 Positions/2026-27 Initial Scarcity]].

## Current watchlist priorities

1. Correct the top 80 using the expanded source graph and club-specific role evidence.
2. Verify starting goalkeeper hierarchies.
3. Confirm Manchester City rotation and roles for Semenyo, Anderson, Cherki and Foden.
4. Confirm Chelsea's attacking hierarchy around Palmer, Rogers, João Pedro, Delap and other forwards.
5. Track Kroupi's recovery and Bournemouth's No. 10 structure.
6. Track Liverpool centre-back availability and Wirtz's role.
7. Resolve Arsenal injury flags for Saliba, Timber and White.
8. Monitor Bruno Guimarães transfer reporting, but do not move him on weak links.

## Method and reproducibility

The branch adds `scripts/build_initial_board.py`, which fetches current official FPL data, maps the draft model to stable IDs and writes the canonical board and API snapshot. This prevents the first 220-row ordering from becoming an untraceable manual artefact.

## Conclusion

The first review successfully establishes a complete, API-linked baseline and documents its limitations. The most important finding is not the precise ranking at every position; it is that the current external model must be corrected with tactical, role, transfer and club-source evidence before the top rounds are considered reliable.

The next iteration should concentrate on source-graph expansion and manual review of the top 80 rather than generating another wholesale ranking from scratch.
