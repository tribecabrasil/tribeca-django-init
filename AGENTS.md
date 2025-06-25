# AGENTS.md — Guidance for Agents (Tribeca Django Init)

## Project Update and History Guidance

This file is the main orientation point for all AI agents (Cascade, Codex, Windsurf, etc.) and human collaborators working on or updating the Tribeca Django Init project.

- **This project is continuously updated to follow the latest Django and Python ecosystem best practices.**
- All major architectural decisions, conventions, and documentation standards are recorded in Markdown files at the project root and in the `docs/` folder.
- Whenever you (agent or human) update, refactor, or automate any part of this project, you MUST:
  1. **Consult this AGENTS.md and the README.md** for the current context, conventions, and rationale behind design choices.
  2. **Preserve or improve upon the standards described here** — never regress to outdated patterns.
  3. **Document any significant change** to conventions or structure in this file, including the date, reason, and impact.
  4. **Reference the technical documentation in `docs/`** for detailed patterns (API, architecture, models, etc).
- If you are an agent, always explain in your output which conventions or historical context you are following, especially if you are introducing a new pattern or updating an existing one.
- **Every CLI command execution must display a friendly, visual context message** (with emojis, usage instructions, and documentation references), both for human users and AI agents. This ensures clarity, onboarding, and a unified experience for all collaborators.

## CLI and Test Debugging Guidance

When working with the CLI and its automated tests (`tests/test_cli.py`), be aware of the following common pitfalls:

- **Test Input Alignment**: The tests use `click.testing.CliRunner` to simulate user input by feeding a newline-separated string. It is critical that the sequence of inputs exactly matches the sequence of prompts in `init_django/cli.py`.
  - **Symptom**: `click.exceptions.Abort` or unexpected errors where the wrong input is received for a prompt.
  - **Solution**: Carefully trace the CLI's execution flow. Add temporary debug prints in the CLI to see what value is being received at each prompt. Ensure every single prompt is accounted for in the test's input string, including prompts for versions or optional features.

- **Django Settings Template Errors**: The CLI generates a new Django project from templates (`init_django/templates/`). If the generated project fails during `manage.py migrate` or server startup, the issue is likely in the settings templates.
  - **Symptom**: `django.core.exceptions.ImproperlyConfigured` or `django.core.management.base.SystemCheckError`.
  - **Solution**: Ensure that `settings/base.py.tpl` contains all necessary settings for a default Django project to run, including `TEMPLATES` and `DATABASES`. The tests run in an isolated environment, so these settings must be self-sufficient.

- **Git Identity in CI**: The automated tests include running `git commit`. In a CI environment like GitHub Actions, there is no default Git user configured.
  - **Symptom**: `git commit` fails with `fatal: empty ident name` or `Author identity unknown`.
  - **Solution**: Add a step to the CI workflow (`.github/workflows/ci.yml`) to configure a dummy user name and email before running the tests. Example: `git config --global user.name "Test User"` and `git config --global user.email "test@example.com"`.

## Settings Templates Architecture (2025)

- **Motivação:** Para garantir clareza, manutenção e alinhamento com as melhores práticas Django, os templates de settings agora ficam em `init_django/templates/settings/`.
- **Arquivos:**
  - `base.py.tpl`, `dev.py.tpl`, `prod.py.tpl` (geram os arquivos finais em `config/settings/`)
- **Vantagens:**
  - Facilita a busca e manutenção dos templates.
  - Permite adicionar outros templates de settings ou ambientes facilmente.
  - Fica alinhado com o padrão Django e projetos modernos.
  - Torna o fluxo do CLI e a documentação mais previsíveis para humanos e IAs.

## Example of Update Log

```
## [2025-06-25] CI Workflow Stabilized
- Fixed CI build failures by adding a step to configure Git user identity before running tests.

## [2025-06-25] CLI Test Suite Stabilized
- Fixed test failures by correcting input sequences to match all CLI prompts (including Django version).
- Resolved migration errors by adding default `TEMPLATES` and `DATABASES` configurations to `settings/base.py.tpl`.
- The CLI is now robustly tested for the entire project creation flow.

## [2025-06-24] Initial project bootstrap and documentation structure finalized
- All documentation and templates are now in English
- Docs folder standardized: api_documentation.md, architecture_blueprint.md, django_models_template.md
- README and AGENTS.md reference all docs and explain project standards
```

## References
- Always keep this file and the README.md up to date with any relevant change.
- For detailed technical standards, see the files in `docs/`.
