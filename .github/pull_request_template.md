## What changed, and why

<!-- The reasoning. The diff already carries the file list. -->

## How it was verified

<!-- What you ran, not what you meant to run. -->

- [ ] `make mutations` — every gate watched refusing a planted defect. This
      runs first: a gate nobody has watched fail is not known to be checking
      anything
- [ ] `make gates` — clean. These read the source and need no PDF, so they run
      before the build rather than inside it
- [ ] `make book && make cards` — zero errors, zero unresolved references, no
      overfull vbox, nothing over the 15pt budget
- [ ] Each card still fits on one A4 side. A card that runs to two pages is not
      a card

## If it touches a claim

- [ ] Every new `\reported{}{}` carries a key that resolves in `sources.json`,
      with a URL and the date it was checked
- [ ] A claim resting on one source says *one source* in the sentence, rather
      than only in the register
- [ ] An opinion is `\judgement{}` and reads as one
- [ ] The chapter's **what this chapter does not claim** still covers what the
      chapter now says

## If it touches genericity

- [ ] No employer, no individual, no posting id, no currency figure. The gate
      checks this; the checklist is here because the gate can only refuse the
      terms somebody thought of
- [ ] A public company appears only as a cited source

## What this deliberately does not do

<!-- Scope needs something to fail against. -->
