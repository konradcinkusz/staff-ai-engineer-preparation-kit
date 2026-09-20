#!/usr/bin/env python3
"""Decide whether a LaTeX run actually succeeded.

THE DEFECT THIS EXISTS FOR
--------------------------
Do not check a build with `grep '^!' main.log`.

With -file-line-error an error line begins with a path rather than a bang, and
with -interaction=nonstopmode pdflatex writes a PDF over the top of the error
and exits reporting a document. So the exit code says fine, the PDF exists, and
the grep finds nothing -- three independent signals all agreeing, all wrong.

This tool reads the log the way somebody would if they had been bitten: it
matches both error formats, and it fails on the two classes of complaint that
never produce an error at all.

  Overfull vbox      a box grew past a page and could not break. The fix is to
                     split the table, never to shrink the text, and it is worth
                     failing on because the result is content with nowhere to
                     go.
  Overfull hbox      only above a budget. A book on this measure produces a
                     tail of small ones that no rewording clears, because the
                     offending run is usually a file name. Anything over the
                     budget is a real defect; the tail is reported.

It also fails on a non-converged run. "Rerun to get cross-references right" and
"Label(s) may have changed" mean a number on the page is stale, and a stale
number fails silently -- which is the same shape as every other defect here.
"""

import pathlib
import re
import sys

BUDGET_PT = 15.0

ERROR = re.compile(r"^(?:! |[^\s:]+\.\w+:\d+: )", re.M)
OVERFULL_H = re.compile(r"Overfull \\hbox \(([0-9.]+)pt too wide\)")
OVERFULL_V = re.compile(r"Overfull \\vbox \(([0-9.]+)pt too high\)")
HARD_WARN = ("Rerun to get", "Label(s) may have changed", "There were undefined references")


def check(path: pathlib.Path) -> tuple[int, list[str], list[str]]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    fails, notes = [], []

    for m in ERROR.finditer(text):
        line = text[m.start() : text.find("\n", m.start())].strip()
        if line.startswith("!"):
            fails.append(f"{path.name}: {line}")
        elif ".tex:" in line or ".sty:" in line or ".cls:" in line:
            fails.append(f"{path.name}: {line}")

    vboxes = [float(x) for x in OVERFULL_V.findall(text)]
    for size in vboxes:
        fails.append(
            f"{path.name}: overfull vbox, {size:.1f}pt too high -- a block grew past a "
            "page and could not break. Split it; do not shrink it."
        )

    hboxes = sorted((float(x) for x in OVERFULL_H.findall(text)), reverse=True)
    for size in hboxes:
        if size > BUDGET_PT:
            fails.append(f"{path.name}: overfull hbox, {size:.1f}pt over a {BUDGET_PT:.0f}pt budget")

    for warn in HARD_WARN:
        if warn in text:
            fails.append(f"{path.name}: '{warn}' -- the run did not converge, so a number on the page may be stale")

    under = len(re.findall(r"Underfull \\hbox", text))
    tail = [h for h in hboxes if h <= BUDGET_PT]
    if tail:
        notes.append(f"{path.name}: {len(tail)} overfull hbox under budget, worst {tail[0]:.1f}pt")
    if under:
        notes.append(f"{path.name}: {under} underfull hbox")
    pages = re.findall(r"Output written on \S+\.pdf \((\d+) pages?", text)
    if pages:
        notes.append(f"{path.name}: {pages[-1]} pages")

    return len(fails), fails, notes


def main(argv: list[str]) -> int:
    if not argv:
        print("usage: checklog.py <logfile> [...]", file=sys.stderr)
        return 2
    total, all_fails, all_notes = 0, [], []
    for name in argv:
        path = pathlib.Path(name)
        if not path.exists():
            all_fails.append(f"{name}: no such log -- did the build run?")
            total += 1
            continue
        n, fails, notes = check(path)
        total += n
        all_fails += fails
        all_notes += notes

    for note in all_notes:
        print(f"   {note}")
    if total:
        print(f"\nFAIL [log] {total} problem(s):", file=sys.stderr)
        for f in all_fails:
            print(f"  {f}", file=sys.stderr)
        return 1
    print(f"ok [log] {len(argv)} log(s), no errors, no overfull vbox, nothing over {BUDGET_PT:.0f}pt")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
