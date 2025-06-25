# 📋 Backlog Estruturado — Tribeca Django Init CLI

## 1. Internacionalização e Localização (Prioridade Alta)
- [ ] **Pergunta de Idioma Inicial:**  
  CLI deve perguntar o idioma principal do projeto (`LANGUAGE_CODE`).  
  Sugerir e documentar: `en`, `pt-br`, `es`, `fr`, `it`, `de`, `zh-cn`, `ja`, `ru`, `ar`.
- [ ] **Pergunta de Segunda Língua:**  
  Permitir ao usuário escolher uma segunda língua (`LANGUAGES`).
- [ ] **Pergunta de TIME_ZONE:**  
  CLI deve perguntar o fuso horário do projeto (com sugestões).
- [ ] **Atualização dos Templates:**  
  Modificar `base.py.tpl` para refletir as escolhas de idioma e timezone.
- [ ] **Documentação:**  
  Explicar como funciona a configuração de idiomas e timezone no README.
- [ ] **Testes Automatizados:**  
  Testar se as escolhas do usuário são aplicadas corretamente no settings.

## 2. Experiência do Usuário no CLI (Prioridade Média)
- [ ] **Validação de Entradas:**  
  Validar e sugerir valores padrão/documentados para idioma e timezone.
- [ ] **Mensagens Contextuais:**  
  Melhorar prompts e feedbacks do CLI sobre internacionalização.
- [ ] **Sugestão de Idiomas Populares:**  
  Auto-completar ou sugerir os idiomas mais comuns ao digitar.

## 3. Suporte a Traduções Django (Prioridade Média)
- [ ] **LOCALE_PATHS:**  
  Adicionar configuração de `LOCALE_PATHS` no settings.
- [ ] **Comando para makemessages/compilemessages:**  
  Adicionar comando opcional no CLI para rodar `django-admin makemessages` e `compilemessages`.
- [ ] **Exemplo de uso no README:**  
  Documentar como adicionar novas traduções.

## 4. Qualidade e Manutenção (Prioridade Baixa)
- [ ] **Refino dos Templates:**  
  Revisar e padronizar comentários, docstrings e exemplos nos templates.
- [ ] **Checklist de Internacionalização:**  
  Adicionar checklist visual no README para onboarding rápido.
- [ ] **Sugestão de Ferramentas de Tradução:**  
  Listar ferramentas recomendadas para tradução colaborativa.

## 5. IA, Automação e MCPs (Prioridade Alta)
- [ ] **Compatibilidade com MCPs (Multi-Component Platforms/AI agents):**
  Tornar o CLI facilmente integrável e utilizável por plataformas de agentes inteligentes (MCPs), garantindo interoperabilidade e automação.
- [ ] **Modo Não-Interativo/Automatizável:**
  Permitir execução do CLI via argumentos/flags para integração com scripts, pipelines e MCPs.
- [ ] **Prompts e Saídas Estruturadas:**
  Garantir que todos os prompts e saídas sejam claros, padronizados e facilmente interpretáveis por agentes e MCPs.
- [ ] **Documentação para Agentes e MCPs:**
  Adicionar seção no README e AGENTS.md explicando como integrar o CLI com MCPs, exemplos de automação e melhores práticas para agentes.
- [ ] **Testes Automatizados para Uso por Agentes/MCPs:**
  Garantir que o CLI funcione bem em ambientes headless, pipelines CI/CD e plataformas MCP.

## 6. Ideias Futuras e Outras Features
- [ ] **Suporte a múltiplos ambientes de settings (ex: staging):**
- [ ] **Geração de arquivos de configuração para CI/CD internacionalizados**
- [ ] **Integração com serviços de tradução automática**
- [ ] **Sugestões do usuário**

---

> Edite e detalhe este backlog conforme necessário para o roadmap do projeto.
