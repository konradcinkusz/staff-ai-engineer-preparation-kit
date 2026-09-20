# Templates

Copy this whole directory per company. The originals stay clean.

```sh
cp -r templates/ ../applications/<company>/
```

Every template opens with an `UNFILLED` marker. Delete it when the document is
finished. `python3 tools/check_templates.py` reports how many still carry it —
it reports rather than fails, because a half-filled template is a normal state
mid-process and only a problem when you have forgotten it is there.

| File | Chapter | Fill it in |
|---|---|---|
| `fit-check.md` | 12 | before applying, twenty minutes |
| `role-rubric.md` | 4 | before the screen |
| `company-brief.md` | 14 | before the screen |
| `interviewer-brief.md` | 15 | one per person, before each call |
| `claim-inventory.md` | 10 | before you submit anything |
| `banned-claims.md` | 10 | before every conversation |
| `project-deep-dive.md` | 16 | once, then reuse |
| `run-sheet.md` | 22 | before a build round |
| `decision-log.md` | 22 | during a build round |
| `retrospective.md` | 18 | after every process, including short ones |
| `outcome-ledger.md` | 18 | one row per process, kept forever |

The last one is the only document here that is worth more the longer you keep
it. One process tells you almost nothing; four rows with a pattern in the last
column tell you where your actual constraint is.
