# AGENTS.md — Guia para Agentes em Projetos Django

Este arquivo orienta agentes de IA (Cascade, Codex, Windsurf, etc) e desenvolvedores humanos quanto a padrões, práticas e automações obrigatórias em projetos Django modernos.

## Estrutura Recomendada de Projeto Django

* `/config`: Pacote principal do projeto (settings particionados)
  * `/settings/`: `base.py`, `dev.py`, `prod.py`, `__init__.py`
* `/manage.py`: Script de gerenciamento Django
* `/app_name/`: Apps Django separados por domínio de negócio
* `/tests/`: Testes unitários e de integração
* `/scripts/`: Scripts auxiliares
* `.venv/`: Ambiente virtual local
* `.git/`, `.gitignore`, `README.md`, `AGENTS.md`

## Convenções de Código Python/Django

* Use Python 3.12+ e Django 5.2+ (LTS)
* Siga PEP 8 e formate com Black (máx. 88 chars por linha)
* Nomes claros: snake_case para funções/variáveis, PascalCase para classes, UPPER_CASE para constantes
* Sempre use type annotations (PEP 484/526)
* Comentários explicativos para lógicas complexas
* Cada função/método deve ter responsabilidade única
* Use async/await apenas quando necessário (ex: I/O intensivo)

## Estrutura de Apps Django

* Cada domínio de negócio deve ser um app Django pequeno e isolado
* Models, views, forms, serializers e admin devem ser organizados por arquivo
* Sempre documente models conforme o template em `init_django/templates/docs/ProjectDjangoModels.md.ply`
* Use migrations para toda alteração de schema

## Docstrings (PEP 257 — Windows-style)

* Resumo em uma linha seguido de explicação detalhada
* Sempre documente parâmetros e tipos de retorno

Exemplo:

```python
def clean_text(text: str) -> str:
    """Limpa texto removendo caracteres indesejados e espaços extras.

    Args:
        text: Texto de entrada.

    Returns:
        Texto limpo e padronizado.
    """
    pass
```

## Testes e Qualidade

* Use pytest e pytest-django para todos os apps
* Cobertura mínima recomendada: 80%
* Configure pre-commit com Black, isort, flake8, e testes automáticos

```bash
black --check .
isort --check-only .
flake8
pytest
```

Todos os checks devem passar antes de mergear qualquer PR.

## Pull Requests e CI/CD

* PRs devem ser pequenos, focados e bem descritos
* Sempre referencie issues relacionadas
* Todos os testes e linters devem passar no CI

## Integração com Agentes/IA

* Sempre consulte este arquivo e o README.md da raiz para decisões de arquitetura, padrões e automação
* Use o template de models como referência obrigatória
* Não sobrescreva configs/settings sem confirmação do usuário

---

## Docker e Contêineres

- Sempre forneça um `Dockerfile` otimizado para produção, usando imagens oficiais do Python e Django.
- Utilize variáveis de ambiente para configurações sensíveis (nunca hardcode).
- Use `docker-compose.yml` para orquestrar serviços como banco de dados (Postgres), cache (Redis), Celery worker, Flower, etc.
- Inclua instruções para build, run, e troubleshooting no README.md.

Exemplo mínimo de `docker-compose.yml`:

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
      POSTGRES_PASSWORD: pass
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

- Use Django REST Framework (DRF) para criar APIs robustas e padronizadas.
- Implemente versionamento de API (`/api/v1/`).
- Sempre escreva serializers, viewsets, e utilize routers do DRF.
- Documente as rotas com Swagger/OpenAPI (ex: drf-yasg ou drf-spectacular).
- Escreva testes para endpoints (usando APIClient do DRF).
- Siga princípios RESTful: métodos HTTP corretos, status codes apropriados, mensagens de erro padronizadas.

Exemplo de viewset básico:

```python
from rest_framework import viewsets
from .models import MyModel
from .serializers import MyModelSerializer

class MyModelViewSet(viewsets.ModelViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer
```

## Celery (Tarefas Assíncronas)

- Use Celery para tarefas assíncronas e agendadas.
- Configure Celery no projeto (`config/celery.py`) e adicione inicialização no `__init__.py` do pacote principal.
- Use Redis ou RabbitMQ como broker.
- Documente tasks e exemplos de uso.
- Utilize Flower para monitoramento.
- Escreva testes para tasks assíncronas.

Exemplo de task Celery:

```python
from celery import shared_task

@shared_task
def send_welcome_email(user_id):
    # lógica para envio de email
    pass
```

## Dicas Gerais

- Sempre documente como rodar, debugar e monitorar Docker, Celery, e APIs no README.md.
- Inclua scripts de healthcheck e readiness para produção.
- Oriente agentes a nunca expor segredos em código ou logs.

---
Consulte sempre este arquivo e o README.md da raiz para garantir conformidade e máxima eficiência na colaboração entre IA e humanos.

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
