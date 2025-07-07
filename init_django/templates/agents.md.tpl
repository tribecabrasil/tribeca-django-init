# AGENTS.md — Guide for Agents in Django Projects

This file guides AI agents (Cascade, Codex, Windsurf, etc) and human developers on standards, practices, and required automations in modern Django projects.

## Recommended Django Project Structure

* `/config`: Main project package (partitioned settings)
  * `/settings/`: `base.py` (from `settings/base.py.tpl`), `dev.py` (from `settings/dev.py.tpl`), `prod.py` (from `settings/prod.py.tpl`), `__init__.py`
* `/manage.py`: Django management script
* `/app_name/`: Django apps separated by business domain
* `/tests/`: Unit and integration tests
* `/scripts/`: Helper scripts
* `.venv/`: Local virtual environment
* `.git/`, `.gitignore`, `README.md`, `AGENTS.md`

## Python/Django Code Conventions

* Use Python 3.12+ and Django 5.2+ (LTS)
* Follow PEP 8 and format with Black (max. 88 chars per line)
* Clear names: snake_case for functions/variables, PascalCase for classes, UPPER_CASE for constants
* Always use type annotations (PEP 484/526)
* Explanatory comments for complex logic
* Each function/method must have a single responsibility

## Django App Structure

* Each business domain should be a small and isolated Django app
* Models, views, forms, serializers, and admin should be organized by file
* Always document models according to the template in `init_django/templates/docs/ProjectDjangoModels.md.ply`
* Use migrations for every schema change

## Docstrings (PEP 257 — Windows-style)

* One-line summary followed by a detailed explanation
* Always document parameters and return types

Example:

```python
def clean_text(text: str) -> str:
    """Clean text by removing unwanted characters and extra spaces.

    Args:
        text: Input text.

    Returns:
        Cleaned and standardized text.
    """
    pass
```

## Tests and Quality

* Use pytest and pytest-django for all apps
* Always write tests for new features
* Maintain test coverage >=80%
* All checks must pass before merging any PR.

## Pull Requests and CI/CD

* PRs must be small, focused, and well described
* Always reference related issues
* All tests and linters must pass in CI

## Integration with Agents/AI

* Always consult this file and the root README.md for architecture, standards, and automation decisions
* Use the models template as a mandatory reference
* Do not overwrite configs/settings without user confirmation

---

## Docker and Containers

- Always provide a production-optimized `Dockerfile` using official Python and Django images.
- Use environment variables for sensitive configurations (never hardcode).
- Use `docker-compose.yml` to orchestrate services like database (Postgres), cache (Redis), Celery worker, Flower, etc.
- Include instructions for build, run, and troubleshooting in README.md.

Minimal `docker-compose.yml` example:

```yaml
version: '3.8'
services:
  web:
    build: .
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
    env_file:
      - .env
    depends_on:
      - db
      - redis
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: project_db
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
  redis:
    image: redis:7
  celery:
    build: .
    command: celery -A config worker -l info
    depends_on:
      - db
      - redis
  flower:
    build: .
    command: celery -A config flower
    ports:
      - 5555:5555
    depends_on:
      - redis
      - db
```

## REST APIs

- Use Django REST Framework (DRF) to create robust and standardized APIs.
- Implement API versioning (`/api/v1/`).
- Always write serializers, viewsets, and use DRF routers.
- Document routes with Swagger/OpenAPI (e.g., drf-yasg or drf-spectacular).
- Write tests for endpoints (using DRF's APIClient).
- Follow RESTful principles: correct HTTP methods, appropriate status codes, standardized error messages.

Basic viewset example:

```python
from rest_framework import viewsets
from .models import MyModel
from .serializers import MyModelSerializer

class MyModelViewSet(viewsets.ModelViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer
```

## Celery (Asynchronous Tasks)

- Use Celery for asynchronous and scheduled tasks.
- Configure Celery in the project (`config/celery.py`) and add initialization in the package's `__init__.py`.
- Use Redis or RabbitMQ as the broker.
- Document tasks and usage examples.
- Use Flower for monitoring.
- Write tests for asynchronous tasks.

Exemplo de task Celery:

```python
from celery import shared_task

@shared_task
def send_welcome_email(user_id):
    # logic to send email
    pass
```

## General Tips

- Always document how to run, debug, and monitor Docker, Celery, and APIs in README.md.
- Include healthcheck and readiness scripts for production.
- Instruct agents to never expose secrets in code or logs.

---
Always consult this file and the root README.md to ensure compliance and maximum efficiency in AI and human collaboration.

## Coding Conventions

* Use Python 3.10+ for all Codex-generated code
* Follow PEP 8 guidelines and Black formatter (line length ≤ 88 chars)
* Meaningful variable/function names (snake_case), classes (PascalCase), constants (UPPER_CASE)
* Comments for complex logic; descriptive and concise
* Always provide type annotations (PEP 484 and PEP 526)

## Modules and Functions

* Clearly structured, single-purpose modules
* Functions should perform one logical action
* Proper use of async/await (PEP 492) when relevant

## Docstrings (PEP 257 Windows-style)

* One-line summary followed by detailed description if needed
* Describe parameters and return types clearly

Example:

```python
def clean_text(text: str) -> str:
    """Clean text by removing unwanted characters and extra spaces.

    Args:
        text: Input text to clean.

    Returns:
        Cleaned text with standardized spacing.
    """
    pass
```

## Testing Requirements

Codex must generate tests using pytest:

```bash
pytest tests/ # Run all tests
pytest tests/test_module.py # Run specific tests
pytest --cov=tribeca_insights tests/ # Run with coverage
```

Maintain test coverage ≥80%.

## Pull Request (PR) Standards

Codex-generated PRs must:

* Include clear description and rationale
* Reference any related GitHub issues
* Ensure all tests pass
* Focus on one logical change per PR

## CI/CD and Checks

Before submitting code:

```bash
black --check .
isort --check-only .
flake8
pytest
```

All checks must pass to merge Codex-generated code.

## AI Analysis Integration (`ai_analysis`)

Codex should maintain consistency with the Tribeca Insights JSON schema (`project_{DOMAIN}.json`), populating or updating fields in `ai_analysis`:

* `embedding`: vector for semantic analysis
* `sentiment`: "positive", "neutral", "negative"
* `entities`: named entities from NLP
* `topics`: content classification
* `summary_ai`: AI-generated summary
* `faq_ai`: AI-generated FAQs
* `intent`: classified intent ("informational", "transactional")
* `quality_score_ai`: content quality score

## Usage and Workflow Commands

Codex can assist users with standard commands:

```bash
# Standard crawling execution
tribeca-insights --max-pages 50 --language en

# Validation of JSON structure
python scripts/validate_structure.py
```

## Technologies Detection

Codex should implement and extend detection heuristics:

* Parse headers, meta tags, file patterns
* Integrate external APIs (e.g., Wappalyzer, BuiltWith)

This document ensures structured and consistent Codex assistance within Tribeca Insights, enhancing AI and human collaboration efficiency.
