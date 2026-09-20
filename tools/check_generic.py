#!/usr/bin/env python3
"""This kit stays company-independent.

THE DEFECT THIS EXISTS FOR
--------------------------
The material behind this book came out of real hiring processes, and the pull
back towards one of them is constant: a specific example is always more vivid
than a general rule, and a company's rubric is always more concrete than a
published ladder. A book that drifts that way stops being usable by anybody
whose process is different, which is everybody.

So the constraint is a gate rather than an intention, and it fails the build
on:

  1. a deny-listed term -- employers, individuals, processes from the author's
     own history. tools/denylist.txt, one per line
  2. a currency figure. Chapter 14 says why this book carries no salary
     numbers; this is that decision enforced rather than remembered
  3. a job-posting identifier, which only ever comes from one application

WHAT IS REPORTED RATHER THAN GATED
----------------------------------
Capitalised words that are neither in sources.json nor in the stoplist are
PRINTED, not failed. A proper-noun gate over English prose produces false
positives faster than anybody will read them, and a gate nobody reads is worse
than no gate. The list is short enough to scan, and scanning it is the point.
"""

import re
import sys

from kitlib import ROOT, load_json, report, strip_comments

CURRENCY = re.compile(r"(?:[€£¥]\s?\d|\\\$\s?\d|\b(?:EUR|USD|GBP|PLN)\s?\d)")
POSTING = re.compile(r"\b(?:job|posting|requisition|req)\s*(?:id|number|#)?\s*\d{4,}", re.I)
# A capitalised word is only interesting when it sits MID-SENTENCE, so the
# pattern requires a lowercase word immediately before it. Sentence starts,
# table cells, list items and headings are all excluded by construction.
#
# The first version matched every capitalised word and excluded sentence starts
# with a lookbehind. It reported 274 words, which is a report nobody reads --
# and a report nobody reads is the failure mode this tool is trying to avoid,
# committed by the tool itself. Narrowing it to mid-sentence takes it to a list
# somebody will actually scan.
# The separator is spaces, not \s. A newline between the two words means the
# capitalised one starts a line -- a table row, a list item, a heading -- and
# those are not proper nouns. Allowing \s reported every table cell in the
# book, including "Recruiter" and "Discovery", because the preceding line
# happened to end in \midrule.
#
# (?<!\\) keeps a macro name from counting as the lowercase word before it.
CAPWORD = re.compile(r"(?<!\\)\b[a-z]{2,}[ ]+([A-Z][a-z]{2,})\b")
ANYCAP = re.compile(r"\b([A-Z][a-z]{2,})\b")

# Ordinary capitalised English, plus this book's own vocabulary. A word here is
# not evidence of anything; it is a word the report would otherwise repeat on
# every run until nobody read the report.
STOPLIST = {
    "Appendix", "Chapter", "Part", "Note", "Drill", "The", "This", "That", "There",
    "These", "Those", "They", "Their", "Then", "Them", "What", "When", "Where",
    "Which", "While", "Who", "Why", "How", "And", "But", "For", "Not", "Now",
    "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten",
    "First", "Second", "Third", "Staff", "Senior", "Junior", "Principal",
    "English", "British", "Every", "Each", "Ask", "Say", "Read", "Write", "Take",
    "Find", "Give", "Keep", "Look", "Make", "Most", "Much", "Some", "Something",
    "Nobody", "Somebody", "Anybody", "Anything", "Nothing", "Everything",
    "Before", "After", "During", "Against", "About", "Above", "Below", "Between",
    "Into", "Over", "Under", "Without", "With", "From", "Once", "Only", "Other",
    "Put", "Set", "Start", "Stop", "Still", "Such", "Test", "Tests", "Your",
    "You", "Yes", "Both", "Because", "Being", "Build", "Called", "Can", "Choose",
    "Count", "Decide", "Describe", "Everybody", "Fill", "Getting", "Have",
    "Here", "Hiring", "Its", "Knowing", "Learn", "Left", "Let", "List", "Low",
    "May", "Measure", "Name", "Never", "Nearly", "New", "Prefer", "Prepare",
    "Print", "Rate", "Real", "Record", "Return", "Right", "Run", "Score",
    "Several", "Show", "Sometimes", "Sort", "Spend", "Store", "Tell", "Time",
    "Treat", "Use", "Used", "Usually", "Verdict", "Was", "Watch", "Work",
    "Would", "Rows", "Reads", "Ended", "Strength", "Claim", "Date", "Session",
    "Format", "Green", "Amber", "Red", "Elapsed", "Clock", "Decision", "Level",
    "Segment", "Band", "Location", "Visa", "Reveals", "Describes", "Assert",
    "Answer", "Reported", "Related", "Grade", "Means", "Topic", "Status",
    "Shape", "Rests", "Example", "Class", "Column", "Question", "Draw",
    "Allowed", "Signal", "Source", "Sources", "Weak", "Strong", "Choosing",
    "Documented", "Cache", "Caching", "Ordinary", "Absence", "Agent", "Model",
    "Chapters", "Tuesday", "Read", "Print",
}


