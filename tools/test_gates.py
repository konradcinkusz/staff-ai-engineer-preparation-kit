#!/usr/bin/env python3
"""Every gate is watched refusing a planted defect.

THE DEFECT THIS EXISTS FOR
--------------------------
A check nobody has watched fail is not known to be checking anything. That
sentence is in Chapter 32 as advice to the reader, and a repository that gives
it while shipping unexercised checks would be advice nobody should take.

So each gate gets two runs: one against a tree with a specific defect planted
in it, which must FAIL, and one against the clean tree, which must PASS. Both
halves matter. Without the second, a gate that is broken in some other way
looks like a successful catch -- which is the mutation-testing rule from the
same chapter, applied here.

The tree is copied to a temporary directory and mutated there, so a run that
dies half way cannot leave a planted defect behind in the repository.

Run: python3 tools/test_gates.py
"""

import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP = {".git", "build", "__pycache__", ".latexmk"}


def plant_denylisted(tree: pathlib.Path) -> None:
    (tree / "tools" / "denylist.txt").write_text(
        "# planted\nNorthwind Trading\n", encoding="utf-8"
    )
    f = tree / "chapters" / "11-loop-anatomy.tex"
    f.write_text(f.read_text() + "\nThe loop at Northwind Trading had five stages.\n")


def plant_currency(tree: pathlib.Path) -> None:
    # chr(0x20AC) rather than an escape in a string literal. The first version
    # of this mutation wrote "\\u20ac" and therefore planted the six literal
    # characters rather than a euro sign, so the mutation survived and looked
    # like a hole in check_generic.py. The gate was fine; the instrument
    # planting the defect was not, which is the failure this whole file exists
    # to make visible -- it just found it one level up.
    euro = chr(0x20AC)
    f = tree / "chapters" / "14-researching-a-company.tex"
    f.write_text(f.read_text() + f"\nThe band for this level is {euro}105000.\n")


def plant_posting_id(tree: pathlib.Path) -> None:
    f = tree / "chapters" / "04-segment-and-posting.tex"
    f.write_text(f.read_text() + "\nSee posting id 312427 for the wording.\n")


def plant_unmarked_single_source(tree: pathlib.Path) -> None:
    """A single-source claim cited as though it were corroborated."""
    f = tree / "chapters" / "19-three-formats.tex"
    t = f.read_text().replace("\\reported[single]{At least one large employer's round",
                              "\\reported{At least one large employer's round", 1)
    f.write_text(t)


def plant_unknown_source(tree: pathlib.Path) -> None:
    f = tree / "chapters" / "30-retrieval.tex"
    f.write_text(f.read_text() + "\n\\reported{Nine in ten loops do this.}{no-such-key}\n")


def plant_unverified_as_claim(tree: pathlib.Path) -> None:
    """An unverified source used as evidence rather than as a refusal."""
    f = tree / "chapters" / "30-retrieval.tex"
    f.write_text(
        f.read_text()
        + "\n\\reported[single]{Roles pay far more.}{refused-comp-premium}\n"
    )


def plant_missing_section(tree: pathlib.Path) -> None:
    f = tree / "chapters" / "20-discovery.tex"
    f.write_text(f.read_text().replace(
        "\\section*{What this chapter does not claim}", "\\section*{Closing thoughts}", 1))


def plant_missing_bank_part(tree: pathlib.Path) -> None:
    f = tree / "chapters" / "32-evals.tex"
    f.write_text(f.read_text().replace("\\qcontested", "\\bankpart{Notes}", 1))


def plant_stale_structure(tree: pathlib.Path) -> None:
    f = tree / "structure.tex"
    f.write_text(f.read_text().replace(
        "\\include{chapters/30-retrieval}", "", 1))


def plant_orphan_chapter(tree: pathlib.Path) -> None:
    (tree / "chapters" / "99-unlisted.tex").write_text("\\chapter{Unlisted}\n")


def plant_broken_ref(tree: pathlib.Path) -> None:
    f = tree / "chapters" / "30-retrieval.tex"
    f.write_text(f.read_text() + "\nSee Chapter~\\ref{ch:does-not-exist}.\n")


def plant_missing_path(tree: pathlib.Path) -> None:
    f = tree / "chapters" / "28-rehearsal.tex"
    f.write_text(f.read_text() + "\nThe brief is in \\code{drills/role-briefs/99-nothing.md}.\n")


def plant_broken_md_link(tree: pathlib.Path) -> None:
    # In docs/ rather than in templates/, because docs/ is the directory the
    # markdown sweep did not originally cover. A mutation planted where the
    # check already looked would have passed before the widening as well.
    f = tree / "docs" / "BASELINE-COMPLIANCE.md"
    f.write_text(f.read_text() + "\nSee [the register](../sources.yaml).\n")


