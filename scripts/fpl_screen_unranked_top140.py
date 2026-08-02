from pathlib import Path
import json, re, urllib.request
B=Path('vault/01 Current/Current Draft Board.md')
with urllib.request.urlopen('https://fantasy.premierleague.com/api/bootstrap-static/',timeout=30) as r: api=json.load(r)
T={t['id']:t['short_name'] for t in api['teams']}; POS={1:'GKP',2:'DEF',3:'MID',4:'FWD'}
ranked=set()
for l in B.read_text().splitlines():
    if re.match(r'^\| \d+ \|',l):
        c=[x.strip() for x in l.strip('|').split('|')]; ranked.add(int(c[6]))
rows=[]
for p in api['elements']:
    if p['id'] in ranked: continue
    score=(p.get('now_cost',0)*1.5 + float(p.get('selected_by_percent') or 0)*4 + p.get('total_points',0)*5 + p.get('minutes',0)/50 + p.get('starts',0)*2)
    rows.append((score,p))
rows.sort(reverse=True,key=lambda x:x[0])
out=['# Unranked FPL candidate screen','','| Score | ID | Player | Pos | Team | Cost | Own% | Points | Minutes | Starts | Status |','|---:|---:|---|---|---|---:|---:|---:|---:|---:|---|']
for s,p in rows[:120]:
    out.append(f"| {s:.1f} | {p['id']} | {p['web_name']} | {POS[p['element_type']]} | {T[p['team']]} | {p['now_cost']/10:.1f} | {p['selected_by_percent']} | {p['total_points']} | {p['minutes']} | {p.get('starts',0)} | {p.get('news') or 'Available'} |")
Path('tmp-unranked-candidates.md').write_text('\n'.join(out)+'\n')
print({'ranked':len(ranked),'unranked':len(rows),'top_ids':[p['id'] for _,p in rows[:30]]})
