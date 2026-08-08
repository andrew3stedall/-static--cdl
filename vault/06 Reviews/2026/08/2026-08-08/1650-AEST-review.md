---
type: review
reviewed_at: 2026-08-08T16:50:00+10:00
scope: final full-board 1-350 sweep
block_size: 20
buffer: 5
---

# Final full-board FPL Draft sweep — 8 August 2026

## Changes since prior iteration

All 350 ranks were rechecked in 20-player blocks with five-player boundary challengers. The current FPL player pool, transfer/exit risk, injury evidence beyond FPL metadata, newly registered players, roster coverage and current Obsidian links were reconciled.

## Sources searched

- Official FPL player pool: https://fantasy.premierleague.com/api/bootstrap-static/
- Official FPL fixtures: https://fantasy.premierleague.com/api/fixtures/
- Premier Injuries: https://www.premierinjuries.com/injury-table.php
- Bruno Guimaraes agreement: https://www.theguardian.com/football/2026/aug/05/arsenal-agree-75m-fee-with-newcastle-for-bruno-guimaraes-as-clubs-reach-compromise
- Romero Atletico talks: https://www.theguardian.com/football/2026/aug/07/tottenham-and-atletico-in-talks-over-romero-with-van-de-ven-set-to-sign-new-deal
- Rodri Barcelona talks: https://www.theguardian.com/football/2026/aug/07/manchester-city-reject-barcelonas-opening-385m-bid-for-rodri-as-talks-continue
- Newcastle Hornicek/Pope context: https://www.theguardian.com/football/2026/aug/03/premier-league-transfer-newcastle-reject-first-bid-arsenal-bruno-guimaraes
- Chelsea/Fulham transfer roundup: https://www.theguardian.com/football/2026/aug/03/transfer-roundup-chelsea-sell-trevoh-chalobah-sign-jordan-henderson
- Current transfer-rumour sweeps: https://www.theguardian.com/football/2026/aug/07/football-transfer-rumours-cristian-romero-spurs-arsenal-atletico-inter; https://www.theguardian.com/football/2026/aug/05/football-transfer-rumours-folarin-balogun-tottenham-hotspur-pedro-neto-manchester-city; https://www.theguardian.com/football/2026/aug/04/football-transfer-rumour-mill-chelsea-mykhailo-mudryk-lampard-coventry
- Ipswich/Maeda context: https://www.theguardian.com/football/2026/jul/29/premier-league-clubs-strengthen-season-manchester-united-arsenal-midfielders-city-liverpool-chelsea
- Coventry/Rushworth confirmation: https://www.theguardian.com/football/2026/aug/04/frank-lampard-coventry-brighton-carl-rushworth-transfer-roundup
- Tottenham injury update: https://www.tottenhamhotspur.com/news/1079669/team-news-robertos-latest-on-deki-kudus-and-vicario-from-new-zealand

## API reconciliation

The current FPL API contains **573** players. All retained board IDs are present in the API. The prior board had no API-missing IDs but omitted many newly registered players; those players were screened rather than blindly imported. Trevoh Chalobah was removed because his Como transfer is confirmed even though the FPL pool may lag the real-world move.

## New entrants accepted

