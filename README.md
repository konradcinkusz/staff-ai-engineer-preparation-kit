# Staff AI Engineer Preparation Kit

A book, a set of fill-in artefacts, and five cards you print before a call —
for an experienced engineer who is **not** an AI Engineer by title and is
aiming at Staff level.

It is company-independent by construction: a build gate refuses any named
employer, any individual, and any currency figure, so it cannot drift back
towards the one process it came out of.

## What is in it

| | |
|---|---|
| **The book** | five parts, built to `Staff_AI_Engineer_Preparation_Kit.pdf` |
| **`templates/`** | fill-in documents you copy per company |
| **`onepagers/`** | five cards, each one A4 side, meant to be printed |
| **`drills/`** | a rehearsal protocol and four role briefs for a partner |

The five parts: **the map** (what the job is, and what Staff means), **the
evidence** (what you build before applying), **the process** (the loop and what
each stage measures), **the build rounds** (three formats, and the craft each
needs), and **the bank** (questions, ordered by how often each surface is
actually asked).

Run `make ledger` for the current counts. They are not written here, because a
number typed into prose is a claim nobody maintains — which is a rule this book
spends an appendix defending, and would be an odd one to break on its own front
page.

## What it refuses to do

**No figures it cannot source.** No salary bands, no premiums, no pass rates.
Those are regional, stale within two quarters, and mostly unsourced where they
circulate. What is here instead is the method for measuring your own market.

**No case study, and no company.** The method is general or it is not worth
having.

**No claims it could not trace.** Appendix C names the figures every competing
resource repeats and says why each one is not here.

## How claims are marked

Almost nothing in this subject can be measured, so the kind of every claim is
marked on the page. A superscript number means the claim is reported and the
source is in `sources.json` — with its URL, the date it was checked, how good
it is, and whether it was read directly or through somebody else's summary. A
claim resting on one source says *one source* in the sentence. A diamond means
the author's judgement, unsourced on purpose, and you are invited to disagree.

Every chapter ends with **what this chapter does not claim**.

## Build

```sh
make            # gates, then the book, then the cards, then read the log
make gates      # every check that does not need a PDF — run this while writing
make mutations  # prove the gates can fail
make help       # the rest
```

The gates run **before** the build. They read the source, none of them needs a
PDF, and they cost seconds against a LaTeX run that costs minutes.

Nothing generated is committed: `structure.tex`, `sources.tex` and `ledger.tex`
are written by `tools/`, and the PDFs are CI artefacts and release assets. So a
fresh clone runs `make generate` before anything else — which is why `make` on
its own starts there, and why every CI job that gates or compiles does too.

## The gates

| Tool | Refuses |
|---|---|
| `check_structure.py` | manifest, chapters and `structure.tex` disagreeing; a chapter missing a required section; a bank question missing one of its six parts |
| `check_generic.py` | a deny-listed term, a currency figure, a job-posting identifier |
| `check_sources.py` | a citation to nothing; a single-source claim not marked as one; an unverified source used as evidence |
| `check_figures.py` | a figure drawn and never placed, or placed twice |
| `check_templates.py` | a template that has lost a section |
| `check_links.py` | a reference, a value or a named file that does not resolve |
| `checklog.py` | an error, an overfull vbox, or an hbox over budget — never `grep '^!'` |
| `ledger.py` | nothing. It **reports**, and `--check` fails a stale ledger |

`tools/test_gates.py` plants each check's defect and requires refusal. A check
nobody has watched fail is not known to be checking anything.

## The rest of the repository

| | |
|---|---|
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | how to set up, what a change has to satisfy, and what the book most needs |
| [`ROADMAP.md`](ROADMAP.md) | what is deliberately thin, and what is deliberately absent |
| [`DEVIATIONS.md`](DEVIATIONS.md) | departures from the estate's standards, dated, each with a closing condition |
| [`docs/BASELINE-COMPLIANCE.md`](docs/BASELINE-COMPLIANCE.md) | the baseline checklist, one row per item, with every N/A carrying the condition that would end it |
| [`AGENTS.md`](AGENTS.md) | orientation for an agent working here |

## Licence

Text under [CC BY-NC-SA 4.0](LICENSE-CONTENT). Tooling, macros and build under
[MIT](LICENSE).
