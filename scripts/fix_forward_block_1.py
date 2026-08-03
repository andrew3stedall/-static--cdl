from pathlib import Path
import re
TS='2026-08-03T16:48:00+10:00'
root=Path('vault')
board=root/'01 Current/Current Draft Board.md'
s=board.read_text()
s=re.sub(r'(?m)^last_updated: .*$',f'last_updated: {TS}',s)
s=re.sub(r'(?m)^status: .*$', 'status: forward_positions_1_30_reviewed', s)
s=re.sub(r'This is the \*\*only canonical current overall ordering\*\*\..*?\n\n## Advised order', 'This is the **only canonical current overall ordering**. Forward positional ranks 1–30 have been insertion-sorted with challengers 31–35. Raw expected FPL points were compared first, followed by minutes, role, set pieces and risk; all non-forward global slots were preserved.\n\n## Advised order', s, count=1, flags=re.S)
board.write_text(s)

p=root/'04 Positions/Forward.md'
s=p.read_text()
s=re.sub(r'## Current leaders\n\n.*?\n\n## Current risks', '''## Current leaders

1. [[02 Players/Haaland - 411]]
2. [[02 Players/Isak - 379]]
3. [[02 Players/Watkins - 55]]
4. [[02 Players/Thiago - 106]]
5. [[02 Players/Gyökeres - 25]]
6. [[02 Players/João Pedro - 165]]

## Current risks''', s, count=1, flags=re.S)
p.write_text(s)

c=root/'07 Changes/2026/08/2026-08-03/1648-AEST-changes.md'
s=c.read_text().replace('Challengers Isidor, Wright, Hirst and Georginio did not enter the top 30 forwards.', 'Challengers Emegha, Isidor, Wright, Hirst and Georginio did not enter the top 30 forwards.')
c.write_text(s)
