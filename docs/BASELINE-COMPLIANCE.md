# Baseline compliance

`architecture-standards`' [`REPO-BASELINE.md`](https://github.com/konradcinkusz/architecture-standards/blob/main/docs/guides/REPO-BASELINE.md)
§7 is titled **"Standards adoption is declared, not remembered"**. This is that
declaration for `staff-ai-engineer-preparation-kit`, one row per §9 checklist
item.

The useful column is the third. Several baseline items do not apply to a
repository whose product is a PDF and a handful of Markdown templates, and
without a stated reason each absence looks like neglect — so every **N/A**
carries both why it does not apply *and* the condition under which it would
start to.

Written after the work: every **Yes** points at a file that exists in this
repository today. A compliance document describing intentions is the staleness
§8 warns about — and this one has an additional reason to be careful, because
the book it accompanies spends a chapter on the difference between an artefact
that is legible and an artefact that claims to be.

---

## §1 The baseline

| Item | Answer | Evidence, or why not |
|---|---|---|
| `CODEOWNERS` | **Yes** | [`.github/CODEOWNERS`](../.github/CODEOWNERS). Blanket ownership, with five paths called out because they decide what the book is *allowed to say* rather than what it says: `sources.json` (a grade promoted from `unverified` to `strong` changes nothing on the page and everything about what the page means), `tools/denylist.txt` and `check_generic.py` (a term removed is a term the build accepts forever after, silently), `tools/check_sources.py` with `tools/test_gates.py` (a weakened check and a passing build look identical from outside), and `chapters/app-refused.tex`, the refusal list, where adding is easy and removing should not be |
| Dependency update automation | **Yes, one ecosystem** | [`.github/dependabot.yml`](../.github/dependabot.yml) covers `github-actions`, grouped into one pull request. There is no other ecosystem to cover: the book is LaTeX and every tool under `tools/` imports only the Python standard library. That is deliberate rather than incidental — a preparation kit that needs a dependency resolution to build is a kit that stops building — so the pinned Actions are the only third-party code here, and `release.yml` runs with `contents: write` |
| `.editorconfig` | **Yes** | [`.editorconfig`](../.editorconfig). `trim_trailing_whitespace` is off for `*.md` because trailing whitespace is a hard line break in Markdown and trimming it silently reflows the rendered page — which matters here, where eleven of the Markdown files are templates somebody fills in. `max_line_length = 79` on `*.tex` is stated and deliberately *not* gated: it is what the files look like, so a chapter rewrapped to another width turns a one-sentence change into an unreadable diff, but URLs legitimately exceed it and a gate would be a permanently red ledger |
| `Directory.Build.props` + `Directory.Packages.props` | **N/A** | Central package management for a repository with no packages. There is no `.csproj`, no `package.json`, no `requirements.txt`. **Applies the day any tool here takes a dependency** — and the first one to do so should be argued for in [`DEVIATIONS.md`](../DEVIATIONS.md) rather than merely added, because the zero is load-bearing |
| PR + issue templates | **Yes** | [`pull_request_template.md`](../.github/pull_request_template.md) asks for `make mutations` **first** — a gate nobody has watched fail is not known to be checking anything — and then for the two things a diff cannot show: whether a new claim's source resolves with a date, and whether a claim resting on one source says so *in the sentence* rather than only in the register. Three issue forms, [`claim`](../.github/ISSUE_TEMPLATE/claim.yml), [`generic`](../.github/ISSUE_TEMPLATE/generic.yml) and [`gap`](../.github/ISSUE_TEMPLATE/gap.yml), split the three genuinely different reports this repository can receive. The `generic` form exists because the genericity gate can only refuse the terms somebody thought of, and cannot see a passage that is *implicitly* about one market |
| Real `.gitattributes` | **Yes** | [`.gitattributes`](../.gitattributes). Rules rather than a commented-out template: LF normalisation, explicit `text` for every format present, `binary` for PDFs and images, and `diff=tex` and `diff=python` so a hunk header names the section or the function rather than the nearest blank line |
| `.dockerignore`, exclusion-based | **N/A** | Nothing here is containerised. The artefacts are a PDF and five cards, built on a runner by `xu-cheng/latex-action`. **Applies if the build ever moves into an image** — which is the likeliest future change on this list, because pinning a TeX distribution is the one way to make the page count reproducible |
| Secret scanning: pre-commit **and** CI | **Yes** | §2 below |
| CodeQL / SAST + dependency audit | **N/A for both, and both are close** | There is no compiled first-party code. The nearest thing is thirteen Python files that read files in this tree and write files in this tree. **SAST applies the day a tool here takes untrusted input or touches a credential** — none does, and `tools/check_links.py` is the one to watch, because the day it starts *fetching* the URLs in `sources.json` rather than checking that they parse, it becomes a program that makes network requests on a runner. No dependency audit because there is nothing to audit beyond the Actions, which Dependabot covers |
| CI runs the linters and tests the repo claims | **Yes** | [`build.yml`](../.github/workflows/build.yml) is two jobs, split so that a convention mistake costs five seconds rather than twenty-five minutes: `gates` needs Python only, `build` needs TeX. Every job that gates or compiles runs `make generate` first, because nothing derived is committed and a fresh checkout has nothing to check — the first run of this workflow failed exactly there, reporting `structure.tex is stale` about a file that was not in the tree. Generating unconditionally makes staleness *impossible* on a runner rather than detectable; the `ledger.py --check` that closes `make gates` is a tautology there and is what catches a forgotten `make generate` locally, where the files persist. Then `make gates`, then **`make mutations`** — which is what makes the line above it mean anything, since "the gates passed" is otherwise compatible with the gates checking nothing. Neither job is `continue-on-error` |