- **García** (FWD, FUL) entered at **109**; FPL ID 569.
- **Horníček** (GKP, NEW) entered at **115**; FPL ID 567.
- **Maeda** (MID, IPS) entered at **135**; FPL ID 562.
- **Hato** (DEF, CHE) entered at **152**; FPL ID 148.
- **Rudoni** (MID, COV) entered at **163**; FPL ID 183.
- **Fatawu** (MID, IPS) entered at **174**; FPL ID 315.
- **Elliott** (MID, LIV) entered at **181**; FPL ID 383.
- **Clarke** (MID, IPS) entered at **190**; FPL ID 313.
- **Dibling** (MID, EVE) entered at **195**; FPL ID 245.
- **Tchaouna** (MID, COV) entered at **201**; FPL ID 190.
- **Abraham** (FWD, AVL) entered at **207**; FPL ID 56.
- **Nwaneri** (MID, ARS) entered at **212**; FPL ID 22.
- **McAtee** (MID, NFO) entered at **219**; FPL ID 486.
- **Piroe** (FWD, LEE) entered at **224**; FPL ID 348.
- **Kulusevski** (MID, TOT) entered at **231**; FPL ID 521.
- **Palacios** (MID, FUL) entered at **237**; FPL ID 570.
- **Mason-Clark** (MID, COV) entered at **243**; FPL ID 186.
- **Quenda** (MID, CHE) entered at **250**; FPL ID 164.
- **Ferguson** (FWD, BHA) entered at **255**; FPL ID 139.
- **Rushworth** (GKP, COV) entered at **262**; FPL ID 110.
- **Trafford** (GKP, LEE) entered at **268**; FPL ID 385.
- **Philogene** (MID, IPS) entered at **274**; FPL ID 318.
- **Buonanotte** (MID, BHA) entered at **280**; FPL ID 128.
- **O'Riley** (MID, BHA) entered at **287**; FPL ID 126.
- **Carvalho** (MID, BRE) entered at **292**; FPL ID 100.
- **Belloumi** (MID, HUL) entered at **298**; FPL ID 286.
- **Barco** (MID, CHE) entered at **303**; FPL ID 568.
- **Hackney** (MID, EVE) entered at **308**; FPL ID 247.
- **Sakamoto** (MID, COV) entered at **315**; FPL ID 185.
- **Grimes** (MID, COV) entered at **320**; FPL ID 184.
- **Destan** (FWD, HUL) entered at **327**; FPL ID 298.
- **Lavia** (MID, CHE) entered at **333**; FPL ID 161.
- **Fábio Vieira** (MID, ARS) entered at **339**; FPL ID 23.
- **Bailey** (MID, AVL) entered at **345**; FPL ID 44.

## Removals

- **Chalobah** (old rank 111) — confirmed Chelsea-to-Como transfer.
- **Xavi** (old rank 175) — fell below the 350-player buffer after new-player insertion.
- **Yarmoliuk** (old rank 285) — fell below the 350-player buffer after new-player insertion.
- **Onana** (old rank 294) — fell below the 350-player buffer after new-player insertion.
- **Touré** (old rank 321) — fell below the 350-player buffer after new-player insertion.
- **Devenny** (old rank 322) — fell below the 350-player buffer after new-player insertion.
- **Kamara** (old rank 323) — fell below the 350-player buffer after new-player insertion.
- **Svoboda** (old rank 324) — fell below the 350-player buffer after new-player insertion.
- **Kelleher** (old rank 325) — fell below the 350-player buffer after new-player insertion.
- **Diakité** (old rank 326) — fell below the 350-player buffer after new-player insertion.
- **Disasi** (old rank 327) — fell below the 350-player buffer after new-player insertion.
- **Lindelöf** (old rank 328) — fell below the 350-player buffer after new-player insertion.
- **Muharemović** (old rank 329) — fell below the 350-player buffer after new-player insertion.
- **Mosquera** (old rank 330) — fell below the 350-player buffer after new-player insertion.
- **Lewis-Skelly** (old rank 331) — fell below the 350-player buffer after new-player insertion.
- **O'Nien** (old rank 332) — fell below the 350-player buffer after new-player insertion.
- **M.Sarr** (old rank 333) — fell below the 350-player buffer after new-player insertion.
- **Andrey Santos** (old rank 334) — fell below the 350-player buffer after new-player insertion.
- **Iroegbunam** (old rank 335) — fell below the 350-player buffer after new-player insertion.
- **Munoz** (old rank 336) — fell below the 350-player buffer after new-player insertion.
- **Alleyne** (old rank 337) — fell below the 350-player buffer after new-player insertion.
- **Verbruggen** (old rank 338) — fell below the 350-player buffer after new-player insertion.
- **Leno** (old rank 339) — fell below the 350-player buffer after new-player insertion.
- **Sels** (old rank 340) — fell below the 350-player buffer after new-player insertion.
- **Roefs** (old rank 341) — fell below the 350-player buffer after new-player insertion.
- **Lammens** (old rank 342) — fell below the 350-player buffer after new-player insertion.
- **Martinez** (old rank 343) — fell below the 350-player buffer after new-player insertion.
- **Palmer** (old rank 344) — fell below the 350-player buffer after new-player insertion.
- **Kinsky** (old rank 345) — fell below the 350-player buffer after new-player insertion.
- **Perri** (old rank 346) — fell below the 350-player buffer after new-player insertion.
- **Wilson** (old rank 347) — fell below the 350-player buffer after new-player insertion.
- **Mamardashvili** (old rank 348) — fell below the 350-player buffer after new-player insertion.
- **Dubravka** (old rank 349) — fell below the 350-player buffer after new-player insertion.
- **Darlow** (old rank 350) — fell below the 350-player buffer after new-player insertion.

