"""
Funções utilitárias e lógica compartilhada entre interfaces CLI (usuário e MCP).
Sempre que um comando for adicionado ou alterado, garanta que ambos cli_user.py e cli_mcp.py estejam compatíveis com a mesma API e semântica.
"""
import os
import subprocess
from pathlib import Path
from shutil import copyfile
from typing import Any, Dict, Optional

import click
import json
from datetime import datetime, timezone

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

# Outras funções utilitárias compartilhadas podem ser adicionadas aqui.
