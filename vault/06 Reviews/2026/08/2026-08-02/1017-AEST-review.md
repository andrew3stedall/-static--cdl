---
type: review
timestamp: 2026-08-02T10:17:00+10:00
scope: expand canonical board to 350
---

# FPL Draft review — expand to 350

## API reconciliation

Official FPL returned 564 active players, 20 teams and 380 fixtures. Stable FPL IDs were preserved.

## Method

The manually reviewed top 140 was frozen. Every player absent from the 254-player board was screened using current API identity, position, availability, prior points, minutes and starts. The highest 96 plausible candidates were merged into ranks 141–350, with forward scarcity applied after the raw screening estimate. These placements are provisional and explicitly lower confidence than the pairwise-reviewed top 140.

## Added players

- 146. Berge (MID, FUL)
- 168. Sadiki (MID, SUN)
- 184. C.Jones (MID, LIV)
- 186. Yeremy (MID, CRY)
- 187. Hutchinson (MID, NFO)
- 198. Joelinton (MID, NEW)
- 200. Tel (MID, TOT)
- 202. Ajer (DEF, BRE)
- 203. Gudmundsson (DEF, LEE)
- 204. Reinildo (DEF, SUN)
- 210. Mainoo (MID, MUN)
- 213. Darlow (GKP, MUN)
- 214. Tielemans (MID, MUN)
- 220. Kamada (MID, CRY)
- 222. Lerma (MID, CRY)
- 225. Lukić (MID, FUL)
- 226. Johnson (MID, CRY)
- 228. P.M.Sarr (MID, TOT)
- 231. Iroegbunam (MID, EVE)
- 237. Tanaka (MID, LEE)
- 239. N.Gonzalez (MID, MCI)
- 240. Xavi (MID, TOT)
- 242. Pau (DEF, AVL)
- 245. Danso (DEF, TOT)
- 246. Castagne (DEF, FUL)
- 248. King (MID, FUL)
- 249. Adli (MID, BOU)
- 252. Gray (MID, TOT)
- 253. J.Ramsey (MID, NEW)
- 257. Baleba (MID, BHA)
- 259. Onana (MID, AVL)
- 262. Yoro (DEF, MUN)
- 265. Garnacho (MID, AVL)
- 267. Brooks (MID, BOU)
- 270. Mount (MID, MUN)
- 272. Gruev (MID, LEE)
- 275. Smith (DEF, BOU)
- 276. Maatsen (DEF, AVL)
- 278. Rodrigo (MID, MCI)
- 280. L.Miley (MID, NEW)
- 283. McNeil (MID, EVE)
- 284. Morato (DEF, NFO)
- 285. Longstaff (MID, LEE)
- 287. Robertson (DEF, TOT)
- 291. Barkley (MID, AVL)
- 292. Henry (DEF, BRE)
- 294. Ndoye (MID, NFO)
- 295. Elanga (MID, NEW)
- 296. Martinez (DEF, MUN)
- 299. Mazraoui (DEF, MUN)
- 300. Mings (DEF, AVL)
- 302. Fofana (DEF, CHE)
- 304. Dominguez (MID, NFO)
- 306. Zirkzee (FWD, MUN)
- 308. Bergvall (MID, TOT)
- 310. Kevin (MID, FUL)
- 311. Andrey Santos (MID, MUN)
- 312. Diakité (DEF, BOU)
- 313. Muniz (FWD, FUL)
- 314. Perri (GKP, LEE)
- 315. Savinho (MID, MCI)
- 316. White (DEF, ARS)
- 317. Guessand (MID, AVL)
- 318. Bobb (MID, FUL)
- 319. Ngumoha (MID, LIV)
- 320. Kostoulas (FWD, BHA)
- 321. Heaven (DEF, MUN)
- 322. Bogarde (MID, AVL)
- 323. Cook (MID, BOU)
- 324. Cairney (MID, FUL)
- 325. Willock (MID, NEW)
- 326. J.Cuenca (DEF, FUL)
- 327. Wissa (FWD, NEW)
- 328. Acheampong (DEF, CHE)
- 329. Rigg (MID, SUN)
- 330. Devenny (MID, CRY)
- 331. Hickey (DEF, BRE)
- 332. Mamardashvili (GKP, LIV)
- 333. Röhl (MID, EVE)
- 334. G.Jesus (FWD, ARS)
- 335. Adingra (MID, SUN)
- 336. Enes Ünal (FWD, BOU)
- 337. Chiesa (MID, LIV)
- 338. Tosin (DEF, CHE)
- 339. Udogie (DEF, TOT)
- 340. Lindelöf (DEF, AVL)
- 341. Gnonto (MID, LEE)
- 342. Odobert (MID, TOT)
- 343. Lewis-Skelly (MID, ARS)
- 344. Christie (MID, BOU)
- 345. Alcaraz (MID, EVE)
- 346. De Ligt (DEF, MUN)
- 347. Bakwa (MID, NFO)
- 348. Gittens (MID, CHE)
- 349. Bradley (DEF, LIV)
- 350. O'Nien (DEF, SUN)

## Evidence adopted

Confirmed API identity, team, position, availability, prior points, starts and minutes.

## Evidence rejected

Price and ownership were not used as draft value. Screening scores were not interpreted as precise season projections. Players marked as departed were heavily penalised.

## Uncertainty and next triggers

Directly pairwise-review the highest new entrants, especially forwards, attacking full-backs and players changing clubs or roles. Confirm preseason first-team minutes, set pieces and manager comments before promoting anyone into the manually reviewed top 140.

## Sources

- [Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/)
- [Official fixtures](https://fantasy.premierleague.com/api/fixtures/)
