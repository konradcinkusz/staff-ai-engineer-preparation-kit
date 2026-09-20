#!/usr/bin/env bash
# The secret-scan CI job, reproducible locally, so that "it passed on my
# machine" means the same thing the runner means.
#
# Same config, same scanner, same scope. The only difference is that CI also
# scans the full history on a schedule; this scans what you have.
set -euo pipefail

cd "$(dirname "$0")/.."

if ! command -v gitleaks >/dev/null 2>&1; then
  echo "gitleaks is not installed." >&2
  echo "  https://github.com/gitleaks/gitleaks -- or run the CI job instead." >&2
  exit 2
fi

mode="${1:-history}"
case "$mode" in
  history) exec gitleaks detect --config .gitleaks.toml --redact --verbose ;;
  staged)  exec gitleaks protect --staged --config .gitleaks.toml --redact --verbose ;;
  *) echo "usage: $0 [history|staged]" >&2; exit 64 ;;
esac
