#!/usr/bin/env bash
# Point git at the hooks that are committed, rather than asking every
# contributor to copy a file into .git/ by hand and remember to do it again
# after a fresh clone.
set -euo pipefail

cd "$(dirname "$0")/.."
git config core.hooksPath scripts/hooks
chmod +x scripts/hooks/* scripts/*.sh
echo "core.hooksPath -> scripts/hooks"
echo "Installed: $(ls scripts/hooks | tr '\n' ' ')"
