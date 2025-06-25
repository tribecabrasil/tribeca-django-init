# Tribeca Django Init

This project was generated using the Tribeca Django Init CLI, which automates the creation of a modern Django project following professional best practices.

**Stack:**
- Python 3.12+
- Django 5.2+ (LTS)
- Django REST Framework
- PostgreSQL (recommended, but you can adapt)
- Gunicorn, Whitenoise, django-environ, psycopg[binary]
- pytest-django, black, isort, pre-commit (quality tools)

**Project structure and features:**
- Partitioned settings (`base`, `dev`, `prod`) for clear environment separation
- Local virtualenv `.venv` for reproducibility
- Essential dependencies for development and production already installed
- Git initialized with official Python `.gitignore`
- First app scaffolded and ready to extend
- Quality and automation tools pre-configured
- Production-ready static files setup

You can start developing immediately, following the standards and conventions described below.

## Technical Documentation

Detailed project documentation is located in the `docs/` folder at the project root. Always refer to both `README.md` and `agents.md` for general standards.

### docs/api_documentation.md
Comprehensive API documentation, endpoints, request/response examples, and best practices for versioning and authentication.

### docs/architecture_blueprint.md
Project architecture blueprint, describing modules, main flows, integrations, and key technical decisions.

### docs/django_models_template.md
Mandatory template for documenting all Django models in the project. Includes code examples, standardized docstrings, and field tables. Follow this pattern for every new model.

> Always refer to the `agents.md` file at the project root for automation guidelines, code standards, and AI integration.