## Injury findings beyond the old FPL labels

- **Xavi Simons:** ACL rehabilitation with a 20 Feb 2027 potential return — severe season-value hit.
- **Amadou Onana:** ACL rupture — substantial downgrade.
- **Wilson Odobert:** ACL recovery with a late-November potential return — long but holdable, still well below healthy peers.
- **Ekitike:** dated 12 Oct potential return is materially better than an indefinite label, so season-long value improves despite surgery/rehab risk.
- **De Ligt:** 6 Sep potential return after back surgery converts an indefinite absence into a medium-term one.
- **Tzimas, Livramento, Lewis Miley and Murillo:** dated August/September targets reduce uncertainty and therefore reduce their injury penalties.
- **Kudus:** Tottenham's manager described him as very close to returning to training, supporting only a small season-long penalty.

## Transfer findings adopted

- **Trevoh Chalobah:** confirmed Como sale -> removed.
- **Cristian Romero:** advanced Atletico negotiations and preferred exit -> major PL-exit discount.
- **Rodri:** Barcelona negotiations/personal terms plus back surgery -> heavy risk discount.
- **Nick Pope:** Hornicek expected to become Newcastle first choice and Pope likely to leave -> major downgrade; Hornicek added.
- **Bruno Guimaraes:** Arsenal fee agreement is a team/role-change watch, not a Premier-League-exit risk -> no punitive season-value downgrade.
- **Gabriel Jesus and Zirkzee:** credible overseas interest recorded, but not treated as completed transfers.
- **Gakpo:** Spurs interest retained as a watch only because Liverpool reportedly have no intention to sell without an exceptional offer.

## Evidence rejected / kept low weight

- Ordinary transfer interest without agreement did not trigger large moves when the likely destination remained in the Premier League.
- Price and ownership were used only to identify new API candidates worth manual attention; they did not determine rank.
- Raw preseason goals or assists without first-team role evidence were not decisive.

## 20-player blocks and five-player buffers

