"""CLI interface for MCPs/agents (non-interactive, arguments/flags, JSON output).
Always keep command compatibility and semantics in sync with ``cli_user.py``.
"""

import os
import sys
from pathlib import Path
from shutil import copyfile
from typing import Optional

import click

from init_django import print_install_success
from init_django.cli_common import TEMPLATES_DIR, emit_json_event, run


@click.command()
@click.option(
    "--json",
    "json_mode",
    is_flag=True,
    help="Emit output as JSON Lines (MCP/agent friendly)",
)
@click.option("--venv", type=click.Choice(["reuse", "recreate", "skip"]), default=None)
@click.option("--install-deps", type=click.Choice(["yes", "no"]), default=None)
@click.option("--django-version", default=None)
@click.option("--git-init", type=click.Choice(["yes", "no"]), default=None)
@click.option("--project", type=click.Choice(["yes", "no"]), default=None)
@click.option("--settings", type=click.Choice(["yes", "no"]), default=None)
@click.option("--app-name", default=None)
@click.option("--app-create", type=click.Choice(["yes", "no"]), default=None)
@click.option("--migrate", type=click.Choice(["yes", "no"]), default=None)
@click.option("--readme", type=click.Choice(["yes", "no"]), default=None)
def main(
    json_mode: bool,
    venv: Optional[str],
    install_deps: Optional[str],
    django_version: Optional[str],
    git_init: Optional[str],
    project: Optional[str],
    settings: Optional[str],
    app_name: Optional[str],
    app_create: Optional[str],
    migrate: Optional[str],
    readme: Optional[str],
) -> None:
    """MCP/agent CLI: non-interactive, argument-driven, emits JSON."""
    try:
        print_install_success()
        base = Path.cwd()
        venv_path = base / ".venv"
        emit_json_event("start", "success", "Bootstrap started", {"cwd": str(base)})

        # 1️⃣ Virtual environment
        venv_action = venv or "reuse" if venv_path.exists() else "recreate"
        if venv_action == "reuse" and venv_path.exists():
            emit_json_event(
                "virtualenv",
                "success",
                "Using existing .venv",
                {"path": str(venv_path)},
            )
        elif venv_action == "recreate":
            run("rm -rf .venv")
            run("python3 -m venv .venv")
            run(f"{venv_path}/bin/pip install --upgrade pip wheel")
            emit_json_event(
                "virtualenv", "success", ".venv recreated", {"path": str(venv_path)}
            )
        else:
            emit_json_event(
                "virtualenv", "skipped", "Skipped virtual environment setup", {}
            )

        # 2️⃣ Dependencies
        if install_deps == "yes":
            dj_version = django_version or "5.2.3"
            try:
                parts = dj_version.split(".")
                major = int(parts[0])
                if major < 3:
                    emit_json_event(
                        "dependencies",
                        "warning",
                        "Django version too old/invalid. Using default 5.2.3",
                        {},
                    )
                    dj_version = "5.2.3"
            except Exception:
                emit_json_event(
                    "dependencies",
                    "warning",
                    "Invalid Django version. Using default 5.2.3",
                    {},
                )
                dj_version = "5.2.3"
            if "." in dj_version and dj_version.count(".") == 2:
                django_spec = f"django=={dj_version}"
            else:
                django_spec = f"django~={dj_version}"
            run(
                f"{venv_path}/bin/pip install '{django_spec}' "
                "djangorestframework django-environ psycopg[binary] "
                "gunicorn whitenoise pytest-django black isort pre-commit"
            )
            emit_json_event(
                "dependencies",
                "success",
                "Dependencies installed",
                {"django": dj_version},
            )
        else:
            emit_json_event(
                "dependencies", "skipped", "Dependency installation skipped", {}
            )

        # 3. Git
        if (base / ".git").exists():
            emit_json_event("git", "success", "Git repository already initialized", {})
        elif git_init == "yes":
            run("git init")
            run(
                "curl -O "
                "https://raw.githubusercontent.com/github/gitignore/main/"
                "Python.gitignore"
            )
            run("git add . && git commit -m 'bootstrap'")
            emit_json_event("git", "success", "Git initialized", {})
        else:
            emit_json_event("git", "skipped", "Git initialization skipped", {})

        # 4. Django project
        if (base / "manage.py").exists():
            emit_json_event("project", "success", "Django project already exists", {})
        elif project == "yes":
            run(f"{venv_path}/bin/django-admin startproject config .")
            req_tpl = TEMPLATES_DIR / "requirements.txt"
            req_target = base / "requirements.txt"
            if req_tpl.exists() and not req_target.exists():
                copyfile(req_tpl, req_target)
                emit_json_event(
                    "requirements",
                    "success",
                    "requirements.txt created from template",
                    {"path": str(req_target)},
                )
            settings_dir = base / "config" / "settings"
            if settings_dir.exists():
                emit_json_event(
                    "settings",
                    "success",
                    "Settings package already exists",
                    {"path": str(settings_dir)},
                )
            elif settings == "yes":
                os.makedirs(settings_dir)
                for fname in ["base.py", "dev.py", "prod.py"]:
                    copyfile(
                        TEMPLATES_DIR / "settings" / f"{fname}.tpl",
                        settings_dir / fname,
                    )
                with open(settings_dir / "__init__.py", "w") as fh:
                    fh.write("from .dev import *  # default to dev")
                with open(base / "config" / "wsgi.py", "r+") as fh:
                    content = fh.read()
                    fh.seek(0)
                    fh.write(content.replace("config.settings", "config.settings.dev"))
                emit_json_event(
                    "settings",
                    "success",
                    "Settings package created",
                    {"path": str(settings_dir)},
                )
            else:
                emit_json_event(
                    "settings", "skipped", "Skipped settings package creation", {}
                )
            # App
            app = app_name or "users"
            if (base / app).exists():
                emit_json_event(
                    "app", "success", f"App '{app}' already exists", {"name": app}
                )
            elif app_create == "yes":
                run(f"{venv_path}/bin/python manage.py startapp {app}")
                if migrate == "yes":
                    run(f"{venv_path}/bin/python manage.py migrate")
                    emit_json_event(
                        "migrations", "success", "Initial migrations applied", {}
                    )
                else:
                    emit_json_event("migrations", "skipped", "Skipped migrations", {})
            else:
                emit_json_event(
                    "app", "skipped", f"Skipped creation of app '{app}'", {"name": app}
                )
            # README
            if (base / "README.md").exists():
                emit_json_event("readme", "success", "README.md already exists", {})
            elif readme == "yes":
                copyfile(TEMPLATES_DIR / "readme.md.tpl", base / "README.md")
                emit_json_event(
                    "readme",
                    "success",
                    "README.md created from template",
                    {"path": str(base / "README.md")},
                )
            else:
                emit_json_event("readme", "skipped", "Skipped README creation", {})
        else:
            emit_json_event("project", "skipped", "Skipped Django project creation", {})
        emit_json_event(
            "done",
            "success",
            "Project initialization/interactive flow completed",
            {"project_root": str(base.resolve())},
        )
    except Exception as e:
        import traceback

        emit_json_event(
            "error",
            "error",
            f"Error: {e}",
            {"traceback": traceback.format_exc()},
            error_code="UNHANDLED_EXCEPTION",
        )
        sys.exit(1)