def main() -> int:
    failures: list[str] = []

    deny_path = ROOT / "tools" / "denylist.txt"
    deny = []
    if deny_path.exists():
        for raw in deny_path.read_text(encoding="utf-8").split("\n"):
            term = raw.split("#", 1)[0].strip()
            if term:
                deny.append(term)

    sources = load_json("sources.json")
    allowed = set(STOPLIST)
    for key, meta in sources.items():
        if key.startswith("$"):
            continue
        for field in ("title", "author", "publisher"):
            allowed |= set(ANYCAP.findall(str(meta.get(field, ""))))

    unknown: dict[str, list[str]] = {}
    scanned = 0

    targets = (
        sorted((ROOT / "chapters").glob("*.tex"))
        + sorted((ROOT / "frontmatter").glob("*.tex"))
        + sorted((ROOT / "onepagers").glob("*.tex"))
        + sorted((ROOT / "templates").glob("*.md"))
        + sorted((ROOT / "drills").rglob("*.md"))
    )

    for path in targets:
        scanned += 1
        rel = path.relative_to(ROOT)
        raw = path.read_text(encoding="utf-8")
        text = strip_comments(raw) if path.suffix == ".tex" else raw

        for n, line in enumerate(text.split("\n"), 1):
            low = line.lower()
            for term in deny:
                if re.search(rf"\b{re.escape(term.lower())}\b", low):
                    failures.append(f"{rel}:{n}: deny-listed term '{term}'")
            if CURRENCY.search(line):
                failures.append(f"{rel}:{n}: a currency figure -- this kit carries none")
            if POSTING.search(line):
                failures.append(f"{rel}:{n}: what looks like a job-posting identifier")

        # The role briefs contain invented first names on purpose -- a
        # rehearsal partner needs somebody to be. They are scanned for
        # deny-listed terms and currency like everything else, and excluded
        # from the proper-noun report, which would otherwise report the
        # feature as a defect on every run.
        if "role-briefs" not in str(rel):
            for word in set(CAPWORD.findall(text)):
                if word not in allowed:
                    unknown.setdefault(word, []).append(f"{rel}")

    summary = f"{scanned} files, no deny-listed terms, no currency figures, no posting ids"
    code = report("generic", failures, summary)

    if unknown:
        print(f"   note: {len(unknown)} capitalised word(s) not in sources.json or the stoplist.")
        print("   Reported, not failed -- read them, then add to the stoplist or fix the text.")
        for word in sorted(unknown)[:40]:
            where = unknown[word][0]
            print(f"     {word:<22} {where}")
        if len(unknown) > 40:
            print(f"     ... and {len(unknown) - 40} more")
    return code


if __name__ == "__main__":
    sys.exit(main())
