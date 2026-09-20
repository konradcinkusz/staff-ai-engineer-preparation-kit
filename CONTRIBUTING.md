# Contributing

Corrections are more welcome than additions, and a correction with a source is
the most welcome thing of all.

## What this book most needs

1. **Being wrong about something.** If a claim here does not match what you
   have seen, say so. The claim marking exists so you can tell which sentences
   are evidence and which are opinion, and disagreeing with the second kind is
   the intended use.
2. **A better source.** Several claims rest on one source and say so in the
   sentence. Replacing one of those with a corroborating source is worth more
   than a new chapter.
3. **Depth in Part V**, chapters 34–37 (`DEVIATIONS.md` D-4).
4. **A reader who used this and reported back** (D-1). This is the one thing
   the book cannot do for itself.

## The rules a change has to satisfy

**A claim about the market carries a source.** `\reported{text}{key}`, with the
key in `sources.json`. If your source is one person's account, grade it
`single-source` and write `\reported[single]{...}` — the sentence has to say so.

**An opinion is marked.** `\judgement{...}`, and never with a source attached.

**No named companies, people or currency figures.** A public company may be
named as a cited source in `sources.json` and in no other way.
`check_generic.py` enforces it.

**Never state a count of occurrences.** Name the rule, or reference a computed
`\val{}`.

**A new gate comes with its mutation.** Plant the defect in
`tools/test_gates.py` and watch the gate refuse it, in the same change. A check
nobody has watched fail is not known to be checking anything.

## Setting up

```sh
make hooks         # point git at the committed pre-commit hook
```

That is the whole of it. The gates need Python 3.11 and nothing else — no
`pip install`, no lock file, no virtual environment — and the build needs a TeX
distribution with `tikz`, `tcolorbox`, `xltabular` and `environ`.

The hook refuses a commit carrying a secret, and **refuses outright when no
scanner is installed** rather than warning and passing. A check that skips
itself on the machine without the tool is not a check; `git commit --no-verify`
is the deliberate way past it.

## Before you open a pull request

```sh
make mutations     # FIRST -- prove the gates can fail
make generate      # structure.tex, sources.tex, ledger.tex
make gates         # every check that does not need a PDF
make book cards    # the handbook and the five cards
make check         # read the log properly
```

`make mutations` goes first for the reason the rules above give: the sentence
"the gates passed" is compatible with the gates checking nothing, and only the
mutation pass separates the two.

The rest runs before the build rather than inside it. Those checks read the
source, none of them needs a PDF, and they cost seconds against a LaTeX run
that costs minutes.

All of it runs in CI. Running it first is faster than finding out there.

## Adding a chapter

1. A row in `manifest.json`.
2. `chapters/NN-slug.tex`, with a `\label{ch:...}` and the sections the
   skeleton for its `kind` requires.
3. `make generate`.
4. `make gates` names whichever half you forgot.

## Adding a source

A key in `sources.json` with a URL, an `accessed` date, a `quality` grade and a
`read` field saying whether you read it or its coverage. Then `make generate`,
which renumbers and regenerates the register Appendix D prints.

Be honest about `read`. A summary of a source is somebody else's reading of it,
with their emphasis, and the book records the difference on purpose.

## Where the rest of it is documented

| | |
|---|---|
| What is deliberately not here, and what would bring it back | [`ROADMAP.md`](ROADMAP.md) |
| Departures from the estate's standards, dated, with closing conditions | [`DEVIATIONS.md`](DEVIATIONS.md) |
| The baseline checklist, one row per item, with every N/A justified | [`docs/BASELINE-COMPLIANCE.md`](docs/BASELINE-COMPLIANCE.md) |
| How to get an agent usefully oriented in this repository | [`AGENTS.md`](AGENTS.md) |

## Style

British English. Second person. A senior reader. No marketing register: no
*simply*, no *just*, no *powerful*. Where a claim is contested, say so rather
than picking the side that makes a cleaner sentence.
