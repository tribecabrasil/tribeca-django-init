# Unified Development and Operations Guide

This guide consolidates recommended practices for shell scripts, Python/Django projects, and CI/CD workflows. It serves as a reference for both human developers and AI agents working on Tribeca Django Init.

## 1. Principles
- **Clean Code**
- **Modularity**
- **Living Documentation**
- **Security by Design**
- **Performance Awareness**

## 2. Shell Scripts

### 2.1 Standard Header
Include the following metadata block at the top of every shell script:
```bash
########################################################################
# Script Name: <name>
# Version: x.y.z
# Date: YYYY-MM-DD
# Author: <team>
# Description: <purpose>
# Usage: <examples>
# Exit codes: 0 (OK) | 1 (Error)
# Prerequisites: OS, dependencies, root
# Steps: 1. …
# See Also: useful links
########################################################################
```

### 2.2 Size Limits
| Item  | Limit |
|-------|-------|
| File  | ≤ 600 lines |
| Refactor starting from | 400 lines |
| AI chunk | ≤ 300 lines |

### 2.3 Safe Flow
- Always enable `set -e`.
- Validate prerequisites.
- Create backups or rollback steps before destructive actions.

### 2.4 Comments
- Briefly describe each logical block.
- Use `[INFO][YYYY-MM-DD HH:MM:SS]` messages for progress logs.

## 3. Python/Django Projects

### 3.1 Conventions
- Python ≥ 3.10.
- PEP 8 style with Black (88 char line length).
- `snake_case` for functions and variables, `PascalCase` for classes.
- Full type annotations (PEP 484/526).

### 3.2 Limits
| Item  | Limit |
|-------|-------|
| File  | ≤ 500 lines |
| Refactor starting from | 300 lines |
| AI chunk | ≤ 200 lines |

### 3.3 Module Structure
- One module per objective.
- One function per action.
- Use `async/await` when needed.

### 3.4 Docstrings
```python
def clean_text(text: str) -> str:
    """Remove undesired characters and extra spaces."""
```

### 3.5 Tests
```bash
pytest tests/
pytest --cov=tribeca_insights  # minimum 90% coverage
```

### 3.6 Pull Requests
1. Objective description and related issue.
2. One logical change per PR.
3. All checks must pass.

### 3.7 Pre-commit (mandatory)
Configure `.pre-commit-config.yaml` with:
1. `black`
2. `isort`
3. `flake8`
4. `mypy` (optional)
5. `pytest` (smoke)

Failures block commits.

## 4. CI/CD
- Run lint, tests, and coverage in pull requests.
- Block merge when coverage < 90%.
- Enable secret scanning.

## 5. Updates
Include all new practices in this guide via documentation pull requests.