def plant_gutted_template(tree: pathlib.Path) -> None:
    f = tree / "templates" / "fit-check.md"
    f.write_text(f.read_text().replace("## Verdict", "## Thoughts", 1))


def plant_template_without_marker(tree: pathlib.Path) -> None:
    f = tree / "templates" / "run-sheet.md"
    f.write_text(f.read_text().replace("<!-- UNFILLED -->\n", "", 1))


def plant_stale_ledger(tree: pathlib.Path) -> None:
    f = tree / "chapters" / "30-retrieval.tex"
    f.write_text(f.read_text() + "\nOne more sentence, which moves the word count.\n")


def plant_unplaced_figure(tree: pathlib.Path) -> None:
    (tree / "diagrams" / "orphan.tex").write_text("\\begin{tikzpicture}\\end{tikzpicture}\n")


def plant_missing_value(tree: pathlib.Path) -> None:
    f = tree / "chapters" / "app-kit-ledger.tex"
    f.write_text(f.read_text() + "\nThere are \\val{noSuchLedgerKey} of them.\n")


def plant_bad_log(tree: pathlib.Path) -> None:
    """checklog is fed a log rather than a tree; plant one it must refuse."""
    (tree / "planted.log").write_text(
        "chapters/30-retrieval.tex:12: Undefined control sequence.\n"
        "Overfull \\vbox (91.0pt too high) has occurred while \\output is active\n"
        "Output written on main.pdf (200 pages, 1 bytes).\n"
    )


CASES = [
    ("check_generic.py", "a deny-listed employer", plant_denylisted),
    ("check_generic.py", "a currency figure", plant_currency),
    ("check_generic.py", "a job-posting identifier", plant_posting_id),
    ("check_sources.py", "a single-source claim not marked", plant_unmarked_single_source),
    ("check_sources.py", "a citation to no such source", plant_unknown_source),
    ("check_sources.py", "an unverified source used as evidence", plant_unverified_as_claim),
    ("check_structure.py", "a chapter missing its does-not-claim section", plant_missing_section),
    ("check_structure.py", "a bank question missing one of its six parts", plant_missing_bank_part),
    ("check_structure.py", "a stale structure.tex", plant_stale_structure),
    ("check_structure.py", "a chapter in no manifest row", plant_orphan_chapter),
    ("check_links.py", "a reference to a label that does not exist", plant_broken_ref),
    ("check_links.py", "a named file that is not there", plant_missing_path),
    ("check_links.py", "a markdown link outside templates/ that does not resolve", plant_broken_md_link),
    ("check_templates.py", "a template that lost a section", plant_gutted_template),
    ("check_templates.py", "a template with no UNFILLED marker", plant_template_without_marker),
    ("ledger.py --check", "a ledger that no longer matches the tree", plant_stale_ledger),
    ("check_figures.py", "a figure drawn and never placed", plant_unplaced_figure),
    ("check_links.py", "a value with nothing behind it", plant_missing_value),
    ("checklog.py ../planted.log", "an error and a vbox in a build log", plant_bad_log),
]


def run(gate: str, tree: pathlib.Path) -> int:
    parts = gate.split()
    cmd = [sys.executable, str(tree / "tools" / parts[0])] + parts[1:]
    proc = subprocess.run(cmd, cwd=tree / "tools", capture_output=True, text=True)
    return proc.returncode


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        clean = pathlib.Path(tmp) / "clean"
        shutil.copytree(ROOT, clean, ignore=shutil.ignore_patterns(*SKIP))

        # checklog reads a log rather than a tree, so the clean tree needs one
        # that passes -- otherwise its baseline is meaningless.
        (clean / "planted.log").write_text(
            "Output written on main.pdf (200 pages, 1 bytes).\n"
        )

        print("Baseline -- every gate must pass on the clean tree.\n")
        gates = sorted({g for g, _, _ in CASES})
        baseline_bad = []
        for gate in gates:
            code = run(gate, clean)
            mark = "ok  " if code == 0 else "FAIL"
            print(f"  {mark} {gate}")
            if code != 0:
                baseline_bad.append(gate)
        if baseline_bad:
            print("\nThe clean tree does not pass. Nothing below would mean anything:")
            print("a scenario that was broken some other way looks like a successful catch.")
            return 1

        print("\nMutations -- every gate must refuse its planted defect.\n")
        failures = []
        for gate, description, plant in CASES:
            case = pathlib.Path(tmp) / "case"
            if case.exists():
                shutil.rmtree(case)
            shutil.copytree(clean, case)
            plant(case)
            code = run(gate, case)
            if code == 0:
                print(f"  SURVIVED  {gate:<22} {description}")
                failures.append((gate, description))
            else:
                print(f"  caught    {gate:<22} {description}")

        print()
        if failures:
            print(f"{len(failures)} mutation(s) survived. Those gates are not known to check "
                  "what they claim to check.")
            return 1
        print(f"All {len(CASES)} mutations caught, and the clean tree passes.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
