#!/usr/bin/env python3
"""Every reported claim carries a source, and says when the source is thin.

THE DEFECT THIS EXISTS FOR
--------------------------
This book makes claims about a subject where almost nothing can be measured.
The honest arrangement is that a claim about the market carries a source, an
opinion is marked as an opinion, and a claim resting on one source says so on
the page rather than in a file nobody opens.

\\reported takes its source key as a mandatory second argument, so a reported
claim with no source is a LaTeX error rather than something this gate has to
catch. What this gate catches is the rest:

  1. a key that does not resolve in sources.json
  2. a source graded single-source or unverified cited WITHOUT [single]
  3. [single] used on a source that does not need it -- because a marker
     sprinkled on for safety stops meaning anything
  4. an unverified source cited as a \\reported at all; those exist only so
     Appendix C can name what it refuses
  5. a source with no access date, which is a claim nobody has dated
"""

import sys

from kitlib import ROOT, find_calls, load_json, prose_files, report, strip_comments

THIN = {"single-source", "unverified"}


def main() -> int:
    sources = {k: v for k, v in load_json("sources.json").items() if not k.startswith("$")}
    failures: list[str] = []
    used: set[str] = set()
    reported = 0

    for key, meta in sorted(sources.items()):
        if not meta.get("accessed"):
            failures.append(f"sources.json: '{key}' has no accessed date")
        if meta.get("quality") not in {"strong", "moderate", "single-source", "unverified"}:
            failures.append(f"sources.json: '{key}' has no usable quality grade")

    for path in prose_files():
        rel = path.relative_to(ROOT)
        text = strip_comments(path.read_text(encoding="utf-8"))

        for line, opt, args in find_calls(text, "reported", 2, optional=True):
            reported += 1
            key = args[1].strip()
            used.add(key)
            meta = sources.get(key)
            if meta is None:
                failures.append(f"{rel}:{line}: \\reported cites '{key}', absent from sources.json")
                continue
            grade = meta.get("quality")
            if grade == "unverified":
                failures.append(
                    f"{rel}:{line}: \\reported cites '{key}', graded unverified. "
                    "Those exist only for Appendix C to refuse."
                )
            elif grade in THIN and opt != "single":
                failures.append(
                    f"{rel}:{line}: \\reported cites '{key}' ({grade}) without [single]. "
                    "The sentence has to say so."
                )
            elif grade not in THIN and opt == "single":
                failures.append(
                    f"{rel}:{line}: \\reported cites '{key}' ({grade}) with [single]. "
                    "A marker used where it is not needed stops meaning anything."
                )

        for line, _, args in find_calls(text, "source", 1):
            key = args[0].strip()
            used.add(key)
            if key not in sources:
                failures.append(f"{rel}:{line}: \\source{{{key}}} is absent from sources.json")

    unused = sorted(set(sources) - used)
    summary = f"{reported} reported claims, {len(used)} of {len(sources)} sources cited"
    code = report("sources", failures, summary)
    if unused and not failures:
        # Reported, never fatal. An uncited source is a reading-list entry or a
        # refusal in Appendix C, both of which are legitimate.
        print(f"   note: {len(unused)} source(s) not cited by any claim: {', '.join(unused)}")
    return code


if __name__ == "__main__":
    sys.exit(main())
