#!/bin/bash
set -euo pipefail

# Remove Python build/test artifacts
declare -a patterns=(
  "build/" "dist/" ".pytest_cache/" "*.egg-info/" "**/*.egg-info/"
  ".mypy_cache/" ".coverage" ".cache/" ".tox/" ".hypothesis/"
  "__pycache__/" "**/__pycache__/" ".vscode/" ".idea/" "*.iml"
  "logs/" "*.log"
  "visited_urls_*.csv" "*/pages_md" "*/pages_json" "*.com/"
)

for p in "${patterns[@]}"; do
  rm -rf $p 2>/dev/null || true
done

printf "Temporary build, test, and crawl artifacts cleaned.\n"
