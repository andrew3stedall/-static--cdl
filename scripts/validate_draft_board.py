from __future__ import annotations

import re
from pathlib import Path

BOARD = Path("vault/01 Current/Current Draft Board.md")
EXPECTED_MAX_RANK = 350


def main() -> None:
    # The canonical board must remain a complete physical sequence, not merely contain rank labels.
    lines = BOARD.read_text(encoding="utf-8").splitlines()
    rows: list[tuple[int, int, str]] = []

    for line in lines:
        if not re.match(r"^\| \d+ \|", line):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 7:
            raise SystemExit(f"Malformed board row: {line}")
        rank = int(cells[0])
        player = cells[1]
        fpl_id = int(cells[6])
        rows.append((rank, fpl_id, player))

    ranks = [rank for rank, _, _ in rows]
    ids = [fpl_id for _, fpl_id, _ in rows]
    expected = list(range(1, EXPECTED_MAX_RANK + 1))

    missing = sorted(set(expected) - set(ranks))
    duplicate_ranks = sorted({rank for rank in ranks if ranks.count(rank) > 1})
    duplicate_ids = sorted({fpl_id for fpl_id in ids if ids.count(fpl_id) > 1})

    errors: list[str] = []
    if len(rows) != EXPECTED_MAX_RANK:
        errors.append(f"expected {EXPECTED_MAX_RANK} ranked rows, found {len(rows)}")
    if ranks != expected:
        errors.append("rank rows are not physically ordered 1..350")
    if missing:
        errors.append(f"missing ranks: {missing}")
    if duplicate_ranks:
        errors.append(f"duplicate ranks: {duplicate_ranks}")
    if duplicate_ids:
        errors.append(f"duplicate FPL IDs: {duplicate_ids}")

    if errors:
        raise SystemExit("Draft board validation failed:\n- " + "\n- ".join(errors))

    print("Draft board valid: 350 unique, physically ordered ranks and 350 unique FPL IDs.")


if __name__ == "__main__":
    main()
