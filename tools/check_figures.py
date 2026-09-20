#!/usr/bin/env python3
"""Every figure is drawn once and placed once.

THE DEFECT THIS EXISTS FOR
--------------------------
A figure file that nothing inputs is invisible: it compiles, it is committed,
and it is not in the book. A \\input{diagrams/...} naming a file that was
renamed is a build error, which is at least loud -- but a figure placed twice
is neither, and it prints the same picture under two numbers.

So: every file in diagrams/ is input exactly once, and every input resolves.
"""

import re
import sys

from kitlib import ROOT, prose_files, report, strip_comments

INPUT = re.compile(r"\\input\{diagrams/([A-Za-z0-9_.\-]+)\}")


def main() -> int:
    failures: list[str] = []
    drawn = {p.stem for p in (ROOT / "diagrams").glob("*.tex")}
    placed: dict[str, list[str]] = {}

    for path in prose_files():
        rel = str(path.relative_to(ROOT))
        text = strip_comments(path.read_text(encoding="utf-8"))
        for name in INPUT.findall(text):
            placed.setdefault(name.removesuffix(".tex"), []).append(rel)

    for name, where in sorted(placed.items()):
        if name not in drawn:
            failures.append(f"{where[0]}: inputs diagrams/{name}, which does not exist")
        elif len(where) > 1:
            failures.append(f"diagrams/{name} is placed {len(where)} times: {', '.join(where)}")

    for orphan in sorted(drawn - set(placed)):
        failures.append(f"diagrams/{orphan}.tex is drawn and never placed, so it is not in the book")

    return report("figures", failures, f"{len(drawn)} figures, each drawn once and placed once")


if __name__ == "__main__":
    sys.exit(main())
