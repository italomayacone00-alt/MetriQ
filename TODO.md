# TODO - Correção do erro `projeto.empresa_id does not exist` no Render

## Problema
A tabela `projeto` no PostgreSQL do Render foi criada em um deploy anterior e não possui
a coluna `empresa_id` (nem as tabelas `planta_baixa`, `checklist_nr` e `checklist_iso`).

## Passos

- [x] 1. Diagnosticar a causa (banco local SQLite tem `empresa_id`, banco do Render não tem)
- [x] 2. Adicionar `empresa_id` à lista de colunas verificadas na migração `run_migration()`
- [x] 3. Adicionar `empresa_id` na migração automática `run_migration_auto()` (roda a cada deploy)
- [x] 4. Generalizar a migração para verificar `empresa_id` também em `planta_baixa`, `checklist_nr` e `checklist_iso`
- [x] 5. Testar a migração localmente com o SQLite (verificar que não quebra e é idempotente)
- [ ] 6. Enviar as alterações para o Git e fazer deploy no Render
- [ ] 7. Verificar se a página /projetos carrega sem erro no Render

## Arquivo alterado
- `qualidade_flask/migrate_projeto_columns.py`

