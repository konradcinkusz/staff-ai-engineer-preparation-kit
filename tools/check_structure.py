#!/usr/bin/env python3
"""The manifest, the chapter files and the generated structure agree.

THE DEFECT THIS EXISTS FOR
--------------------------
Three things have to describe one sequence: manifest.json, the files in
chapters/, and structure.tex. Any two of them can drift apart and the book
still compiles -- it just prints a chapter the gates do not check, or checks
one the book does not print.

It also enforces the section skeletons. Every chapter ends with "What this
chapter does not claim", and that is not a stylistic preference: it is the
section that tells a reader how much weight the chapter bears. A chapter
without one is a chapter making unbounded claims, and it is exactly the kind
of omission that happens under time pressure and is never noticed afterwards.

The bank's six-part question shape is enforced for the same reason. The six
parts are what make its answers comparable to each other; a question missing
one stops being comparable and nothing else would say so.
"""

import subprocess
import sys

from kitlib import ROOT, load_json, report, strip_comments

BANK_PARTS = [
    ("\\qasked", "As asked"),
    ("\\qtested", "What is being tested"),
    ("\\qstaff", "The Staff answer"),
    ("\\qsenior", "The Senior answer that falls short"),
    ("\\qcontested", "Where this is contested"),
    ("\\qdrill", "Drill"),
]


def main() -> int:
    manifest = load_json("manifest.json")
    skeletons = manifest["skeletons"]
    failures: list[str] = []

    chapters = [c for p in manifest["parts"] for c in p["chapters"]]
    expected = {f"{c['n']}-{c['slug']}.tex" for c in chapters}
    expected |= {f"app-{a['slug']}.tex" for a in manifest["appendices"]}
    present = {f.name for f in (ROOT / "chapters").glob("*.tex")}

    for missing in sorted(expected - present):
        failures.append(f"manifest names chapters/{missing}, which does not exist")
    for extra in sorted(present - expected):
        failures.append(f"chapters/{extra} exists and is in no manifest row")

    # structure.tex is generated; a stale one is a silent disagreement.
    gen = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "gen_structure.py"), "--check"],
        capture_output=True,
        text=True,
    )
    if gen.returncode != 0:
        failures.append("structure.tex is stale: run python3 tools/gen_structure.py")

    labels: dict[str, str] = {}

    for ch in chapters:
        path = ROOT / "chapters" / f"{ch['n']}-{ch['slug']}.tex"
        if not path.exists():
            continue
        text = strip_comments(path.read_text(encoding="utf-8"))
        rel = f"chapters/{path.name}"

        for heading in skeletons[ch["kind"]]:
            if f"section*{{{heading}}}" not in text:
                failures.append(f"{rel}: missing section '{heading}' (kind: {ch['kind']})")

        if "\\label{" not in text.split("\n", 2)[1] if len(text.split("\n")) > 1 else True:
            pass  # label position is not policed; existence is, below

        marks = [line for line in text.split("\n") if line.strip().startswith("\\label{ch:")]
        if not marks:
            failures.append(f"{rel}: no \\label{{ch:...}}, so nothing can cross-reference it")
        else:
            key = marks[0].strip()[7:-1]
            if key in labels:
                failures.append(f"{rel}: label {key} is already used by {labels[key]}")
            labels[key] = rel

        if ch["kind"] == "bank":
            blocks = text.split("\\begin{bankq}")[1:]
            if not blocks:
                failures.append(f"{rel}: a bank chapter with no \\begin{{bankq}}")
            for n, block in enumerate(blocks, 1):
                body = block.split("\\end{bankq}")[0]
                for macro, name in BANK_PARTS:
                    if macro not in body:
                        failures.append(f"{rel}: question {n} is missing '{name}' ({macro})")

    summary = (
        f"{len(chapters)} chapters, {len(manifest['appendices'])} appendices, "
        f"{len(labels)} labels, structure.tex current"
    )
    return report("structure", failures, summary)


if __name__ == "__main__":
    sys.exit(main())
