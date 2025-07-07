"""CLI interface for MCPs/agents (non-interactive, arguments/flags, JSON output).
Always keep command compatibility and semantics in sync with ``cli_user.py``.
"""

import sys
from pathlib import Path
from shutil import copyfile
from typing import Optional

import click

from init_django import print_install_success
from init_django.cli_common import (
    TEMPLATES_DIR,
    apply_migrations,
    create_app,
    create_readme,
    create_env_file,
    create_settings_package,
    create_virtualenv,
    emit_json_event,
    initialize_git,
    install_dependencies,
    run,
    start_django_project,
)


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
@click.option("--env-file", type=click.Choice(["yes", "no"]), default=None)
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
    env_file: Optional[str],
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
            create_virtualenv(venv_path)
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
            install_dependencies(venv_path, dj_version)
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
            initialize_git()
            emit_json_event("git", "success", "Git initialized", {})
        else:
            emit_json_event("git", "skipped", "Git initialization skipped", {})

        # 4. Django project
        if (base / "manage.py").exists():
            emit_json_event("project", "success", "Django project already exists", {})
        elif project == "yes":
            start_django_project(venv_path, base, json_mode=json_mode)
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
                create_settings_package(base)
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
                create_app(venv_path, app)
                if migrate == "yes":
                    apply_migrations(venv_path)
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
                create_readme(base)
                emit_json_event(
                    "readme",
                    "success",
                    "README.md created from template",
                    {"path": str(base / "README.md")},
                )
            else:
                emit_json_event("readme", "skipped", "Skipped README creation", {})

            # .env file
            if (base / ".env").exists():
                emit_json_event(
                    "env_file",
                    "success",
                    ".env already exists",
                    {"path": str(base / ".env")},
                )
            elif env_file == "yes":
                create_env_file(base)
                emit_json_event(
                    "env_file",
                    "success",
                    ".env created from template",
                    {"path": str(base / ".env")},
                )
            else:
                emit_json_event("env_file", "skipped", "Skipped .env creation", {})
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
