from pathlib import Path

TS = "2026-08-01T23:08:00+10:00"
REVIEW = "[[06 Reviews/2026/08/2026-08-01/2308-AEST-review]]"
EVIDENCE = "[Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/); [Official fixtures](https://fantasy.premierleague.com/api/fixtures/)"

entries = [
    ("vault/01 Current/Current Draft Board.md", "Updated"),
    ("vault/01 Current/Current Watchlist.md", "Updated"),
    ("vault/Home.md", "Updated"),
    ("vault/Wiki.md", "Updated"),
    ("vault/06 Reviews/2026/08/2026-08-01/2308-AEST-review.md", "Created"),
    ("vault/07 Changes/2026/08/2026-08-01/2308-AEST-changes.md", "Created"),
    ("vault/02 Players/Mitoma - 121.md", "Created"),
    ("vault/02 Players/Xhaka - 544.md", "Created"),
    ("vault/02 Players/Iwobi - 261.md", "Created"),
    ("vault/02 Players/Anderson - 481.md", "Updated"),
    ("vault/02 Players/Ampadu - 338.md", "Updated"),
    ("vault/02 Players/Saliba - 6.md", "Created"),
    ("vault/02 Players/J.Timber - 5.md", "Created"),
    ("vault/02 Players/Chalobah - 143.md", "Updated"),
    ("vault/02 Players/Mukiele - 533.md", "Created"),
    ("vault/02 Players/Mitchell - 204.md", "Created"),
    ("vault/02 Players/Collins - 84.md", "Created"),
    ("vault/02 Players/Raya - 1.md", "Created"),
    ("vault/02 Players/Pickford - 226.md", "Created"),
    ("vault/02 Players/Donnarumma - 384.md", "Created"),
    ("vault/02 Players/Henderson - 198.md", "Created"),
    ("vault/02 Players/Kelleher - 82.md", "Created"),
    ("vault/02 Players/O'Reilly - 387.md", "Updated"),
    ("vault/02 Players/Matheus N. - 389.md", "Created"),
    ("vault/02 Players/Lacroix - 200.md", "Created"),
    ("vault/02 Players/Rúben - 390.md", "Created"),
]

path = Path("vault/00 Meta/Document Changelog.md")
text = path.read_text()
text = text.replace("last_updated: 2026-08-01T23:00:00+10:00", f"last_updated: {TS}", 1)
marker = f"| {TS} | `vault/01 Current/Current Draft Board.md` |"
if marker not in text:
    text += "\n"
    for document, action in entries:
        text += f"| {TS} | `{document}` | {action} | Recorded ranks 65–80 pairwise review evidence and placement. | {REVIEW} | {EVIDENCE} |\n"
    text += f"| {TS} | `vault/00 Meta/Document Changelog.md` | Updated | Appended a separate audit row for every Markdown file changed by the ranks 65–80 review. | {REVIEW} | Per-document audit; {EVIDENCE} |\n"
path.write_text(text)
