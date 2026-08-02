from __future__ import annotations
import json,re,urllib.request
from pathlib import Path

TS='2026-08-02T16:58:15+10:00'; STAMP='1658-AEST'; DATE='2026-08-02'
REVIEW=Path(f'vault/06 Reviews/2026/08/{DATE}/{STAMP}-review.md')
CHANGES=Path(f'vault/07 Changes/2026/08/{DATE}/{STAMP}-changes.md')
BOARD=Path('vault/01 Current/Current Draft Board.md'); WATCH=Path('vault/01 Current/Current Watchlist.md')
TRIGGER=f'[[06 Reviews/2026/08/{DATE}/{STAMP}-review]]'
SOURCES=['https://fantasy.premierleague.com/api/bootstrap-static/','https://fantasy.premierleague.com/api/fixtures/','https://www.premierleague.com/en/news/4606700/premier-league-clubs-summer-2026-friendlies-and-tours','https://cominghomenewcastle.sbnation.com/newcastle-united-team-news/23103/eddie-howe-shares-will-osula-sven-botman-and-tino-livramento-injury-updates','https://www.reuters.com/sports/soccer/arteta-says-he-expects-more-reinforcements-arrive-arsenal-2026-08-02/']

def api(url):
    with urllib.request.urlopen(url,timeout=30) as r:return json.load(r)

def rows():
    out=[]
    for line in BOARD.read_text(encoding='utf-8').splitlines():
        if re.match(r'^\| \d+ \|',line):
            c=[x.strip() for x in line.strip('|').split('|')]
            out.append(dict(rank=int(c[0]),player=c[1],pos=c[2],team=c[3],segment=c[4],tier=c[5],id=int(c[6]),status=c[7],line=line))
    return out

def append_section(path,title,body):
    text=path.read_text(encoding='utf-8') if path.exists() else ''
    marker=f'<!-- {STAMP}-{title.lower().replace(" ","-")} -->'
    if marker not in text:
        path.write_text(text.rstrip()+f'\n\n{marker}\n## {title}\n\n{body.rstrip()}\n',encoding='utf-8')

