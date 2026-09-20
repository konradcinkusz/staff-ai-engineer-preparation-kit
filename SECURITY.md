# Security

This repository builds a PDF from LaTeX and runs Python scripts that read its
own files. It has no server, no database, no network calls at build time, and
no runtime.

## What is worth reporting

- A path traversal or arbitrary write in anything under `tools/`.
- A secret committed anywhere. `gitleaks` runs over the full history on every
  push and weekly, and if it ever misses one, that is worth knowing about.
- A workflow permission wider than the job needs.

## What is not

A LaTeX build compiles code by design, and `-shell-escape` is **not** used
here. If you are compiling a fork you have not read, that is a decision about
trusting the fork rather than a vulnerability in this one.

## How to report

Open a private security advisory on the repository. Please do not open a public
issue for something that would be better fixed before it is described.

## If a secret is ever found

**Rotate first, scrub second.** A rewritten history does not un-leak a
credential that was public for an hour; rotating does. Scrubbing without
rotating is theatre.
