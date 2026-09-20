#!/usr/bin/env python3
"""Every internal pointer resolves.

THE DEFECT THIS EXISTS FOR
--------------------------
This book points at itself constantly: chapters cross-reference chapters, the
prose names files in templates/ and drills/, and the appendices index both.
Every one of those is a claim about the repository, and the class of claim this
book spends an appendix refusing is precisely the kind that decays silently.

A \\ref to a label that does not exist prints "??" in the PDF, which is at
least visible. A \\code{templates/thing.md} naming a file that was renamed
prints perfectly and sends the reader nowhere.

Three checks:

  1. every \\ref and \\label pair up
  2. every path named in \\code{} that looks like a repository path exists
  3. every relative link in the Markdown files resolves
"""

import re
import sys

from kitlib import ROOT, find_calls, prose_files, report, strip_comments

PATHISH = re.compile(r"^[A-Za-z0-9_.\-]+/[A-Za-z0-9_./\-]+$")
MD_LINK = re.compile(r"\[[^\]]*\]\(([^)#][^)]*)\)")


def main() -> int:
    failures: list[str] = []
    labels: set[str] = set()
    refs: list[tuple[str, int, str]] = []
    paths = 0

    # structure.tex is generated and carries the \label{part:...} anchors, so
    # it has to be read for labels even though it contains no prose. Leaving it
    # out reported nine perfectly good part references as broken -- the gate
    # was wrong, not the book, which is the failure mode a new check is most
    # likely to have.
    for path in prose_files() + [ROOT / "structure.tex"]:
        rel = str(path.relative_to(ROOT))
        text = strip_comments(path.read_text(encoding="utf-8"))
        for _, _, args in find_calls(text, "label", 1):
            labels.add(args[0].strip())
        for line, _, args in find_calls(text, "ref", 1):
            refs.append((rel, line, args[0].strip()))
        for line, _, args in find_calls(text, "code", 1):
            target = args[0].strip().replace("\\_", "_")
            if PATHISH.match(target):
                paths += 1
                probe = target.rstrip("/")
                if not (ROOT / probe).exists():
                    failures.append(f"{rel}:{line}: \\code{{{target}}} names a path that is not there")

    for rel, line, key in refs:
        if key not in labels:
            failures.append(f"{rel}:{line}: \\ref{{{key}}} has no matching \\label")

    # Every \val{} resolves against the generated ledger.
    #
    # \val prints ??key?? loudly when a key is missing, and the obvious check
    # is to look for that in the finished PDF. That check was written, ran, and
    # reported zero -- because the machine had no pdftotext, so it was reading
    # an empty string. An instrument that returns a plausible answer to nothing
    # is worse than no instrument. This reads the source instead, which needs
    # no tool that might be absent.
    ledger = ROOT / "ledger.tex"
    known = set()
    if ledger.exists():
        for _, _, args in find_calls(ledger.read_text(encoding="utf-8"), "kitledgerval", 2):
            known.add(args[0].strip())
    vals = 0
    for path in prose_files():
        rel = str(path.relative_to(ROOT))
        text = strip_comments(path.read_text(encoding="utf-8"))
        for line, _, args in find_calls(text, "val", 1):
            vals += 1
            key = args[0].strip()
            if key not in known:
                failures.append(f"{rel}:{line}: \\val{{{key}}} is not in ledger.tex")

    # Every Markdown file in the tree, rather than the three directories
    # somebody thought of. The first version of this swept templates/, drills/
    # and README.md, and docs/BASELINE-COMPLIANCE.md then arrived carrying
    # eighteen relative links none of which was covered -- a sweep is exactly
    # as wide as the directory it was pointed at, and the command line looks
    # complete either way.
    skip = {".git", "__pycache__", "build", "applications", ".latexmk"}
    md = sorted(
        f
        for f in ROOT.rglob("*.md")
        if not any(part in skip for part in f.relative_to(ROOT).parts)
    )
    md_links = 0
    for path in md:
        rel = str(path.relative_to(ROOT))
        for n, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
            for target in MD_LINK.findall(line):
                if target.startswith(("http://", "https://", "mailto:")):
                    continue
                md_links += 1
                if not (path.parent / target).exists():
                    failures.append(f"{rel}:{n}: link to '{target}' does not resolve")

    summary = (
        f"{len(refs)} refs over {len(labels)} labels, {vals} values, "
        f"{paths} paths, {md_links} markdown links"
    )
    return report("links", failures, summary)


if __name__ == "__main__":
    sys.exit(main())
