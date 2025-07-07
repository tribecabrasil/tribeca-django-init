# 📋 Structured Backlog — Tribeca Django Init CLI

## 1. Internationalization and Localization (High Priority)
- [ ] **Primary Language Prompt:**
  The CLI should ask for the project's main language (`LANGUAGE_CODE`). Suggested options: `en`, `pt-br`, `es`, `fr`, `it`, `de`, `zh-cn`, `ja`, `ru`, `ar`.
- [ ] **Second Language Prompt:**
  Allow the user to choose a secondary language (`LANGUAGES`).
- [ ] **TIME_ZONE Prompt:**
  Ask for the project's time zone (with common suggestions).
- [ ] **Template Update:**
  Modify `base.py.tpl` to reflect the chosen language and time zone.
- [ ] **Documentation:**
  Explain how language and time zone configuration works in the README.
- [ ] **Automated Tests:**
  Ensure the user's choices are correctly applied in the settings.

## 2. CLI User Experience (Medium Priority)
- [ ] **Input Validation:**
  Validate and suggest documented defaults for language and time zone.
- [ ] **Contextual Messages:**
  Improve CLI prompts and feedback about internationalization.
- [ ] **Popular Language Suggestions:**
  Auto-complete or suggest the most common languages as the user types.

## 3. Django Translation Support (Medium Priority)
- [ ] **LOCALE_PATHS:**
  Add `LOCALE_PATHS` configuration to the settings.
- [ ] **makemessages/compilemessages Command:**
  Optionally run `django-admin makemessages` and `compilemessages` via the CLI.
- [ ] **README Example:**
  Document how to add new translations.

## 4. Quality and Maintenance (Low Priority)
- [ ] **Template Refinement:**
  Review and standardize comments, docstrings, and examples in the templates.
- [ ] **Internationalization Checklist:**
  Provide a visual checklist in the README for quick onboarding.
- [ ] **Translation Tool Suggestions:**
  List recommended tools for collaborative translation.

## 5. AI, Automation, and MCPs (High Priority)
- [ ] **Compatibility with MCPs (Multi-Component Platforms/AI agents):**
  Make the CLI easily integrable with intelligent agent platforms (MCPs), ensuring interoperability and automation.
- [ ] **Non-Interactive/Automatable Mode:**
  Allow running the CLI via flags for integration with scripts, pipelines, and MCPs.
- [ ] **Structured Prompts and Output:**
  Ensure all prompts and outputs are clear, standardized, and easily interpreted by agents and MCPs.
- [ ] **Documentation for Agents and MCPs:**
  Add a section in the README and AGENTS.md explaining how to integrate the CLI with MCPs, including automation examples and best practices.
- [ ] **Automated Tests for Agent/MCP Usage:**
  Ensure the CLI works well in headless environments, CI/CD pipelines, and MCP platforms.

## 6. Future Ideas and Other Features
- [ ] **Support for multiple settings environments (e.g., staging):**
- [ ] **Generation of internationalized CI/CD configuration files**
- [ ] **Integration with automatic translation services**
- [ ] **User suggestions**

---

> Edit and expand this backlog as needed for the project's roadmap.

