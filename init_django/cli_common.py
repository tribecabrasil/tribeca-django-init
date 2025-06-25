"""
Funções utilitárias e lógica compartilhada entre interfaces CLI (usuário e MCP).
Sempre que um comando for adicionado ou alterado, garanta que ambos cli_user.py e cli_mcp.py estejam compatíveis com a mesma API e semântica.
"""
import os
import subprocess
from pathlib import Path
from shutil import copyfile
import click
import json
from datetime import datetime, timezone

def run(cmd, check=True):
    click.echo(f"→ {cmd}")
    try:
        completed = subprocess.run(cmd, shell=True, check=check, capture_output=True, text=True)
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

def emit_json_event(event, status, message, data=None, error_code=None):
    obj = {
        "event": event,
        "status": status,
        "message": message,
        "data": data or {},
        "ts": datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
    }
    if error_code:
        obj["error_code"] = error_code
    print(json.dumps(obj), flush=True)

TEMPLATES_DIR = Path(__file__).parent / "templates"

# Outras funções utilitárias compartilhadas podem ser adicionadas aqui.
