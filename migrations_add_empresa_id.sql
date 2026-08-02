-- Migration: Adicionar coluna empresa_id na tabela projeto
-- Para projetos existentes que não têm empresa vinculada

ALTER TABLE projeto ADD COLUMN empresa_id INTEGER REFERENCES empresa(id) ON DELETE SET NULL;
CREATE INDEX ix_projeto_empresa_id ON projeto(empresa_id);

-- Atualizar a versão do banco se estiver usando Alembic
-- UPDATE alembic_version SET version_num = 'xxx';

