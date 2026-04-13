#!/usr/bin/env bash
# .scripts/generate-marketplace.sh
# Generates .claude-plugin/marketplace.json from skill directories.
# Delegates to generate-marketplace.py (Python 3.8+, no third-party deps required).

set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"

python3 "$repo_root/.scripts/generate-marketplace.py"
