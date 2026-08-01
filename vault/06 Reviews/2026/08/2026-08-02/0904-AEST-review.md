---
type: review
timestamp: 2026-08-02T09:04:00+10:00
target_block: remaining API pool
board_depth: 240
---

# FPL Draft review — remaining-player sweep

## API reconciliation

Official FPL endpoints returned 564 active players, 20 teams and 380 fixtures. Stable IDs were preserved and no API-absent player was added.

## Method

Every active player outside the top 220 was screened. The top 220 was not reordered. Price and ownership were used only to make the long-list tractable; additions required plausible first-team relevance, role upside, positional scarcity or clean-sheet potential.

## Added extended buffer

- **221. Kerkez** (DEF, LIV, FPL ID 358) — Available; added to the extended watch buffer, not promoted into the top 220.
- **222. Hall** (DEF, NEW, FPL ID 449) — Available; added to the extended watch buffer, not promoted into the top 220.
- **223. Konsa** (DEF, AVL, FPL ID 31) — Available; added to the extended watch buffer, not promoted into the top 220.
- **224. Spence** (DEF, TOT, FPL ID 505) — Available; added to the extended watch buffer, not promoted into the top 220.
- **225. Shaw** (DEF, MUN, FPL ID 423) — Available; added to the extended watch buffer, not promoted into the top 220.
- **226. Tonali** (MID, TOT, FPL ID 455) — Available; added to the extended watch buffer, not promoted into the top 220.
- **227. van Ewijk** (DEF, COV, FPL ID 175) — Available; added to the extended watch buffer, not promoted into the top 220.
- **228. Diop** (DEF, IPS, FPL ID 259) — Available; added to the extended watch buffer, not promoted into the top 220.
- **229. Mosquera** (DEF, ARS, FPL ID 11) — Available; added to the extended watch buffer, not promoted into the top 220.
- **230. Dubravka** (GKP, TOT, FPL ID 497) — Available; added to the extended watch buffer, not promoted into the top 220.
- **231. Yates** (MID, NFO, FPL ID 489) — Available; added to the extended watch buffer, not promoted into the top 220.
- **232. Hughes** (MID, CRY, FPL ID 212) — Available; added to the extended watch buffer, not promoted into the top 220.
- **233. Kusi-Asare** (FWD, FUL, FPL ID 272) — Available; added to the extended watch buffer, not promoted into the top 220.
- **234. Thomas** (DEF, COV, FPL ID 173) — Available; added to the extended watch buffer, not promoted into the top 220.
- **235. Palmer** (GKP, IPS, FPL ID 301) — Available; added to the extended watch buffer, not promoted into the top 220.
- **236. Petrović** (GKP, BOU, FPL ID 57) — Available; added to the extended watch buffer, not promoted into the top 220.
- **237. Leno** (GKP, FUL, FPL ID 250) — Available; added to the extended watch buffer, not promoted into the top 220.
- **238. Kayode** (DEF, BRE, FPL ID 88) — Available; added to the extended watch buffer, not promoted into the top 220.
- **239. Sánchez** (GKP, CHE, FPL ID 140) — Available; added to the extended watch buffer, not promoted into the top 220.
- **240. Hume** (DEF, SUN, FPL ID 534) — Available; added to the extended watch buffer, not promoted into the top 220.

## Sources

- [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/)
- [Official fixtures](https://fantasy.premierleague.com/api/fixtures/)
- [Premier League preseason tracker](https://www.premierleague.com/en/news/4606700/premier-league-clubs-2026-pre-season-fixtures-and-results)

## Decision

These are useful watch cases, but none had enough current role evidence to displace rank 220. Confirmed starts, penalties, set pieces, repeated preseason role, manager comments, transfers or competitor injuries can trigger promotion.
