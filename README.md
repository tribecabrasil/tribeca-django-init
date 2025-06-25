# Tribeca Django Init — MCPs & Agents Ready 🚀🤖

[![Build Status](https://img.shields.io/github/actions/workflow/status/tribecabrasil/tribeca-django-init/ci.yml?branch=main)](https://github.com/tribecabrasil/tribeca-django-init/actions)
[![Coverage Status](https://img.shields.io/codecov/c/github/tribecabrasil/tribeca-django-init)](https://codecov.io/gh/tribecabrasil/tribeca-django-init)
[![License](https://img.shields.io/github/license/tribecabrasil/tribeca-django-init)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/django-5.2%2B-green)](https://www.djangoproject.com/)

> **The next-gen Django project bootstrapper for humans, CI/CD, and AI agents.**
> 
> **Full compatibility with Multi-Component Platforms (MCPs), automation, and intelligent workflows.**

---

## 🚀 Overview
Tribeca Django Init is a fully interactive CLI that automates the creation of robust Django projects, following the latest standards for API-first, maintainable, and scalable web applications.

---

## 🏷️ Recommended Tags

django, cli, bootstrap, automation, mcp, ai-agents, devops, ci-cd, rest-api, production-ready, project-generator, python, template, best-practices, internationalization, i18n, scaffold, json, modern

---

## 📢 Project Description

**Short:**
> Next-gen Django project bootstrapper — interactive, agent-ready, CI/CD-friendly, and production-focused. Full support for MCPs, automation, and best practices.

**Long:**
> Tribeca Django Init is a modern, interactive CLI for bootstrapping Django projects with production-ready structure, automation, and best practices. Designed for seamless integration with Multi-Component Platforms (MCPs), AI agents, and CI/CD pipelines, it offers both human-friendly prompts and a robust JSON mode for headless, scriptable workflows.
>
> - Dual-mode CLI: interactive for humans, JSON/flags for agents and automation
> - Compatible with AI agents and modern DevOps workflows
> - Instantly creates projects with Django REST, i18n, and scalable settings
> - Standardizes best practices for security, maintainability, and deployment
> - Easily extendable and future-proof for evolving automation needs

---

- Fast bootstrap with numbered choices, emojis, and clear prompts
- Installs Django 5.2+, Django REST Framework, and a modern stack
- Modular settings structure: `settings/base.py.tpl` (base), `settings/dev.py.tpl` (development), `settings/prod.py.tpl` (production)
- Uses django-environ and .env for environment-based configuration
- Automated quality tools and CI/CD ready
- Documentation and templates in English, ready for international teams

---

## 🛠️ Stack
- **Python** 3.12+
- **Django** 5.2+
- **Django REST Framework**
- **PostgreSQL** (default, easily swappable)
- **pytest-django**, **black**, **isort**, **pre-commit**
- **Whitenoise**, **gunicorn**, **django-environ**

---

## 📦 Installation

```bash
# Clone the repo
 git clone https://github.com/tribecabrasil/tribeca-django-init.git
 cd tribeca-django-init

# (Recommended) Create and activate a virtualenv
 python3 -m venv .venv
 source .venv/bin/activate

# Install in editable mode
 pip install -e .
```

---

## 💡 Usage

### Human Mode (Interactive)

To use the CLI in the traditional way, simply run:

```bash
python -m init_django.cli_user
```

You will be guided by interactive prompts, with friendly messages and visual context.

### MCP / JSON Mode (Automation, Agents)

For integration with MCPs, automation, or agents, use the non-interactive/JSON mode:

```bash
python -m init_django.cli_mcp --json --venv recreate --install-deps yes --django-version 5.2.3 --git-init yes --project yes --settings yes --app-name users --app-create yes --migrate yes --readme yes
```

Each step will emit a structured JSON line, for example:

```json
{"event": "virtualenv", "status": "success", "message": ".venv recreated", "data": {"path": "/project/path/.venv"}, "ts": "2025-06-25T07:00:00Z"}
```

See more examples and explanations in [docs/mcps_documentation.md](docs/mcps_documentation.md).
- The CLI will guide you through each step: venv, dependencies, git, project, settings, app, migrations, and docs

---

## 🔧 Troubleshooting

- **Command not found**: Ensure you have activated the virtual environment (`source .venv/bin/activate`) and installed the package in editable mode (`pip install -e .`).
- **Test Failures**: If you are contributing and encounter test failures, please see `AGENTS.md` for detailed guidance on debugging common issues related to CLI input alignment and Django settings.

---

## 🏗️ Example Project Structure
```text
config/
  settings/
    __init__.py
    base.py  # Generated from settings/base.py.tpl
    dev.py   # Generated from settings/dev.py.tpl
    prod.py  # Generated from settings/prod.py.tpl
manage.py
.venv/
.git/
README.md
.env  # Your environment variables (see .env.example)
```

### Settings Templates
- All Django settings are generated from templates in `init_django/templates/`:
  - `settings/base.py.tpl` → `config/settings/base.py`
  - `settings/dev.py.tpl` → `config/settings/dev.py`
  - `settings/prod.py.tpl` → `config/settings/prod.py`
- The CLI will copy and configure these automatically.

### Environment Variables & django-environ
- The project uses [django-environ](https://django-environ.readthedocs.io/) for configuration.
- Create a `.env` file in your project root (see `.env.example` for guidance).
- Typical variables:
  - `DJANGO_SECRET_KEY`, `DEBUG`, `DJANGO_ALLOWED_HOSTS`, `DATABASE_URL`, etc.
- This approach keeps secrets and environment-specific config out of version control and enables safe, Twelve-Factor deployments.
```

---

## ✨ Features
- Interactive, emoji-powered CLI
- Detects and reuses existing resources
- Modern, production-ready Django setup
- DRF and quality tools included by default
- All docs, templates, and code in English
- Ready for CI/CD and cloud deployment

---

## 🤝 Contributing
Pull requests and suggestions are welcome! For major changes, please open an issue first to discuss what you would like to change.

- Follow the project standards in [AGENTS.md](AGENTS.md)
- Use English for all documentation and code
- Update/add tests in `tests/` when relevant

---

## 📚 Documentation

### Integration with MCPs (Multi-Component Platforms/AI agents)
Support and compatibility with MCPs is already under active planning. See details, examples, and roadmap in [`docs/mcps_documentation.md`](docs/mcps_documentation.md).

- [README](README.md): this file
- [AGENTS.md](AGENTS.md): standards & automation for humans and AI
- [docs/](init_django/templates/docs/): API, architecture, and models templates

---

## 🧑‍💻 Author
**Flavio Paulino**  
Tribeca Digital — São Paulo, Brazil  
[http://tribecadigital.com.br](http://tribecadigital.com.br)

---

## License
[MIT](LICENSE)

---

## 🏷️ Suggested GitHub Topics

django, cli, bootstrap, project-template, rest-api, python, automation, devtools, tribeca, modern-stack
- [cookiecutter-django](https://github.com/cookiecutter/cookiecutter-django)
- [Django Project](https://www.djangoproject.com/)
- [PEP-257](https://peps.python.org/pep-0257/)

---

> Generated by `Tribeca Django Init` — keep your bootstrap up to date!

