from pathlib import Path

path = Path('vault/00 Meta/Document Changelog.md')
text = path.read_text(encoding='utf-8')
text = text.replace('last_updated: 2026-08-01T23:08:00+10:00', 'last_updated: 2026-08-02T08:00:00+10:00', 1)
rows = [
('vault/06 Reviews/2026/08/2026-08-02/0800-AEST-review.md','Created','Recorded the complete overnight API, transfer, injury, preseason and comparator review.'),
('vault/07 Changes/2026/08/2026-08-02/0800-AEST-changes.md','Created','Recorded the explicit no-change comparison with the prior run.'),
('vault/01 Current/Current Watchlist.md','Updated','Added 1 August friendly evidence triggers and refreshed unresolved risks.'),
('vault/Home.md','Updated','Updated latest-run navigation and next evidence triggers.'),
('vault/Wiki.md','Updated','Updated current state, retained comparisons and active uncertainties.'),
('vault/00 Meta/Document Changelog.md','Updated','Appended a separate audit row for every Markdown file changed by the 08:00 AEST review.'),
]
review='[[06 Reviews/2026/08/2026-08-02/0800-AEST-review]]'
evidence='[Official FPL bootstrap](https://fantasy.premierleague.com/api/bootstrap-static/); [Official fixtures](https://fantasy.premierleague.com/api/fixtures/); [Premier League preseason tracker](https://www.premierleague.com/en/news/4606700/premier-league-clubs-summer-2026-friendlies-and-tours)'
text += '\n'
for doc, action, summary in rows:
    text += f'| 2026-08-02T08:00:00+10:00 | `{doc}` | {action} | {summary} | {review} | {evidence} |\n'
path.write_text(text, encoding='utf-8')
