# Tribeca Django Init

[![Build Status](https://img.shields.io/github/actions/workflow/status/tribecabrasil/tribeca-django-init/ci.yml?branch=main)](https://github.com/tribecabrasil/tribeca-django-init/actions)
[![Coverage Status](https://img.shields.io/codecov/c/github/tribecabrasil/tribeca-django-init)](https://codecov.io/gh/tribecabrasil/tribeca-django-init)
[![License](https://img.shields.io/github/license/tribecabrasil/tribeca-django-init)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/django-5.2%2B-green)](https://www.djangoproject.com/)

**Modern, interactive CLI for bootstrapping Django projects with best practices, automation, and production-ready structure.**

---

## 🚀 Overview
This project was generated using the Tribeca Django Init CLI, which automates the creation of a modern Django project following professional best practices.

- Fast bootstrap with numbered choices, emojis, and clear prompts
- Installs Django 5.2+, Django REST Framework, and a modern stack
- Partitioned settings (base/dev/prod)
- Automated quality tools and CI/CD ready
- Documentation and templates in English, ready for international teams

---

## 🔧 Troubleshooting

- **`manage.py` errors**: If you see a `django.core.exceptions.ImproperlyConfigured` error, ensure that your `.env` file (copied from `.env.example`) is correctly configured and sourced.
- **Dependencies**: Make sure all dependencies from `requirements.txt` are installed in your virtual environment.

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

```bash
init-django
```

- Follow the interactive prompts in your terminal
- The CLI will guide you through each step: venv, dependencies, git, project, settings, app, migrations, and docs

---

## 🏗️ Example Project Structure
```text
config/
  settings/  # Contains base.py, dev.py, prod.py (generated from templates/settings/)
    __init__.py
    base.py
    dev.py
    prod.py
manage.py
.venv/
.git/
README.md
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