| Block | Buffer checked | Material names |
|---|---|---|
| 1–20 | 1–25 | No material movement |
| 21–40 | 16–45 | Bruno G., Kudus |
| 41–60 | 36–65 | No material movement |
| 61–80 | 56–85 | No material movement |
| 81–100 | 76–105 | No material movement |
| 101–120 | 96–125 | García, Collins, McGinn, Livramento, Horníček |
| 121–140 | 116–145 | Aaronson, Scott, Mukiele, Adingra, Brooks, Schär, Maguire, Sessegnon, Barry, Garner, Zubimendi, Bogle, Hincapie, De Cuyper, Maeda |
| 141–160 | 136–165 | Ekitiké, Hutchinson, Gravenberch, Dunk, Kayode, Sadiki, Hato, Mykolenko, Ayari, Struijk, Hinshelwood, Digne, Branthwaite, Ampadu, Udogie |
| 161–180 | 156–185 | Grealish, Spence, Rudoni, Botman, N.Jackson, Milenković, Hume, Ballard, Van den Berg, Richards, Bijol, Alderete, Thiaw, Fatawu, Caicedo, Yeremy, Boscagli, O'Brien, Martinez, Awoniyi |
| 181–200 | 176–205 | Elliott, Merino, Colwill, Keane, Kalimuendo, De Ligt, Gallagher, Emegha, Osula, Clarke, van Ewijk, Mount, Georginio, Mainoo, Dibling, C.Jones, Thomas, Nmecha, Simms, Hirst |
| 201–220 | 196–225 | Tchaouna, Canvot, Maatsen, Wilson, Ngumoha, Adli, Abraham, Wright, Kamada, Pau, Vicario, Nwaneri, Madueke, Isidor, Tzolis, Gittens, Romero, Buendía, McAtee, Anthony |
| 221–240 | 216–245 | Akpom, Kevin, Kostoulas, Piroe, Wharton, P.M.Sarr, Bergvall, Bakwa, Tzimas, Gudmundsson, Kulusevski, Thomas-Asante, McBurnie, Andersen, Kusi-Asare, Pinnock, Palacios, Enes Ünal, Al-Hamadi, Matheus N. |
| 241–260 | 236–265 | Rodríguez, Talbi, Mason-Clark, Lerma, N.Gonzalez, Hill, A.Becker, Zirkzee, Sánchez, Quenda, Konsa, Khusanov, Danso, Bentancur, Ferguson, Joelinton, White, Yoro, Bassey, Robertson |
| 261–280 | 256–285 | Murillo, Rushworth, Henry, Mings, Rodon, Tsimikas, J.Ramsey, Trafford, Alcaraz, Castagne, Guessand, Chiesa, Markelo, Philogene, Odobert, Gomez, Johnson, Hughes, Kroupi.Jr, Buonanotte |
| 281–300 | 276–305 | Palestra, Fofana, Justin, Burn, Rodrigo, Tanaka, O'Riley, Bradley, Diarra, Hickey, L.Miley, Carvalho, Tonali, Barkley, Rigg, Mazraoui, G.Jesus, Belloumi, Adams, Gomes |
| 301–320 | 296–325 | Janelt, Gray, Barco, Ajer, Tosin, B.Badiashile, Acheampong, Hackney, Tielemans, Sangaré, Dominguez, Diop, Wieffer, Heaven, Sakamoto, Berge, Lukić, Smith, Petrović, Grimes |
| 321–340 | 316–345 | Emersonn, Willock, Christie, Vuskovic, Pope, Reinildo, Destan, Morato, Longstaff, Yates, Gruev, Cook, Lavia, Baleba, Röhl, Milosavljević, Vitor Reis, Igor, Fábio Vieira, Coppola |
| 341–350 | 336–350 | Schuster, Costinha, Manzambi, Bogarde, Bailey, J.Cuenca, Anselmino, Cairney, Ji-soo, Jacquet |

## Largest movements

