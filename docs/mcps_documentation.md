# Integração com MCPs (Multi-Component Platforms/AI Agents)

Este documento detalha como tornar o Tribeca Django Init CLI totalmente compatível, automatizável e amigável para plataformas MCPs e agentes de IA.

## Visão Geral
O CLI Tribeca Django Init está sendo planejado e evoluído para uso não apenas por humanos, mas também por agentes inteligentes e plataformas de automação (MCPs). Isso inclui:
- Execução não-interativa via argumentos/flags
- Prompts e saídas estruturadas e padronizadas
- Documentação clara para integração
- Testes automatizados para uso headless

## Arquitetura CLI: Interface Humana e MCP

O Tribeca Django Init CLI possui duas interfaces totalmente sincronizadas:

- `cli_user.py`: interface tradicional para humanos, com prompts interativos, mensagens amigáveis e UX aprimorada.
- `cli_mcp.py`: interface para MCPs/agentes/automação, modo não-interativo, argumentos/flags e saída padronizada JSON.
- Toda a lógica utilitária e de negócio reside em `cli_common.py`, garantindo que ambos os modos compartilhem a mesma API e semântica.

**IMPORTANTE:**
Sempre que uma nova feature, comando ou ajuste for implementado, garanta que a funcionalidade seja replicada e compatível em ambos os arquivos (`cli_user.py` e `cli_mcp.py`).

- O entrypoint (`cli.py`) detecta o modo automaticamente e delega para o arquivo correto.
- Ambas as interfaces devem aceitar os mesmos comandos, argumentos e fluxos, apenas mudando a forma de interação (prompts vs flags/JSON).
- Testes e documentação devem cobrir ambos os modos.

## Modo JSON (--json)

Para integração avançada com MCPs, o CLI suporta o argumento `--json`, que faz com que todas as saídas relevantes do CLI sejam emitidas em formato JSON estruturado, facilitando o parsing por agentes e scripts automatizados.

### Exemplo de uso
```bash
tribeca-django-init ... --json
```

### Exemplo de saída JSON
```json
{
  "step": "virtualenv",
  "status": "created",
  "path": "/home/user/projeto/.venv"
}
{
  "step": "dependencies",
  "status": "installed",
  "packages": ["django==5.2.3", "djangorestframework", ...]
}
{
  "step": "settings",
  "status": "generated",
  "files": ["config/settings/base.py", ...]
}
{
  "step": "done",
  "status": "success",
  "project_root": "/home/user/projeto"
}
```

- Cada etapa relevante do CLI gera um objeto JSON na saída padrão.
- Em caso de erro, um objeto JSON com `status: error` e mensagem detalhada é emitido.
- Ideal para integração com MCPs, CI/CD, scripts e plataformas de agentes inteligentes.

## Roadmap e Features Planejadas

### 1. Modo Não-Interativo/Automatizável
- Permitir execução do CLI com todos os parâmetros via argumentos de linha de comando (ex: `--language-code`, `--timezone`, `--no-input`, etc.)
- Exemplo:
  ```bash
  tribeca-django-init --language-code pt-br --second-language en --timezone America/Sao_Paulo --no-input
  ```

### 2. Prompts e Saídas Estruturadas
- Garantir que todos os prompts e saídas do CLI sejam claros, previsíveis e facilmente parseáveis por scripts e agentes.
- Opcional: saída em JSON ou modo "machine-friendly".

### 3. Documentação para Agentes/MCPs
- Seção dedicada no README e AGENTS.md sobre integração com MCPs
- Exemplos de automação (scripts, pipelines CI/CD, integração com plataformas de agentes)

### 4. Testes Automatizados para Uso por Agentes/MCPs
- Testes que garantam funcionamento do CLI em ambientes headless, CI/CD e automação
- Testes de idempotência e robustez

### 5. Boas Práticas de Integração
- Recomendações para integração segura e previsível em pipelines
- Sugestão de padrões de resposta e tratamento de erros

---

## Referência na Documentação
> O suporte e compatibilidade com MCPs já está em planejamento ativo. Veja também o backlog e a seção "IA, Automação e MCPs" para detalhes e progresso.

---

Sinta-se à vontade para contribuir com sugestões, exemplos ou abrir issues sobre integração com MCPs!