---

## §2 Secret hygiene

| Item | Answer | Evidence, or why not |
|---|---|---|
| Pre-commit hook **and** CI job | **Yes** | [`scripts/hooks/pre-commit`](../scripts/hooks/pre-commit) and [`secret-scan.yml`](../.github/workflows/secret-scan.yml), sharing [`.gitleaks.toml`](../.gitleaks.toml). CI scans full history at `fetch-depth: 0`, plus weekly — a commit clean in March is a finding in June when a detection rule is added. The hook **fails** rather than warns when no scanner is installed, because a protection that turns itself off on the machine without the tool is a note in a document nobody reads; `git commit --no-verify` is the deliberate and visible way past it. Install with `make hooks`, reproduce the CI job with `make secrets` |
| The allowlist is by file, never by directory | **Yes** | Stated in [`.gitleaks.toml`](../.gitleaks.toml) and followed: the one custom rule is an addition rather than an exemption. A directory allowlist turns every rule off for files nobody has written yet, which is exactly the file somebody will paste a token into |
| Local scripts read secrets from a gitignored `.env` with a committed example | **N/A** | No script here reads a secret. They read `.tex` and `.json` and write `.tex`; the scanner takes no credential of its own. There is no variable a `secrets.env.example` could document. **Applies the moment a tool needs to authenticate to anything**, and `.gitleaks.toml` carries the corollary: the first secret introduced gets its detection rule in the same commit |
| Rotate before scrubbing history | **Yes, as procedure** | Stated in the hook's own refusal message, where somebody will actually be reading when it matters. Never exercised — no genuine finding has occurred |

---

## §3 Setup, and §4 operational scripts

| Item | Answer | Evidence, or why not |
|---|---|---|
| §3 One-command interactive setup | **Partly** | `make hooks` is the only setup step there is, and [`CONTRIBUTING.md`](../CONTRIBUTING.md) names it. The gates need Python 3.11 and nothing else; the build needs a TeX distribution, which no script can install portably. There is no secret store to initialise and no mandatory secret to generate, so §3's interactive onboarding would be a script with nothing to ask |
| CI jobs mirrored locally | **Yes** | `make gates` and `make mutations` are the commands CI runs, character for character, and [`scripts/scan-secrets.sh`](../scripts/scan-secrets.sh) reproduces the secret-scan job. So "it passed locally" means what the runner means |
| Numbered, delegating runbook scripts; hand-off token files; destroy lists | **N/A** | §4's runbook shape is for a repository with a deploy sequence. There is nothing to deploy: a PDF on a runner and a static page on Pages, neither of which has an ordered teardown |
| Scripts README with variable tiers | **N/A** | Three scripts, none taking an environment variable, all reachable through `make help`. What a contributor needs to know about them is in `CONTRIBUTING.md`, which is where they will look |
| §4a A script that onboards the *product's* user | **N/A, and the product answers it another way** | The product is a book. Its reader opens it — and [`docs/index.html`](index.html) exists precisely so that deciding whether it is worth reading does not require cloning a repository and installing TeX |
| §4b Per-project dependency counts published | **Yes, trivially** | Zero runtime dependencies, zero build dependencies beyond a TeX distribution and Python 3.11. `CONTRIBUTING.md` states it with the command that proves it |
| §4c Research artifacts in-repo; PDFs built in CI rather than committed | **Yes, and it is enforced** | `.gitignore` excludes `*.pdf` and also `structure.tex`, `sources.tex` and `ledger.tex` — all three are generated from `manifest.json` and `sources.json`, and the README says they are not committed, so leaving them in the tree would have been a claim the repository itself falsified. The kit's own working notes are not in-repo because it has none: what would have been a research artefact is `sources.json`, which ships |

