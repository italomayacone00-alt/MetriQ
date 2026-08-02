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