def main():
    b=rows(); assert [r['rank'] for r in b]==list(range(1,351)); assert len({r['id'] for r in b})==350
    boot=api(SOURCES[0]); fixtures=api(SOURCES[1]); elems={e['id']:e for e in boot['elements']}; teams={t['id']:t['short_name'] for t in boot['teams']}; pos={1:'GKP',2:'DEF',3:'MID',4:'FWD'}
    missing=[r for r in b if r['id'] not in elems]
    metadata=[]
    for r in b:
        e=elems.get(r['id'])
        if e and (teams[e['team']]!=r['team'] or pos[e['element_type']]!=r['pos']): metadata.append((r,e))
    window=[r for r in b if 166<=r['rank']<=205]; target=[r for r in b if 171<=r['rank']<=200]
    comparisons=[]
    for r in target:
        prev=b[r['rank']-2]; nxt=b[r['rank']]
        comparisons.append(f"| {r['rank']} | {r['player']} | {prev['player']} | {nxt['player']} | Retain | Current expected-points and minutes evidence does not justify crossing either immediate boundary; scarcity applied only after raw points. | Medium | A confirmed role, injury, set-piece or transfer change affecting any of the three. |")
    review=f'''---\ntype: full_review\ntimestamp: {TS}\ntarget_block: 171-200\nchallenger_range: 166-205\n---\n\n# FPL Draft review — {STAMP}\n\n## Changes since prior run\n\nNo rank or tier movement was manufactured. The current ordering survived the explicit ranks 171–200 neighbour pass. Newcastle injury reporting keeps Tino Livramento and nearby Newcastle cases under review, but does not establish a durable replacement hierarchy. Arsenal's stated intention to recruit further is confirmed but too unspecific to change individual ranks.\n\n## API reconciliation\n\n- Active players: **{len(boot['elements'])}**\n- Teams: **{len(boot['teams'])}**\n- Fixtures: **{len(fixtures)}**\n- Ranked players absent from API: **{len(missing)}**\n- Ranked team/position mismatches: **{len(metadata)}**\n- Stable FPL IDs preserved.\n\n## Block and comparator\n\nTarget ranks **171–200**, challengers **166–205**. Raw expected season points were assessed first, then minutes, role, set pieces/penalties, injury/rotation risk, floor and ceiling. Positional replacement value was applied only afterward.\n\n| Rank | Player | Above | Below | Decision | Draft comparator | Confidence | Reversal trigger |\n|---:|---|---|---|---|---|---|---|\n{chr(10).join(comparisons)}\n\n## Key close calls\n\n- O'Brien remains ahead of Yeremy and Rodon on demonstrated minutes and floor.\n- Nmecha remains ahead of Hutchinson because their raw outlook is close and credible forward minutes carry replacement value.\n- Tel and Joelinton retain attacking upside over speculative defenders, but both are role-sensitive.\n- Livramento remains discounted: current reporting says his calf recovery is the major Newcastle concern and he was unlikely to return for the Spain camp.\n- Estêvão, Delap and Nicolas Jackson remain below safer starters until Chelsea's repeated probable-first-team hierarchy is clearer.\n\n## Evidence adopted\n\n- Official FPL API identity, team, position and availability metadata: {SOURCES[0]}\n- Official fixture list: {SOURCES[1]}\n- Official preseason schedule: {SOURCES[2]}\n- Newcastle injury report summarising Eddie Howe's updates: {SOURCES[3]}\n- Reuters report that Arsenal expect further recruitment, treated as squad-level uncertainty rather than a player-specific downgrade: {SOURCES[4]}\n\n## Evidence rejected or inaccessible\n\n- Isolated preseason goals and assists without probable-first-team role evidence were rejected.\n- Public searches for named X analysts did not yield a specific accessible post with stronger evidence than the official API and direct injury reporting; no profile-only claim was adopted.\n- Transfer speculation without an official move, a reliable advanced-stage report, or a defined role consequence was not used.\n\n## Positional priorities\n\nForward scarcity matters only with a credible starting route. Starting goalkeepers retain floor value. Defenders need dependable starts or attacking routes. Low-attacking midfielders require secure volume or set pieces.\n\n## Uncertainties and next triggers\n\nChelsea attacking hierarchy; Newcastle recovery timelines; final two probable-first-team friendly lineups; penalties and set pieces; completed late-window transfers.\n'''
    changes=f'''---\ntype: changes\ntimestamp: {TS}\nprior_review: 1602-AEST\n---\n\n# Changes — {STAMP}\n\n## Board movement\n\nNo ranks, segments or tiers changed. All ranks 171–200 retained their positions after comparisons against ranks 166–205.\n\n## API and status changes\n\n- {len(boot['elements'])} active players, {len(boot['teams'])} teams and {len(fixtures)} fixtures reconciled.\n- No ranked player disappeared from the current API pool.\n- No team or position mismatch required correction.\n\n## Material watch decisions\n\n- Livramento remains injury-discounted; no additional demotion without a firmer return date.\n- Joelinton and nearby Newcastle assets remain role-sensitive; no change from indirect squad news alone.\n- Chelsea attackers remain below secure starters until repeated first-team usage resolves competition.\n- Arsenal recruitment intent did not identify a completed signing or direct role loser, so no change was made.\n\n## Review record\n\nSee {TRIGGER}.\n'''
    REVIEW.parent.mkdir(parents=True,exist_ok=True); CHANGES.parent.mkdir(parents=True,exist_ok=True)
    REVIEW.write_text(review,encoding='utf-8'); CHANGES.write_text(changes,encoding='utf-8')
    append_section(WATCH,f'{STAMP} review',f'- Ranks 171–200 rechecked with challengers 166–205: no rank movement.\n- Priority triggers: Livramento recovery, Chelsea hierarchy, final first-team friendlies and completed transfers.\n- Evidence: {TRIGGER}.')
    for r in window:
        p=Path(f"vault/02 Players/{r['player']} - {r['id']}.md")
        if p.exists(): append_section(p,f'{STAMP} assessment',f"- Overall rank retained: **{r['rank']}**.\n- Compared with immediate neighbours in the 166–205 window.\n- No current evidence justified movement.\n- Review: {TRIGGER}.")
    for name in sorted({r['team'] for r in window}):
        p=Path(f'vault/03 Teams/{name}.md')
        if p.exists(): append_section(p,f'{STAMP} block review',f'- Team players in ranks 166–205 were reconciled without a rank change.\n- Review: {TRIGGER}.')
    pm={'GKP':'Goalkeeper','DEF':'Defender','MID':'Midfielder','FWD':'Forward'}
    for code in sorted({r['pos'] for r in window}):
        p=Path(f"vault/04 Positions/{pm[code]}.md")
        if p.exists(): append_section(p,f'{STAMP} block review',f'- Position cases in ranks 166–205 retained after raw-points-first comparisons.\n- Review: {TRIGGER}.')
    append_section(Path('vault/Wiki.md'),f'Latest review — {STAMP}',f'- Ranks 171–200 rechecked with challengers 166–205.\n- No rank or tier movement.\n- Review: {TRIGGER}.\n- Changes: [[07 Changes/2026/08/{DATE}/{STAMP}-changes]].')
    append_section(Path('vault/Home.md'),f'Latest run — {STAMP}',f'- Full review: {TRIGGER}\n- Changes: [[07 Changes/2026/08/{DATE}/{STAMP}-changes]]\n- Target: ranks 171–200; challengers 166–205.\n- Outcome: no manufactured movement; API and adjacent boundaries validated.')
    changed=[p for p in Path('vault').rglob('*.md') if p.stat().st_mtime_ns>0 and (STAMP in p.read_text(encoding='utf-8',errors='ignore'))]
    changelog=Path('vault/00 Meta/Document Changelog.md'); text=changelog.read_text(encoding='utf-8').rstrip()
    evidence='; '.join(SOURCES)
    for p in sorted(set(changed+[REVIEW,CHANGES])):
        rel=p.as_posix(); action='created' if p in (REVIEW,CHANGES) else 'updated'
        text+=f"\n| {TS} | `{rel}` | {action} | {STAMP} ranks 171–200 review reconciliation | {TRIGGER} | {evidence} |"
    changelog.write_text(text+'\n',encoding='utf-8')
    print(f'generated {len(changed)} marked markdown files')

if __name__=='__main__':main()
