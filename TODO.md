# TODO - Tela de Perfil do Usuário

## Objetivo
Criar uma tela de perfil onde o usuário possa visualizar/editar seus dados cadastrais,
alterar a senha e ver estatísticas de uso do sistema.

## Passos

- [x] 1. Adicionar campos ao modelo `User` em `models.py` (nome_completo, email, telefone, cargo, data_cadastro)
- [x] 2. Adicionar migração automática das novas colunas em `migrate_projeto_columns.py`
- [x] 3. Criar rotas de perfil em `auth.py` (visualizar, editar dados, alterar senha)
- [x] 4. Criar template `perfil.html` com abas (Meus Dados, Alterar Senha, Estatísticas)
- [x] 5. Atualizar `registro.html` com campos adicionais (nome, e-mail, telefone, cargo)
- [x] 6. Atualizar `registro_post` no `auth.py` para salvar novos campos
- [x] 7. Atualizar `base.html` para linkar o nome do usuário ao perfil
- [x] 8. Testar rotas e validações (senha atual, confirmação, CSRF) — migração rodou, rotas registradas, template renderizado com sucesso

---

# TODO - Otimização de Performance (CDNs e Banco)

## Resumo
- **Chart.js (~130 KB) + Datalabels (~30 KB)**: Removidos do `base.html`. Agora carregados apenas em: cep, dispersao, folha_verificacao, histograma
- **SheetJS/xlsx.full.min.js (~500 KB)**: Removido do `base.html`. Agora carregado apenas em: cep, dispersao, fluxograma, folha_verificacao, histograma, ishikawa
- **Índices no banco**: Adicionados em `user_id`, `empresa_id`, `norma_id` nas tabelas mais consultadas
- **`__tablename__` explícito**: Adicionado em todas as tabelas para evitar conflitos com palavras reservadas

## Passos

- [x] 1. Remover Chart.js, Datalabels e SheetJS do `base.html`
- [x] 2. Adicionar índices e `__tablename__` em todas as tabelas em `models.py`
- [x] 3. Remover Chart.js duplicado do `{% block content %}` em cep.html, dispersao.html, histograma.html
- [x] 4. Mover Chart.js/Datalabels para `{% block scripts %}` em folha_verificacao.html
- [x] 5. Remover `scan_templates.py` (script temporário)

