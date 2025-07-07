# Integration with MCPs (Multi-Component Platforms / AI Agents)

This guide explains how to make the Tribeca Django Init CLI fully automation friendly and suitable for AI agents and other platforms.

## Overview
The CLI is designed for both humans and intelligent automation tools. Key goals include:
- Non‑interactive execution through flags and arguments
- Predictable, structured prompts and output
- Clear documentation for third‑party integration
- Automated tests covering both human and JSON/MCP modes

## CLI Architecture: Human and MCP Interfaces
The Tribeca Django Init CLI offers two synchronized entry points:

- `cli_user.py`: traditional interactive mode with friendly prompts
- `cli_mcp.py`: non‑interactive mode that accepts flags and produces JSON output
- All utility and business logic lives in `cli_common.py` so both modes share the same API and semantics

**Important**: whenever a new feature or command is added, it must exist in both interfaces (`cli_user.py` and `cli_mcp.py`).

- `cli.py` detects which mode to run and delegates accordingly
- Both interfaces accept the same commands and options; only the interaction style changes
- Tests and documentation must cover both modes

## JSON Mode (`--json`)
When the `--json` flag is provided, the CLI emits structured JSON describing each step. This allows easy parsing by automation tools.

### Example usage
```bash
tribeca-django-init ... --json
```

### Example JSON output
```json
{
  "step": "virtualenv",
  "status": "created",
  "path": "/home/user/project/.venv"
}
{
  "step": "dependencies",
  "status": "installed",
  "packages": ["django==5.2.3", "djangorestframework", ...]
}
{
  "step": "settings",
  "status": "generated",
  "files": ["config/settings/base.py", ...]
}
{
  "step": "done",
  "status": "success",
  "project_root": "/home/user/project"
}
```

- Each relevant step outputs a JSON object
- On error, a JSON object with `status: error` and a message is produced
- Ideal for MCPs, CI/CD pipelines, and intelligent agents

## Roadmap and Planned Features

### 1. Non‑Interactive / Automatable Mode
- Allow running the CLI entirely via command‑line flags (e.g. `--language-code`, `--timezone`, `--no-input`)
- Example:
  ```bash
  tribeca-django-init --language-code en --second-language pt-br --timezone America/Sao_Paulo --no-input
  ```

### 2. Structured Prompts and Output
- Ensure prompts and CLI output are clear and easily parsed
- Optional: provide JSON or other machine‑friendly output formats

### 3. Documentation for Agents/MCPs
- Dedicated sections in `README` and `AGENTS.md` showing integration examples
- Automation snippets, CI/CD pipelines, and agent workflows

### 4. Automated Tests for Agent Use
- Tests that verify the CLI works in headless or CI environments
- Idempotency and robustness checks

### 5. Integration Best Practices
- Recommendations for safe integration in pipelines
- Suggested patterns for responses and error handling

---

## Documentation Reference
Support for MCPs is under active development. See the backlog and the "AI, Automation and MCPs" section for progress.

---

Feel free to contribute ideas, examples, or open issues about MCP integration!

