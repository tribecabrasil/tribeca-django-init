"""Utility functions and shared logic for both CLI interfaces (user and MCP).

Whenever a command is added or modified, ensure ``cli_user.py`` and ``cli_mcp.py``
remain compatible with the same API and semantics.
"""

import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from shutil import copyfile
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


def create_virtualenv(venv_path: Path) -> None:
    """Create a Python virtual environment and upgrade tooling."""

    run(f"python3 -m venv {venv_path}")
    run(f"{venv_path}/bin/pip install --upgrade pip wheel")


def install_dependencies(venv_path: Path, django_version: str) -> None:
    """Install Django and common packages into ``venv_path``."""

    if "." in django_version and django_version.count(".") == 2:
        django_spec = f"django=={django_version}"
    else:
        django_spec = f"django~={django_version}"
    run(
        f"{venv_path}/bin/pip install '{django_spec}' "
        "djangorestframework django-environ psycopg[binary] "
        "gunicorn whitenoise pytest-django black isort pre-commit"
    )


def initialize_git() -> None:
    """Initialize a git repository with a standard Python ``.gitignore``."""

    run("git init")
    gitignore_src = TEMPLATES_DIR / "Python.gitignore"
    if gitignore_src.exists():
        copyfile(gitignore_src, "Python.gitignore")
    run("git add . && git commit -m 'bootstrap'")


def start_django_project(venv_path: Path, base: Path, json_mode: bool = False) -> None:
    """Create the base Django project in ``base`` using ``venv_path``.

    Parameters
    ----------
    venv_path:
        The virtualenv that should contain ``django-admin``.
    base:
        Directory where the project will be created.
    json_mode:
        Emit a JSON event instead of printing when ``True``.
    """

    django_admin = venv_path / "bin" / "django-admin"
    if not django_admin.exists():
        msg = (
            f"django-admin not found in {venv_path}. "
            "Install dependencies first."
        )
        if json_mode:
            emit_json_event(
                "project",
                "error",
                msg,
                {"venv": str(venv_path)},
                error_code="DJANGO_ADMIN_MISSING",
            )
        else:
            click.echo(f"❌ {msg}")
        raise click.ClickException(msg)

    run(f"{django_admin} startproject config .")


def create_settings_package(base: Path) -> None:
    """Generate the ``config/settings`` package from templates."""

    settings_dir = base / "config" / "settings"
    os.makedirs(settings_dir, exist_ok=True)
    for fname in ["base.py", "dev.py", "prod.py"]:
        copyfile(TEMPLATES_DIR / "settings" / f"{fname}.tpl", settings_dir / fname)
    with open(settings_dir / "__init__.py", "w") as fh:
        fh.write("from .dev import *  # default to dev")
    with open(base / "config" / "wsgi.py", "r+") as fh:
        content = fh.read()
        fh.seek(0)
        fh.write(content.replace("config.settings", "config.settings.dev"))


def create_app(venv_path: Path, app: str) -> None:
    """Create a Django app named ``app`` using the given virtualenv."""

    run(f"{venv_path}/bin/python manage.py startapp {app}")


def apply_migrations(venv_path: Path) -> None:
    """Apply initial Django migrations using ``venv_path``."""

    run(f"{venv_path}/bin/python manage.py migrate")


def create_readme(base: Path) -> None:
    """Create ``README.md`` from the packaged template."""

    copyfile(TEMPLATES_DIR / "readme.md.tpl", base / "README.md")


def create_env_file(base: Path) -> None:
    """Copy ``.env.example`` to ``.env`` in ``base`` if missing."""

    src = TEMPLATES_DIR / ".env.example"
    dest = base / ".env"
    if not dest.exists() and src.exists():
        copyfile(src, dest)
