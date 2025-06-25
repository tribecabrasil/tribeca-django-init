# Tribeca Django Init

Interactive CLI for bootstrapping Django projects according to the latest ecosystem best practices (2025).

## What does it do?
This CLI automates and documents, step by step, the creation of modern Django projects, interacting with you at each stage:

- Creation or reuse of a local virtual environment (`.venv`)
- Installation of minimal and quality dependencies (Django, Django REST Framework, django-environ, psycopg[binary], gunicorn, whitenoise, pytest-django, black, isort, pre-commit)
- Git repository initialization and download of the official Python `.gitignore`
- Django project creation at the root (`config`)
- Partitioned settings structure (`config/settings/` with `base.py`, `dev.py`, `prod.py`)
- Creation of the first isolated app
- Applying initial migrations
- README generation and production-ready structure

## Interactive Flow
The CLI detects already existing resources (venv, git, settings, apps) and allows you to skip or customize steps, making bootstrap safe and flexible for both new and partially configured environments.

Sample prompts:
- Virtual environment (.venv) already exists. Reuse it?
- Install minimal project dependencies?
- Initialize Git repository?
- Create Django project at root (config)?
- Partition settings as a package (config/settings)?
- Name of the first app (e.g., users)
- Apply initial migrations?

## How to use

```bash
pip install -e .
init-django
```

Follow the interactive instructions in the terminal.

## Generated Structure
```
config/
  settings/
    __init__.py
    base.py
    dev.py
    prod.py
manage.py
.venv/
.git/
README.md
```

## Convenções e boas práticas
- Django 5.2+ (LTS) e Python 3.12/3.13
- settings desacoplados
- ambiente reprodutível
- apps pequenos e isolados
- qualidade de código automatizada
- pronto para deploy em produção

## Referências
- [cookiecutter-django](https://github.com/cookiecutter/cookiecutter-django)
- [Django Project](https://www.djangoproject.com/)
- [PEP-257](https://peps.python.org/pep-0257/)

---

> Gerado por `Tribeca Django Init` — mantenha seu bootstrap sempre atualizado!
