# Roadmap

Milestones carry *what* and *when*. This document carries the two things they
cannot: **why the order is what it is**, and **what must not break**. A future
session — human or agent — should be able to read this file alone and pick up
the work.

## 1. What "complete" means

The book is written end to end: five parts, every chapter, five appendices,
every template, every card, the drills, and the gates with their mutation
tests. Nothing in it is a stub.

Run `make ledger` for the measured state. No counts are written here, for the
reason the book spends an appendix on: a tally nobody maintains decays, and
this file would be the first place it decayed.

What is *thin* rather than missing is in `DEVIATIONS.md`, with a closing
condition for each row. Read that before deciding anything is finished.

## 2. Phases

**Phase 1 — depth in Part V.** Bank chapters 34–37 carry fewer questions and
shorter *where this is contested* sections than 30–33 (D-4). The shape is
right; the filling is uneven.

**Phase 2 — the reading list.** Appendix D is seeded (D-3). It is the thinnest
part of the book and the cheapest to improve.

**Phase 3 — figures.** Four, where several chapters would carry one (D-5).
`check_figures.py` already gates placement, so this is drawing rather than
plumbing.

**Phase 4 — reader validation.** D-1, and the only phase that cannot be done
alone. Until two or three people have prepared with this and said what was
wrong, the assembly is unvalidated and the book says so on its own pages.

## 3. Why that order

Depth before breadth, because the parts that are thin are thin *in a way a
reader will notice*: a bank chapter with two questions where its neighbour has
four reads as an unfinished book rather than as a shorter subject.

The reading list before figures, because it is the part somebody else can
verify and therefore the part where being wrong is most visible.

Validation last, because it is the only phase whose input is other people's
time, and asking for that before the thin parts are filled spends it badly.

## 4. What must not break

| | |
|---|---|
| **Genericity** | `check_generic.py` fails on a deny-listed term, a currency figure or a posting identifier. The kit came out of real processes and the pull back towards one of them is constant. Do not weaken this gate; add to `tools/denylist.txt` instead. |
| **The claim marking** | `\reported` takes its source as a mandatory argument, so an unsourced reported claim is a build error. Do not add a one-argument convenience form. |
| **The single-source marking** | `check_sources.py` requires `[single]` exactly where the grade demands it, and refuses it elsewhere. A marker sprinkled on for safety stops meaning anything. |
| **The six-part question** | A bank question missing one of its six parts stops being comparable with the others. `check_structure.py` refuses it. |
| **Mutation tests** | Every gate is watched refusing a planted defect. If you add a gate, add its mutation in the same change. |
| **Nothing generated is committed** | `structure.tex`, `sources.tex`, `ledger.tex` and every PDF. A committed generated file is a copy that will disagree with its source. |
| **The manifest is the sequence** | `manifest.json`, and nothing else. Two copies of a list disagree eventually and both still compile. |

## 5. Execution policy

One issue, one pull request. Regenerate before committing:
`make generate && make gates`. If a gate fails on something you believe is
correct, **fix the gate and add the mutation that proves the new behaviour** —
do not weaken it and move on.

If a check cannot be made to fail on a planted defect, it is not known to be
checking anything, and it should be deleted rather than kept for reassurance.

## 6. Non-goals, with re-activation triggers

**A Polish edition.** Bilingual is taken all the way or not at all — one body,
a language file per edition, and a parity gate class proving the two cannot
drift. Reactivate when somebody wants it enough to build that machinery, not
when somebody offers a translation.

**A flashcard bundle of the bank.** The six-part question shape does not
survive compression to a card, and a lossy second presentation of the same
material is a second thing to keep true. Reactivate if the bank is ever
restructured around single-fact questions, which would be a different book.

**A case study.** Refused permanently. The method is general or it is not worth
having, and a worked case is how a generic kit becomes one company's rubric.
