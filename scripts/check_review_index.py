#!/usr/bin/env python3
"""Pre-commit hook to ensure review/indexReview.md is updated."""

import subprocess
import sys
from pathlib import Path

INDEX_PATH = Path("review/indexReview.md")


def review_index_modified() -> bool:
    """Return True if the review index is staged for commit."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True,
        text=True,
        check=False,
    )
    staged_files = result.stdout.splitlines()
    return str(INDEX_PATH) in staged_files


def main() -> None:
    if not review_index_modified():
        print(
            "❌  review/indexReview.md não foi atualizado.\n"
            "🚨  Atualize o índice de revisões antes de realizar o commit.\n"
            "ℹ️  Consulte review/indexReview.md e AGENTS.md para detalhes."
        )
        sys.exit(1)
    print("✅  Index de revisões atualizado. Obrigado por manter o histórico!")


if __name__ == "__main__":
    main()
