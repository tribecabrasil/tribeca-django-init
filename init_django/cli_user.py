"""Traditional CLI interface for human users with interactive prompts.
Always keep command compatibility and semantics in sync with ``cli_mcp.py``.
"""

from pathlib import Path
import click
from init_django.cli_common import run, TEMPLATES_DIR
from init_django import print_install_success
import os
from shutil import copyfile


@click.command()
def main():
    """Interactive CLI to bootstrap Django projects following best practices."""
    print_install_success()
    base = Path.cwd()
    venv = base / ".venv"
    click.echo("\nTribeca Django Init — Interactive Django Bootstrap\n")

    # 1️⃣ Virtual environment
    click.echo("\n🌱  Step 1: Virtual Environment Setup")
    venv_choices = ["Reuse existing .venv", "Recreate .venv", "Skip this step"]
    if venv.exists():
        venv_choice = click.prompt(
            "🌱 What do you want to do about the virtual environment (.venv)?\n"
            + "\n".join([f"{i+1}\u20e3  {opt}" for i, opt in enumerate(venv_choices)]),
            type=click.Choice([str(i + 1) for i in range(len(venv_choices))]),
            default="1",
        )
        if venv_choice == "1":
            click.echo("Using existing .venv.")
        elif venv_choice == "2":
            run("rm -rf .venv")
            run("python3 -m venv .venv")
            run(f"{venv}/bin/pip install --upgrade pip wheel")
        else:
            click.echo("Skipping virtual environment setup.")
    else:
        create_venv = click.prompt(
            "🌱 .venv not found.\n"
            "1\u20e3  Create new .venv\n"
            "2\u20e3  Skip this step\n"
            "Enter your choice:",
            type=click.Choice(["1", "2"]),
            default="1",
        )
        if create_venv == "1":
            run("python3 -m venv .venv")
            run(f"{venv}/bin/pip install --upgrade pip wheel")
        else:
            click.echo("Skipping virtual environment setup.")

    # 2️⃣ Dependencies
    click.echo("\n📦  Step 2: Install Dependencies")
    dep_choices = [
        "Install minimal and quality dependencies (incl. Django REST Framework)",
        "Skip this step",
    ]
    dep_choice = click.prompt(
        "📦 Which dependencies do you want to install?\n"
        + "\n".join([f"{i+1}\u20e3  {opt}" for i, opt in enumerate(dep_choices)]),
        type=click.Choice([str(i + 1) for i in range(len(dep_choices))]),
        default="1",
    )
    if dep_choice == "1":
        django_version = click.prompt("🔢 Django version to install", default="5.2.3")
        try:
            parts = django_version.split(".")
            major = int(parts[0])
            if major < 3:
                click.echo(
                    "⚠️  Django version too old or invalid. Using default 5.2.3."
                )
                django_version = "5.2.3"
        except Exception:
            click.echo("⚠️  Invalid Django version. Using default 5.2.3.")
            django_version = "5.2.3"
        if "." in django_version and django_version.count(".") == 2:
            django_spec = f"django=={django_version}"
        else:
            django_spec = f"django~={django_version}"
        cmd = (
            f"{venv}/bin/pip install '{django_spec}' "
            "djangorestframework django-environ psycopg[binary] "
            "gunicorn whitenoise pytest-django black isort pre-commit"
        )
        run(cmd)
    else:
        click.echo("Skipping dependency installation.")

    # 3. Git
    if (base / ".git").exists():
        click.echo("Git repository already initialized.")
    else:
        git_choice = click.prompt(
            "3️⃣  Git repository setup\n"
            "1\u20e3  Initialize git repository\n"
            "2\u20e3  Skip this step\n"
            "Enter your choice:",
            type=click.Choice(["1", "2"]),
            default="1",
        )
        if git_choice == "1":
            run("git init")
            run(
                "curl -O https://raw.githubusercontent.com/"
                "github/gitignore/main/Python.gitignore"
            )
            run("git add . && git commit -m 'bootstrap'")
        else:
            click.echo("Skipping git initialization.")

    # 4. Django project
    if (base / "manage.py").exists():
        click.echo("Django project already exists in this folder.")
    else:
        proj_choice = click.prompt(
            "4️⃣  Django project setup\n"
            "1\u20e3  Create Django project (config)\n"
            "2\u20e3  Skip this step\n"
            "Enter your choice:",
            type=click.Choice(["1", "2"]),
            default="1",
        )
        if proj_choice == "1":
            run(f"{venv}/bin/django-admin startproject config .")
            req_tpl = TEMPLATES_DIR / "requirements.txt"
            req_target = base / "requirements.txt"
            if req_tpl.exists() and not req_target.exists():
                copyfile(req_tpl, req_target)
                click.echo("requirements.txt created from template.")

            settings_dir = base / "config" / "settings"
            if settings_dir.exists():
                click.echo("Settings package already exists.")
            else:
                settings_choice = click.prompt(
                    "5️⃣  Settings package setup\n"
                    "1️⃣  Create settings package (config/settings)\n"
                    "2️⃣  Skip this step\n"
                    "Enter your choice:",
                    type=click.Choice(["1", "2"]),
                    default="1",
                )
                if settings_choice == "1":
                    os.makedirs(settings_dir)
                    for f in ["base.py", "dev.py", "prod.py"]:
                        copyfile(
                            TEMPLATES_DIR / "settings" / f"{f}.tpl", settings_dir / f
                        )
                    with open(settings_dir / "__init__.py", "w") as f:
                        f.write("from .dev import *  # default to dev")
                    with open(base / "config" / "wsgi.py", "r+") as f:
                        content = f.read()
                        f.seek(0)
                        f.write(
                            content.replace("config.settings", "config.settings.dev")
                        )
                else:
                    click.echo("Skipping settings package creation.")

            app_name = click.prompt(
                "Name of the first app (e.g., users)", default="users"
            )
            if (base / app_name).exists():
                click.echo(f"App '{app_name}' already exists.")
            else:
                app_choice = click.prompt(
                    f"6️⃣  App creation\n"
                    f"1️⃣  Create app '{app_name}'\n"
                    "2️⃣  Skip this step\n"
                    "Enter your choice:",
                    type=click.Choice(["1", "2"]),
                    default="1",
                )
                if app_choice == "1":
                    run(f"{venv}/bin/python manage.py startapp {app_name}")
                    migrations_choice = click.prompt(
                        "7️⃣  Run migrations\n"
                        "1️⃣  Run initial migrations\n"
                        "2️⃣  Skip this step\n"
                        "Enter your choice:",
                        type=click.Choice(["1", "2"]),
                        default="1",
                    )
                    if migrations_choice == "1":
                        run(f"{venv}/bin/python manage.py migrate")
                    else:
                        click.echo("Skipping migrations.")
                else:
                    click.echo(f"Skipping creation of app '{app_name}'.")

            if (base / "README.md").exists():
                click.echo("README.md already exists.")
            else:
                copyfile(TEMPLATES_DIR / "readme.md.tpl", base / "README.md")
                click.echo("README.md created from template.")
        else:
            click.echo("Skipping Django project creation.")

    click.echo(
        f"\n✅ Project initialization/interactive flow completed in "
        f"{base.resolve()}\n"
    )
