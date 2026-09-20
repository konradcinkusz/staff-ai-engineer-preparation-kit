# Deviations

What this repository does not do, and what would close each one.

The discipline is Chapter 7's, applied here rather than only recommended:
**an acknowledged deviation is a decision; an unacknowledged one is drift.**
A row is *deleted* when it is fixed — never marked resolved, because a register
that only grows is a register nobody reads.

Appendix E of the book prints **D-1 to D-7**, which are the rows a reader of
the book is affected by. The rest are about the repository's own tooling and
stay here. That duplication is D-8 — and the split is stated because the
earlier wording said the appendix printed *the same list*, which the appendix
itself falsifies.

Last read against the repository: 2026-09-20.

| # | Date | What | Why | What would close it |
|---|---|---|---|---|
| D-1 | 2026-09-20 | **No reader has used this to prepare for a hiring process and reported back.** The components are evidenced to varying degrees; the assembly of them into a method is not. | It has just been written. | Two or three people running a process with it and saying what was wrong. This is the one claim the book prints as outstanding rather than quietly carrying. |
| D-2 | 2026-09-20 | Several primary sources were read through coverage rather than directly. | They were unreachable from the machine this was written on. `sources.json` marks each with `read: secondary`. | Reading them, and re-checking what rests on them. |
| D-3 | 2026-09-20 | Appendix D is seeded rather than complete. | Time. | A pass whose whole purpose is the reading list. |
| D-4 | 2026-09-20 | Bank chapters 34–37 carry fewer questions and shorter *where this is contested* sections than 30–33. | Deliberate, to get the whole shape standing first. Recorded so it is a decision rather than something a reader discovers. | A second pass over Part V, question by question. |
| D-5 | 2026-09-20 | Four figures, where several chapters would be clearer with one. | Same. | A figure pass. `check_figures.py` already gates placement. |
| D-6 | 2026-09-20 | No Polish edition, though the estate's other book has one. | Bilingual is taken all the way — one body, a language file per edition, a parity gate class — or not at all. Half-done is worse than not done. | Somebody wanting it enough to build the parity machinery, not a translation pass. |
| D-7 | 2026-09-20 | Every layout figure was measured on a bare TeX installation with neither `lmodern` nor `inconsolata`. | It is the machine available. `preamble.tex` probes rather than requires, so the book sets in both — but line breaks, and therefore page counts, differ. | Nothing. It is recorded so no page count is quoted as a fact about both installations. |
| D-8 | 2026-09-20 | Appendix E restates this register rather than being generated from it. | A LaTeX table generated from Markdown is a third generator for one small list. | A generator, if this list grows past a page. |
| D-9 | 2026-09-20 | Figures are TikZ, drawn inline, not the estate's Mermaid-source-plus-render pipeline with a byte-identity check. | That pipeline needs a package registry and a headless browser. With four figures it would make the book rebuildable only where npm resolves — so a reader cloning this could not build it. | Enough figures that maintaining them inline costs more than the dependency. |
| D-10 | 2026-09-20 | `check_generic.py`'s proper-noun half **reports** rather than fails. | A proper-noun gate over English prose produces false positives faster than anybody reads them, and a gate nobody reads is worse than none. The deny-list, currency and posting-id halves do fail. | A better heuristic than "capitalised, mid-sentence, not in the stoplist". |
| D-11 | 2026-09-20 | **Half of the pre-commit hook has been watched failing and half has not.** The branch that refuses when no scanner is installed was exercised directly; the branch that refuses a detected secret was not. | `gitleaks` is not installed on the machine the kit was written on. The detection *rule* in `.gitleaks.toml` was watched firing on a planted token and staying quiet on prose beside it, so the regex is exercised and the hook's own call is not. | Running `make secrets` on a machine that has the scanner, with a planted key, and watching it refuse. `secret-scan.yml` covers it on every push in the meantime. |

## Deliberately not taken

**A gate on how many judgements a chapter may carry.** The ledger reports the
ratio of judgements to sourced claims and does not bound it. There is no
defensible threshold, and a permanently red gate teaches the next person to
stop reading the output.

**A check that a bank answer is *correct*.** The gates check that all six parts
of a question are present. Whether the Staff answer is a good one is a reading
job, and the tool says so rather than letting a green ledger imply otherwise.
