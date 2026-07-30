"""
Script de migração universal para adicionar colunas faltantes na tabela 'projeto'.
Funciona tanto para SQLite (local) quanto PostgreSQL (Render/produção).

Uso: python -c "from qualidade_flask.migrate_projeto_columns import run_migration; run_migration()"
"""

import os
import sys

# Garantir que o diretório pai está no path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Flag para evitar recursão infinita quando chamado do __init__.py
_migration_running = False

def run_migration():
    """Executa a migração das colunas faltantes na tabela projeto"""
    from qualidade_flask import create_app, db
    from sqlalchemy import inspect, text
    from sqlalchemy.exc import OperationalError, ProgrammingError
    
    app = create_app()
    
    with app.app_context():
        engine = db.engine
        inspector = inspect(engine)
        
        # Descobrir o dialeto do banco (sqlite, postgresql, etc)
        dialect = engine.dialect.name
        print(f"🔍 Banco detectado: {dialect}")
        
        # ==========================================
        # 1. VERIFICAR COLUNAS EXISTENTES NA TABELA projeto
        # ==========================================
        try:
            colunas_existentes = [col['name'] for col in inspector.get_columns('projeto')]
            print(f"📋 Colunas existentes em 'projeto': {colunas_existentes}")
        except Exception as e:
            print(f"❌ Erro ao inspecionar tabela 'projeto': {e}")
            # Tenta criar a tabela do zero se não existir
            print("🔄 Tentando criar tabelas...")
            db.create_all()
            colunas_existentes = [col['name'] for col in inspector.get_columns('projeto')]
            print(f"📋 Colunas após create_all: {colunas_existentes}")
        
        # Colunas que precisam existir no modelo Projeto
        colunas_necessarias = {
            'tipo': {
                'sqlite': "VARCHAR(20) DEFAULT 'normal'",
                'postgresql': "VARCHAR(20) DEFAULT 'normal'"
            },
            'fase_atual': {
                'sqlite': "VARCHAR(20) DEFAULT 'plan'",
                'postgresql': "VARCHAR(20) DEFAULT 'plan'"
            },
            'ciclo_atual': {
                'sqlite': "INTEGER DEFAULT 1",
                'postgresql': "INTEGER DEFAULT 1"
            },
            'documento_padronizacao': {
                'sqlite': "JSON",
                'postgresql': "JSON"
            },
            'data_conclusao_ciclo': {
                'sqlite': "DATETIME",
                'postgresql': "TIMESTAMP"
            }
        }
        
        colunas_adicionadas = []
        
        for col_name, col_types in colunas_necessarias.items():
            if col_name not in colunas_existentes:
                col_type = col_types.get(dialect, col_types.get('sqlite'))
                try:
                    with engine.connect() as conn:
                        alter_sql = f"ALTER TABLE projeto ADD COLUMN {col_name} {col_type}"
                        conn.execute(text(alter_sql))
                        conn.commit()
                    print(f"  ✅ Coluna '{col_name}' ({col_type}) ADICIONADA com sucesso!")
                    colunas_adicionadas.append(col_name)
                except Exception as e:
                    print(f"  ❌ Erro ao adicionar coluna '{col_name}': {e}")
            else:
                print(f"  ⏭️  Coluna '{col_name}' já existe.")
        
        # ==========================================
        # 2. VERIFICAR TABELA ciclo_historico
        # ==========================================
        try:
            tabelas = inspector.get_table_names()
            if 'ciclo_historico' not in tabelas:
                print("📋 Criando tabela 'ciclo_historico'...")
                # Criar usando SQLAlchemy metadata / create_all
                from qualidade_flask.models import CicloHistorico
                db.create_all()  # create_all é idempotente, só cria tabelas que não existem
                print("  ✅ Tabela 'ciclo_historico' CRIADA!")
            else:
                # Verificar colunas da ciclo_historico
                colunas_ch = [col['name'] for col in inspector.get_columns('ciclo_historico')]
                print(f"  ⏭️  Tabela 'ciclo_historico' já existe. Colunas: {colunas_ch}")
        except Exception as e:
            print(f"  ❌ Erro ao verificar/criar 'ciclo_historico': {e}")
        
        # ==========================================
        # 3. RESUMO FINAL
        # ==========================================
        if colunas_adicionadas:
            print(f"\n✅ Migração concluída! Colunas adicionadas: {colunas_adicionadas}")
        else:
            print(f"\n✅ Nenhuma coluna nova necessária. Schema já está atualizado.")
        
        # Verificar schema final
        try:
            colunas_atuais = [col['name'] for col in inspector.get_columns('projeto')]
            print(f"\n📋 Schema final da tabela 'projeto': {colunas_atuais}")
        except Exception as e:
            print(f"  ❌ Erro ao verificar schema final: {e}")
        
        return colunas_adicionadas


def run_migration_auto():
    """Versão para ser chamada automaticamente do __init__.py (sem criar novo app)"""
    global _migration_running
    if _migration_running:
        return  # Evita recursão infinita
    _migration_running = True
    
    try:
        from qualidade_flask import db
        from sqlalchemy import inspect, text
        
        # Já estamos dentro de um app_context quando chamado do __init__.py
        engine = db.engine
        inspector = inspect(engine)
        dialect = engine.dialect.name
        
        colunas_existentes = [col['name'] for col in inspector.get_columns('projeto')]
        
        colunas_necessarias = ['tipo', 'fase_atual', 'ciclo_atual', 'documento_padronizacao', 'data_conclusao_ciclo']
        colunas_faltando = [c for c in colunas_necessarias if c not in colunas_existentes]
        
        if not colunas_faltando:
            return  # Nada a fazer
        
        print(f"📝 Migração automática: adicionando colunas {colunas_faltando}...")
        
        col_types = {
            'tipo': "VARCHAR(20) DEFAULT 'normal'",
            'fase_atual': "VARCHAR(20) DEFAULT 'plan'",
            'ciclo_atual': "INTEGER DEFAULT 1",
            'documento_padronizacao': "JSON",
            'data_conclusao_ciclo': "TIMESTAMP" if dialect == 'postgresql' else "DATETIME"
        }
        
        with engine.connect() as conn:
            for col_name in colunas_faltando:
                col_type = col_types.get(col_name)
                if col_type:
                    try:
                        conn.execute(text(f"ALTER TABLE projeto ADD COLUMN {col_name} {col_type}"))
                        print(f"  ✅ Coluna '{col_name}' adicionada")
                    except Exception:
                        pass  # Ignora erros individuais
            conn.commit()
        
        db.create_all()  # Garante que ciclo_historico exista
        print("✅ Migração automática concluída!")
            
    except Exception as e:
        print(f"⚠️ Migração automática ignorada: {e}")
    finally:
        _migration_running = False


if __name__ == '__main__':
    run_migration()