- **Pope:** 115 -> 325
- **Romero:** 121 -> 217
- **Rodrigo:** 204 -> 285
- **De Ligt:** 267 -> 186
- **G.Jesus:** 236 -> 297
- **Zirkzee:** 187 -> 248
- **Tielemans:** 270 -> 309
- **Ji-soo:** 319 -> 349
- **J.Cuenca:** 316 -> 346
- **Cairney:** 318 -> 348
- **Jacquet:** 320 -> 350
- **Anselmino:** 317 -> 347
- **Bogarde:** 315 -> 344
- **Manzambi:** 314 -> 343
- **Schuster:** 312 -> 341
- **Coppola:** 311 -> 340
- **Costinha:** 313 -> 342
- **Milosavljević:** 308 -> 336
- **Igor:** 310 -> 338
- **Baleba:** 306 -> 334
- **Röhl:** 307 -> 335
- **Ekitiké:** 174 -> 146
- **Vitor Reis:** 309 -> 337
- **Cook:** 305 -> 332
- **Longstaff:** 302 -> 329
- **Gruev:** 304 -> 331
- **Morato:** 301 -> 328
- **Yates:** 303 -> 330
- **Reinildo:** 300 -> 326
- **Smith:** 293 -> 318
- **Christie:** 298 -> 323
- **Berge:** 291 -> 316
- **Lukić:** 292 -> 317
- **Emersonn:** 296 -> 321
- **Willock:** 297 -> 322
- **Vuskovic:** 299 -> 324
- **Petrović:** 295 -> 319
- **Wieffer:** 289 -> 313
- **Diop:** 288 -> 312
- **Heaven:** 290 -> 314
- **Dominguez:** 287 -> 311
- **Sangaré:** 286 -> 310
- **Gomes:** 277 -> 300
- **Adams:** 276 -> 299
- **Ajer:** 281 -> 304
- **Janelt:** 278 -> 301
- **B.Badiashile:** 283 -> 306
- **Tosin:** 282 -> 305
- **Acheampong:** 284 -> 307
- **Gray:** 279 -> 302
- **Barkley:** 272 -> 294
- **Bradley:** 266 -> 288
- **Mazraoui:** 274 -> 296
- **Tonali:** 271 -> 293
- **Rigg:** 273 -> 295
- **Hickey:** 269 -> 290
- **Tanaka:** 265 -> 286
- **Diarra:** 268 -> 289
- **Fofana:** 262 -> 282
- **Palestra:** 261 -> 281
- **Justin:** 263 -> 283
- **Burn:** 264 -> 284
- **Kroupi.Jr:** 260 -> 279
- **Gomez:** 257 -> 276
- **Johnson:** 258 -> 277
- **Hughes:** 259 -> 278
- **Odobert:** 256 -> 275
- **Guessand:** 253 -> 271
- **Markelo:** 255 -> 273
- **Alcaraz:** 251 -> 269
- **Castagne:** 252 -> 270
- **Chiesa:** 254 -> 272
- **Mings:** 247 -> 264
- **Henry:** 246 -> 263
- **Rodon:** 248 -> 265
- **Tsimikas:** 249 -> 266
- **J.Ramsey:** 250 -> 267
- **White:** 242 -> 257
- **Tzimas:** 214 -> 229
- **Bassey:** 244 -> 259

## Roster coverage guardrail

Top-160 positional availability after the sweep: **5 GKP, 49 DEF, 78 MID, 28 FWD**. This supports the required final squad minimum of **2 GKP / 5 DEF / 8 MID / 3 FWD**; the final two roster slots are flexible.

## Major uncertainties / reversal triggers

- Completion or collapse of Romero, Rodri, Bruno Guimaraes, Gabriel Jesus and Zirkzee moves.
- Newcastle explicitly naming Hornicek or Pope as No.1, or Pope completing a transfer.
- New medical timelines for Saliba, Tielemans and other no-return-date cases.
- New FPL registrations between this sweep and draft day.

## Link audit result

Checked **4245** structured wikilinks across current/player/team/position navigation documents; **0 broken links remain**. Immutable historical review/change records were not rewritten.


## 17:12 AEST goalkeeper-tail quality correction

A post-generation sanity check found that mass insertion of new registrations had pushed established/probable starting goalkeepers out of the 350 while leaving speculative reserve outfielders at the tail. That was rejected as a mechanical artefact rather than a valid Draft comparison.

Re-entered: **Kelleher (219), Lammens (232), Sels (255), Verbruggen (258), Leno (263), Roefs (270), Martinez (277)**. Kelleher is Brentford's established replacement for Flekken; Sels started Forest's preseason opener; Leno remains Fulham's senior goalkeeper; Roefs is Sunderland's established first choice; current reporting also supports Lammens as Manchester United's lead goalkeeper.

Removed instead from the ranked tail: **Jacquet, Ji-soo, Anselmino, J.Cuenca, Costinha, Schuster and Vitor Reis**. Their uncertain/reserve minutes do not beat the season-long floor of a starting goalkeeper when every Draft manager needs two.

Sources: https://www.brentfordfc.com/en/news/article/first-team-brentford-sign-caoimhin-kelleher-liverpool; https://www.premierleague.com/en/news/4680049/team-news-glasners-first-xi-confirmed; https://www.fulhamfc.com/players/bernd-leno/; https://www.sunderlandafc.news/club/first-team-squad/
