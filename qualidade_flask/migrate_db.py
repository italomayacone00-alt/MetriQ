"""
Script de migração para adicionar colunas faltantes ao banco de dados
Execute este script no Render: python qualidade_flask/migrate_db.py
"""
from qualidade_flask import create_app, db
from sqlalchemy import text

def migrate():
    app = create_app()
    with app.app_context():
        # Verificar e adicionar colunas faltantes na tabela projeto
        try:
            # Coluna tipo
            db.session.execute(text("ALTER TABLE projeto ADD COLUMN IF NOT EXISTS tipo VARCHAR(20) DEFAULT 'normal'"))
            print("✓ Coluna 'tipo' adicionada à tabela projeto")
        except Exception as e:
            print(f"Coluna 'tipo' já existe ou erro: {e}")
        
        try:
            # Coluna fase_atual
            db.session.execute(text("ALTER TABLE projeto ADD COLUMN IF NOT EXISTS fase_atual VARCHAR(20) DEFAULT 'plan'"))
            print("✓ Coluna 'fase_atual' adicionada à tabela projeto")
        except Exception as e:
            print(f"Coluna 'fase_atual' já existe ou erro: {e}")
        
        try:
            # Coluna ciclo_atual
            db.session.execute(text("ALTER TABLE projeto ADD COLUMN IF NOT EXISTS ciclo_atual INTEGER DEFAULT 1"))
            print("✓ Coluna 'ciclo_atual' adicionada à tabela projeto")
        except Exception as e:
            print(f"Coluna 'ciclo_atual' já existe ou erro: {e}")
        
        try:
            # Coluna documento_padronizacao
            db.session.execute(text("ALTER TABLE projeto ADD COLUMN IF NOT EXISTS documento_padronizacao JSON"))
            print("✓ Coluna 'documento_padronizacao' adicionada à tabela projeto")
        except Exception as e:
            print(f"Coluna 'documento_padronizacao' já existe ou erro: {e}")
        
        try:
            # Coluna data_conclusao_ciclo
            db.session.execute(text("ALTER TABLE projeto ADD COLUMN IF NOT EXISTS data_conclusao_ciclo TIMESTAMP"))
            print("✓ Coluna 'data_conclusao_ciclo' adicionada à tabela projeto")
        except Exception as e:
            print(f"Coluna 'data_conclusao_ciclo' já existe ou erro: {e}")
        
        db.session.commit()
        print("\n✅ Migração concluída com sucesso!")

if __name__ == '__main__':
    migrate()
