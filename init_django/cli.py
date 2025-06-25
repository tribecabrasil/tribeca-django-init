import os
import subprocess
import sys
from pathlib import Path
import click
from shutil import copyfile
from init_django import print_install_success

TEMPLATES_DIR = Path(__file__).parent / "templates"

def run(cmd, check=True):
    print(f"→ {cmd}")
    subprocess.run(cmd, shell=True, check=check)

@click.command()
def main():
    """
    CLI interativo para bootstrap de projetos Django seguindo convenções profissionais.
    """
    print_install_success()
    base = Path.cwd()
    venv = base / ".venv"
    click.echo("\nTribeca Django Init — Bootstrap interativo Django\n")

    # 1️⃣ Virtual environment
    click.echo("\n🌱  Step 1: Virtual Environment Setup")
    venv_choices = [
        "Reuse existing .venv",
        "Recreate .venv",
        "Skip this step"
    ]
    if venv.exists():
        venv_choice = click.prompt(
            "🌱 What do you want to do about the virtual environment (.venv)?\n" +
            "\n".join([f"{i+1}\u20e3  {opt}" for i, opt in enumerate(venv_choices)]),
            type=click.Choice([str(i+1) for i in range(len(venv_choices))]),
            default="1"
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
            "🌱 .venv not found.\n1\u20e3  Create new .venv\n2\u20e3  Skip this step\nEnter your choice:",
            type=click.Choice(["1", "2"]),
            default="1"
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
        "Skip this step"
    ]
    dep_choice = click.prompt(
        "📦 Which dependencies do you want to install?\n" +
        "\n".join([f"{i+1}\u20e3  {opt}" for i, opt in enumerate(dep_choices)]),
        type=click.Choice([str(i+1) for i in range(len(dep_choices))]),
        default="1"
    )
    if dep_choice == "1":
        django_version = click.prompt("🔢 Django version to install", default="5.2.3")
        run(f"{venv}/bin/pip install 'django~={django_version}' djangorestframework django-environ psycopg[binary] gunicorn whitenoise pytest-django black isort pre-commit")
    else:
        click.echo("Skipping dependency installation.")

    # 3. Git
    if (base / ".git").exists():
        click.echo("Repositório Git já inicializado.")
    else:
        if click.confirm("Inicializar repositório Git?", default=True):
            run("git init")
            run("curl -O https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore")
            run("git add . && git commit -m 'bootstrap'")

    # 4. Projeto Django
    if (base / "manage.py").exists():
        click.echo("Projeto Django já existe nesta pasta.")
    else:
        if click.confirm("Criar projeto Django na raiz (config)?", default=True):
            run(f"{venv}/bin/django-admin startproject config .")

    # 5. Settings particionados
    settings_dir = base / "config" / "settings"
    if settings_dir.exists():
        click.echo("Pacote de settings já existe.")
    else:
        if click.confirm("Estruturar settings como pacote (config/settings)?", default=True):
            os.makedirs(settings_dir)
            for f in ["base.py", "dev.py", "prod.py"]:
                copyfile(TEMPLATES_DIR / f"settings_{f}.tpl", settings_dir / f)
            with open(settings_dir / "__init__.py", "w") as f:
                f.write("from .dev import *  # default to dev")

    # 6. Primeiro app
    app_name = click.prompt("Nome do primeiro app (ex: users)", default="users")
    if (base / app_name).exists():
        click.echo(f"App '{app_name}' já existe.")
    else:
        if click.confirm(f"Criar app '{app_name}'?", default=True):
            run(f"{venv}/bin/python manage.py startapp {app_name}")

    # 7. README
    if (base / "README.md").exists():
        click.echo("README.md já existe.")
    else:
        copyfile(TEMPLATES_DIR / "readme.md.tpl", base / "README.md")

    # 8. Migrações
    if click.confirm("Aplicar migrações iniciais?", default=True):
        run(f"{venv}/bin/python manage.py migrate")

    click.echo(f"\n✅ Projeto inicializado/interativo concluído em {base.resolve()}\n")

    with open(settings_dir / "__init__.py", "w") as f:
        f.write("from .dev import *  # default to dev")

    # Cria primeiro app
    run(f"{venv}/bin/python manage.py startapp {app}")

    # Cria README com template
    copyfile(TEMPLATES_DIR / "readme.md.tpl", base / "README.md")

    # Primeiras migrações e runserver
    run(f"{venv}/bin/python manage.py migrate")
    print(f"\n✅ Projeto inicializado com sucesso em {base.resolve()}\n")

if __name__ == "__main__":
    main()
