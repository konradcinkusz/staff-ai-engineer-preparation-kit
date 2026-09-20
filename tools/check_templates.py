#!/usr/bin/env python3
"""The fill-in templates carry their skeleton, and half-filled ones are visible.

THE DEFECT THIS EXISTS FOR
--------------------------
Two things, and only the first is a failure.

A template that has lost a section is a template that quietly stops asking a
question. The fit check without its verdict block is a form somebody fills in
and draws no conclusion from; the deep-dive without "what would have changed
my mind" has dropped the strongest thing in the round. Those are failures.

A template still carrying its UNFILLED marker is REPORTED, not failed. A
half-filled template is a normal state in the middle of a process and only a
problem when you have forgotten it is there -- so the count is printed and the
build stays green.
"""

import pathlib
import sys

from kitlib import ROOT, report

# One required phrase per template. Chosen to be the thing the template exists
# to make you do, so its absence means the document has stopped working.
REQUIRED = {
    "fit-check.md": ["## The six", "## Verdict", "cannot see"],
    "role-rubric.md": ["Verbs in the responsibilities", "## The rubric as rows", "## Count"],
    "company-brief.md": ["## The ladder", "## The band", "could not answer"],
    "interviewer-brief.md": ["published", "## Bridges", "only they could answer"],
    "claim-inventory.md": ["## The table", "## Blank backings", "Strength"],
    "banned-claims.md": ["## The list", "would cost most", "Recovery lines"],
    "project-deep-dive.md": ["right project", "## The six parts", "## Attribution check"],
    "run-sheet.md": ["## Checkpoints", "Before the session", "not prepared"],
    "decision-log.md": ["out of scope", "## Decisions", "## Fallbacks taken"],
    "retrospective.md": ["## What happened", "had not expected", "## Which class"],
    "outcome-ledger.md": ["## Reading it", "above", "below"],
}


def main() -> int:
    failures: list[str] = []
    unfilled: list[str] = []
    seen: set[str] = set()

    for path in sorted((ROOT / "templates").glob("*.md")):
        if path.name == "README.md":
            continue
        seen.add(path.name)
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)

        required = REQUIRED.get(path.name)
        if required is None:
            failures.append(f"{rel}: a template with no required sections declared in this tool")
            continue
        for phrase in required:
            if phrase not in text:
                failures.append(f"{rel}: missing the section containing '{phrase}'")

        if "UNFILLED" in text:
            unfilled.append(path.name)
        if not text.lstrip().startswith("<!-- UNFILLED -->"):
            failures.append(f"{rel}: does not open with the UNFILLED marker")

    for missing in sorted(set(REQUIRED) - seen):
        failures.append(f"templates/{missing} is declared in this tool and does not exist")

    index = (ROOT / "templates" / "README.md")
    if index.exists():
        listed = index.read_text(encoding="utf-8")
        for name in sorted(seen):
            if name not in listed:
                failures.append(f"templates/README.md does not list {name}")

    summary = f"{len(seen)} templates, all carrying their skeleton"
    code = report("templates", failures, summary)
    if not failures:
        print(f"   note: {len(unfilled)} of {len(seen)} still carry the UNFILLED marker "
              "(expected for the originals; copy them per company)")
    return code


if __name__ == "__main__":
    sys.exit(main())
