# Staff AI Engineer Preparation Kit
#
# pdfinfo is not assumed. The card page count is read out of latexmk's own log,
# because a Makefile that needs a tool the machine may not have fails in a way
# that looks like a failing check rather than a missing dependency.
#
# The ordering below is the whole design: the source gates run BEFORE the
# build. They read the source, none of them needs a PDF, and they cost seconds
# against a LaTeX run that costs minutes. Running them afterwards means finding
# out about a missing section after spending the minutes.
#
# `make` does everything. `make gates` is what you run while writing.

LATEX      := latexmk -pdf -interaction=nonstopmode -file-line-error
PY         := python3
CARDS      := $(basename $(notdir $(wildcard onepagers/*-card.tex)))

.PHONY: all gates generate mutations book cards check ledger hooks secrets watch clean help

all: generate gates book cards check ## generate, gate, build, then read the log
# `generate` first, because structure.tex, sources.tex and ledger.tex are not
# committed -- so on a fresh clone there is nothing for the gates to check and
# nothing for LaTeX to \include. `gates` deliberately does NOT depend on it:
# run alone while writing, its closing ledger --check is what tells you that
# you edited manifest.json and forgot.

help: ## list the targets
# awk rather than `column`, which is bsdmainutils and is simply absent on a
# minimal container -- and `make help` is the first thing anybody runs, so it is
# the worst target to have fail with "column: not found".
	@awk -F':.*## ' '/^[a-z-]+:.*## /{printf "  %-11s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

generate: ## regenerate everything derived from a manifest
	$(PY) tools/gen_structure.py
	$(PY) tools/gen_sources.py
	$(PY) tools/ledger.py > /dev/null

# --- the gates ------------------------------------------------------------
#
# In cost order, cheapest first, so a convention mistake costs a second rather
# than a three-minute LaTeX run.

gates: ## every check that does not need a PDF
	@$(PY) tools/check_structure.py
	@$(PY) tools/check_generic.py
	@$(PY) tools/check_sources.py
	@$(PY) tools/check_figures.py
	@$(PY) tools/check_templates.py
	@$(PY) tools/check_links.py
	@$(PY) tools/ledger.py --check

mutations: ## prove the gates can fail -- run this when you add one
	@$(PY) tools/test_gates.py

# --- the build ------------------------------------------------------------

book: ## build the handbook
	$(LATEX) main.tex

cards: ## build the printable one-pagers
	@for c in $(CARDS); do \
	  (cd onepagers && $(LATEX) $$c.tex > /dev/null) || exit 1; \
	  pages=$$(grep -oE "Output written on $$c\.pdf \\([0-9]+ page" onepagers/$$c.log \
	           | grep -oE "[0-9]+" | tail -1); \
	  if [ "$$pages" != "1" ]; then \
	    echo "FAIL [cards] onepagers/$$c.pdf is $$pages pages."; \
	    echo "  A card is consulted under pressure. Two sides is a document."; \
	    exit 1; \
	  fi; \
	  echo "ok [card] $$c"; \
	done

check: ## read the build log properly -- never grep it
	@$(PY) tools/checklog.py main.log

ledger: ## print the ledger, reported and never gated
	@$(PY) tools/ledger.py

hooks: ## point git at the committed pre-commit hook
	@bash scripts/install-hooks.sh

secrets: ## the secret-scan CI job, run locally
	@bash scripts/scan-secrets.sh

watch: ## rebuild the handbook on every save
	latexmk -pdf -pvc -interaction=nonstopmode main.tex

clean: ## remove build artefacts
	latexmk -C main.tex > /dev/null 2>&1 || true
	@for c in $(CARDS); do (cd onepagers && latexmk -C $$c.tex > /dev/null 2>&1) || true; done
	rm -rf __pycache__ tools/__pycache__
