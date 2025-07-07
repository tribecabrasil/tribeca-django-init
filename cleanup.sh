#!/bin/bash
########################################################################
# Script Name: cleanup.sh
# Version: 1.0.0
# Date: 2025-06-26
# Author: Tribeca Team
# Description: Remove temporary build, test and crawl artifacts.
# Usage: ./cleanup.sh
# Exit codes: 0 (OK) | 1 (Error)
# Prerequisites: Unix-like OS, standard shell utilities
# Steps: 1. Remove predefined patterns
# See Also: docs/unified_dev_ops_guide.md
########################################################################
set -euo pipefail

echo "[INFO][$(date '+%Y-%m-%d %H:%M:%S')] Starting cleanup" 

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

echo "[INFO][$(date '+%Y-%m-%d %H:%M:%S')] Temporary build, test, and crawl artifacts cleaned."