---

## §5, §6, §7, §8

| Item | Answer | Evidence, or why not |
|---|---|---|
| §5 Retired workflows archived, never comment-disabled | **Yes, vacuously** | No workflow has been retired. All four are live and triggered. Recorded so the first retirement goes to a `workflows-archive/` directory rather than behind a comment |
| §6 AI agent definitions in-repo | **Partly** | [`AGENTS.md`](../AGENTS.md) is the onboarding document and points at the standards rather than restating them. There is no `.claude/agents/` definition, because no task here has needed a scoped agent. **Applies the day one is added** — it goes in `.claude/agents/` with allowlisted tools and repo-relative paths, never in somebody's local configuration |
| §7 `.claude/settings.json` declares the marketplace | **Yes** | [`.claude/settings.json`](../.claude/settings.json), enabling `architecture-core`. This repository is meant to conform, so declaring conformance while omitting the file that declares it would be incoherent |
| §7 This document | **Yes** | You are reading it |
| §8 README claims verified in review | **Yes, and mechanically where it can be** | The README deliberately states **no counts** and says why: a number typed into prose is a claim nobody maintains, which is a rule this book spends an appendix defending and would be an odd one to break on its own front page. `make ledger` prints them instead, from the tree. `tools/check_links.py` resolves every cross-reference and every `\val{}` in the book, so a reference to a chapter that moved fails the build rather than printing `??` |
| §8 One named source of truth per environment variable | **N/A** | This repository defines no environment variables. Its equivalent is `manifest.json`, which is the single source for the part and chapter sequence, and `sources.json`, which is the single source for every citation — both generated into LaTeX rather than maintained in two places |

---

## What is not claimed

**The book's claims have not been independently audited.** Every `\reported{}`
carries a source with a URL, an access date, a quality grade and whether it was
read directly or through somebody else's summary — and that is a statement about
*provenance*, not about *truth*. A strong source can be wrong. The `claim` issue
form exists because that gap is expected to be closed by readers rather than by
a tool, and Appendix C is the book's own attempt to close part of it in advance
by naming the figures it will not repeat.

**The genericity gate is a floor, not a proof.** It refuses deny-listed terms,
currency figures and posting ids, and it has been watched refusing each. It
cannot see a passage that is generic in its vocabulary and specific in its
assumptions — a loop shape that only one market runs, a ladder only one kind of
employer publishes. That is what the `generic` issue form is for.

**Half of the pre-commit hook has been watched failing and half has not.** The
branch that refuses when no scanner is installed was exercised directly. The
branch that refuses a detected secret has not been, because `gitleaks` is not
installed in the environment the kit was written in; the detection rule itself
*was* watched firing on a planted token and staying quiet on the prose beside
it. The CI job is the reproduction, and it runs on every push.

**No release has been cut.** `release.yml` attaches the handbook and the cards
to a `v*` tag, with no version in any asset name so that a
`releases/latest/download/` link stays current without being edited. No tag has
been pushed, so those links do not resolve yet.

**GitHub Pages has not been enabled.** Creating a repository's Pages site for
the first time is an administrative action, and `administration` is not a scope
a workflow's own token can be granted — no value of `enablement` reaches it. A
repository admin has to choose **Settings → Pages → Build and deployment →
Source → GitHub Actions**, once. `pages.yml` says so at the point of failure
rather than leaving the first red run to be diagnosed.
