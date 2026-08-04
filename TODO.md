# TODO - Melhorias de Segurança e Login/Cadastro Profissional

## Progresso

### Fase 1 — Fundação (Modelo & Config)
- [x] 1. Adicionar campos ao modelo `User` (plano, status, email_confirmado, ultimo_login, tentativas_login, bloqueio_ate)
- [x] 2. Migração automática das novas colunas em `migrate_projeto_columns.py`
- [x] 3. Secret Key: chave aleatória persistente local + obrigatório variável ambiente em produção
- [x] 4. Sessão configurada (HTTPOnly, SameSite, remember cookie duration)
- [x] 5. Talisman/HTTPS ativo em produção (não só RENDER)
- [x] 6. Adicionar `flask-limiter` + `bleach` ao requirements.txt
- [x] 7. Criar pacote `utils/` com security.py, email.py, sanitize.py

### Fase 2 — Autenticação Robusta
- [x] 8. Login com limite de tentativas (5 falhas → bloqueio 15 min) via `flask-limiter` + lógica manual
- [x] 9. "Lembrar-me" (remember me) no login
- [x] 10. Logout via POST (formulário com CSRF) — eliminado CSRF de logout
- [x] 11. Registro com validação: e-mail obrigatório/único, senha forte (8+ chars, letras+números), confirmação de senha
- [x] 12. Confirmação de e-mail via token (salt='confirmacao_email')
- [x] 13. Recuperação de senha via token (salt='recuperacao_senha', 1h de validade)
- [x] 14. Rate limit nas rotas sensíveis (login: 10/min, registro: 5/min, salvar: 30/min)

### Fase 3 — Segurança de Conteúdo (XSS)
- [x] 15. Sanitizar HTML da IA com `bleach` antes de salvar (`sanitizar_html`)
- [x] 16. Sanitizar `analise_geral` no relatório

### Fase 4 — Preparação Free/Premium
- [x] 17. Campo `plano` no User (free/pro)
- [x] 18. Badge de plano no perfil
- [ ] 19. Página de planos (informativa) — opcional agora

### Fase 5 — Google OAuth (Login com Google)
- [x] 22. Instalar `authlib`
- [x] 23. Criar `qualidade_flask/utils/oauth.py` com configuração do Google OAuth
- [x] 24. Atualizar `__init__.py` para inicializar OAuth
- [x] 25. Adicionar rotas `/login/google` e `/login/google/callback` em `auth.py`
- [x] 26. Atualizar `login.html` com botão "Entrar com Google"
- [x] 27. Testar inicialização do app (OK)

### Fase 6 — Polimento
- [ ] 20. Testar e verificar funcionamento completo
- [ ] 21. Rodar migração automática
