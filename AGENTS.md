# Working in this repository

This page points at the rules rather than restating them, because a second copy
of a rule is a copy that will disagree with the first.

## Read these before forming an opinion

1. **`ROADMAP.md` §4** — what must not break, and why each item is there.
2. **`DEVIATIONS.md`** — what this repository does not do. A row already
   recorded with a date and a reason is a decision, not a finding.
3. **The book's Chapter 7** — the discipline those two files are written under.

## Touching → load

| You are changing | Read first |
|---|---|
| a chapter | `manifest.json` for its `kind`, then the skeleton for that kind |
| a bank question | the six-part shape in `preamble.tex` and `check_structure.py` |
| a claim about the market | `sources.json`, and the grading rules at the top of it |
| the sequence | `manifest.json` only, then `make generate` |
| a gate | `tools/test_gates.py` — add the mutation in the same change |
| a template | `check_templates.py`, which declares its required sections |
| a figure | `diagrams/`, and `check_figures.py` for placement |

## The things most likely to be got wrong here

1. **`structure.tex`, `sources.tex` and `ledger.tex` are generated.** Editing
   one is an edit that will be reverted with a red build attached. Run
   `make generate`.

2. **`\reported` takes two mandatory arguments.** That is not an inconvenience;
   it makes an unsourced reported claim a build error rather than something a
   gate has to catch afterwards. Do not add a one-argument form.

3. **`[single]` is required exactly where the grade demands it and refused
   elsewhere.** A marker used for safety stops meaning anything.

4. **A `\judgement{}` never carries a source.** A citation on an opinion is
   borrowed authority.

5. **Every chapter ends with *what this chapter does not claim*.** It is not
   modesty; it is the section that tells a reader how much weight the chapter
   bears, and the gate refuses a chapter without one.

6. **Never state a count of occurrences in prose.** Name the rule, or reference
   a computed `\val{}`. A tally decays silently and no gate can see it — which
   is why `ledger.py` exists and why `README.md` points at it rather than
   printing numbers.

7. **`\code{}` and long URLs must be able to break.** Both go through `url`'s
   machinery in `preamble.tex`. A thirty-character path in `\texttt` with no
   break opportunity produced a 66pt overfull line here before that was done.

8. **A table that might grow uses `kittable`**, which is an `xltabular` and
   therefore breakable. A `tabularx` in a `center` cannot break, and a
   comparison table taller than the room left produced an 828pt overfull vbox
   naming no file.

9. **Do not check a build with `grep '^!'`.** With `-file-line-error` an error
   line begins with a path and `-interaction=nonstopmode` writes a PDF over the
   top of it. Use `tools/checklog.py`.

## Conventions worth knowing before you fight them

- **The gates run before the build.** They read the source, none needs a PDF,
  and they cost seconds against a run that costs minutes.
- **Nothing generated is committed**, PDFs included.
- **A check nobody has watched fail is not known to be checking anything.** If
  you add one, plant its defect in `test_gates.py` and watch it refuse.
- **Documentation a change makes untrue is part of that change**, not a
  follow-up. A stale README is a review finding on the day it is written.

## Before opening a pull request

```sh
make generate && make gates && make mutations && make book && make cards && make check
```

An acknowledged deviation is a decision; an unacknowledged one is drift. If
your change leaves something undone, add the row to `DEVIATIONS.md` with what
would close it.

## What not to do

- Do not name a company, a person or a salary figure. `check_generic.py` will
  refuse it, and the gate is the point rather than an obstacle.
- Do not add a case study.
- Do not weaken a gate to make a change pass. Fix the change, or fix the gate
  and prove the new behaviour with a mutation.
- **Do not report a gate as passed that you could not run.** Say it was not run.
