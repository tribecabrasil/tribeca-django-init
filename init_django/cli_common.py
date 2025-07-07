"""Utility functions and shared logic for both CLI interfaces (user and MCP).

Whenever a command is added or modified, ensure ``cli_user.py`` and ``cli_mcp.py``
remain compatible with the same API and semantics.
"""

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

import click


def run(cmd: str, check: bool = True) -> None:
    """Run a shell command and echo its output.

    Parameters
    ----------
    cmd:
        Command string to execute.
    check:
        If ``True``, raise an exception when the command exits with a non-zero
        status.
    """

    click.echo(f"→ {cmd}")
    try:
        completed = subprocess.run(
            cmd, shell=True, check=check, capture_output=True, text=True
        )
        if completed.stdout:
            click.echo(completed.stdout)
        if completed.stderr:
            click.echo(completed.stderr, err=True)
    except subprocess.CalledProcessError as e:
        click.echo(f"[ERROR] Command failed: {cmd}", err=True)
        click.echo(f"Return code: {e.returncode}", err=True)
        if e.stdout:
            click.echo("[stdout]", err=True)
            click.echo(e.stdout, err=True)
        if e.stderr:
            click.echo("[stderr]", err=True)
            click.echo(e.stderr, err=True)
        raise


def emit_json_event(
    event: str,
    status: str,
    message: str,
    data: Optional[Dict[str, Any]] = None,
    error_code: Optional[str] = None,
) -> None:
    """Emit a JSON event for consumption by agents or CI/CD.

    Parameters
    ----------
    event:
        Event name, e.g. ``"git"`` or ``"virtualenv"``.
    status:
        Status string such as ``"success"`` or ``"error"``.
    message:
        Human readable message describing the event.
    data:
        Optional payload with additional information.
    error_code:
        Optional error code when ``status`` represents a failure.
    """

    obj: Dict[str, Any] = {
        "event": event,
        "status": status,
        "message": message,
        "data": data or {},
        "ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    if error_code:
        obj["error_code"] = error_code
    print(json.dumps(obj), flush=True)


TEMPLATES_DIR = Path(__file__).parent / "templates"

# Additional shared utility functions can be added here.
