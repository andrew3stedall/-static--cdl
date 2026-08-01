from pathlib import Path
p=Path('vault/00 Meta/Document Changelog.md')
s=p.read_text()
for path in [
'vault/01 Current/Current Draft Board.md',
'vault/01 Current/Current Watchlist.md',
'vault/Home.md','vault/Wiki.md']:
    s=s.replace(f'| `{path}` | Created | Recorded ranks 201–220',f'| `{path}` | Updated | Recorded ranks 201–220')
for path in [
'vault/02 Players/Anthony - 105.md','vault/02 Players/Buendía - 41.md',
'vault/02 Players/Emegha - 170.md','vault/02 Players/Gallagher - 519.md',
'vault/02 Players/Hudson-Odoi - 482.md','vault/02 Players/Janelt - 98.md',
'vault/02 Players/Kroupi.Jr - 78.md','vault/02 Players/Mac Allister - 372.md',
'vault/02 Players/Madueke - 16.md','vault/02 Players/Manzambi - 53.md',
'vault/02 Players/Nketiah - 224.md','vault/02 Players/Strand Larsen - 222.md',
'vault/02 Players/Talbi - 549.md','vault/02 Players/Touré - 461.md',
'vault/02 Players/Yarmoliuk - 102.md']:
    s=s.replace(f'| `{path}` | Updated | Recorded ranks 201–220',f'| `{path}` | Created | Recorded ranks 201–220')
p.write_text(s)
