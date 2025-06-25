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

## Example of Update Log

```
## [2025-06-24] Initial project bootstrap and documentation structure finalized
- All documentation and templates are now in English
- Docs folder standardized: api_documentation.md, architecture_blueprint.md, django_models_template.md
- README and AGENTS.md reference all docs and explain project standards
```

## References
- Always keep this file and the README.md up to date with any relevant change.
- For detailed technical standards, see the files in `docs/`.
