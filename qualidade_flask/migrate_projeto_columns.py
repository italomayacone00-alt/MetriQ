"""
Script de migração universal para adicionar colunas faltantes nas tabelas.
Funciona tanto para SQLite (local) quanto PostgreSQL (Render/produção).

Colunas cobertas:
- projeto:        empresa_id, tipo, fase_atual, ciclo_atual, documento_padronizacao, data_conclusao_ciclo
- planta_baixa:   empresa_id
- checklist_nr:   empresa_id
- checklist_iso:  empresa_id
- user:           nome_completo, email, telefone, cargo, data_cadastro,
                  plano, status, email_confirmado, ultimo_login,
                  tentativas_login, bloqueio_ate

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

# Mapeamento de tabelas -> colunas necessárias -> tipos SQL por dialeto
TABELAS_COLUNAS = {
    'projeto': {
        'empresa_id': {
            'sqlite': "INTEGER",
            'postgresql': "INTEGER"
        },
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
    },
    'planta_baixa': {
        'empresa_id': {
            'sqlite': "INTEGER",
            'postgresql': "INTEGER"
        }
    },
    'checklist_nr': {
        'empresa_id': {
            'sqlite': "INTEGER",
            'postgresql': "INTEGER"
        }
    },
    'checklist_iso': {
        'empresa_id': {
            'sqlite': "INTEGER",
            'postgresql': "INTEGER"
        }
    },
'user': {
        'nome_completo': {
            'sqlite': "VARCHAR(200) DEFAULT ''",
            'postgresql': "VARCHAR(200) DEFAULT ''"
        },
        'email': {
            'sqlite': "VARCHAR(150) DEFAULT ''",
            'postgresql': "VARCHAR(150) DEFAULT ''"
        },
        'telefone': {
            'sqlite': "VARCHAR(20) DEFAULT ''",
            'postgresql': "VARCHAR(20) DEFAULT ''"
        },
        'cargo': {
            'sqlite': "VARCHAR(100) DEFAULT ''",
            'postgresql': "VARCHAR(100) DEFAULT ''"
        },
        'data_cadastro': {
            'sqlite': "DATETIME",
            'postgresql': "TIMESTAMP"
        },
        'plano': {
            'sqlite': "VARCHAR(20) DEFAULT 'free'",
            'postgresql': "VARCHAR(20) DEFAULT 'free'"
        },
        'status': {
            'sqlite': "VARCHAR(20) DEFAULT 'ativo'",
            'postgresql': "VARCHAR(20) DEFAULT 'ativo'"
        },
        'email_confirmado': {
            'sqlite': "BOOLEAN DEFAULT 0",
            'postgresql': "BOOLEAN DEFAULT FALSE"
        },
        'ultimo_login': {
            'sqlite': "DATETIME",
            'postgresql': "TIMESTAMP"
        },
        'tentativas_login': {
            'sqlite': "INTEGER DEFAULT 0",
            'postgresql': "INTEGER DEFAULT 0"
        },
        'bloqueio_ate': {
            'sqlite': "DATETIME",
            'postgresql': "TIMESTAMP"
        }
    }
}


def migrar_tabela(engine, inspector, dialect, tabela, colunas_necessarias):
    """Adiciona colunas faltantes em uma tabela. Retorna lista de colunas adicionadas."""
    colunas_adicionadas = []

    # Verificar se a tabela existe
    if tabela not in inspector.get_table_names():
        print(f"Tabela '{tabela}' nao existe. Será criada pelo db.create_all().")
        return colunas_adicionadas

    try:
        colunas_existentes = [col['name'] for col in inspector.get_columns(tabela)]
        print(f"Colunas existentes em '{tabela}': {colunas_existentes}")
    except Exception as e:
        print(f"Erro ao inspecionar tabela '{tabela}': {e}")
        return colunas_adicionadas

    for col_name, col_types in colunas_necessarias.items():
        if col_name not in colunas_existentes:
            col_type = col_types.get(dialect, col_types.get('sqlite'))
            try:
                with engine.connect() as conn:
                    # Usa aspas duplas para citar o nome da tabela.
                    # Necessário porque 'user' é palavra reservada no PostgreSQL.
                    alter_sql = f'ALTER TABLE "{tabela}" ADD COLUMN "{col_name}" {col_type}'
                    conn.execute(text(alter_sql))
                    conn.commit()
                print(f"Coluna '{col_name}' ({col_type}) adicionada em '{tabela}'!")
                colunas_adicionadas.append(f"{tabela}.{col_name}")
            except Exception as e:
                print(f"Erro ao adicionar coluna '{col_name}' em '{tabela}': {e}")
        else:
            print(f"Coluna '{tabela}.{col_name}' ja existe.")

    return colunas_adicionadas


def run_migration():
    """Executa a migração das colunas faltantes nas tabelas principais"""
    from qualidade_flask import create_app, db
    from sqlalchemy import inspect, text

    app = create_app()

    with app.app_context():
        engine = db.engine
        inspector = inspect(engine)

        # Descobrir o dialeto do banco (sqlite, postgresql, etc)
        dialect = engine.dialect.name
        print(f"Banco detectado: {dialect}")

        # ==========================================
        # 1. VERIFICAR COLUNAS EXISTENTES NAS TABELAS
        # ==========================================
        colunas_adicionadas = []

        for tabela, colunas in TABELAS_COLUNAS.items():
            print(f"\nProcessando tabela '{tabela}'...")
            colunas_adicionadas.extend(migrar_tabela(engine, inspector, dialect, tabela, colunas))

        # ==========================================
        # 2. VERIFICAR TABELA ciclo_historico
        # ==========================================
        try:
            tabelas = inspector.get_table_names()
            if 'ciclo_historico' not in tabelas:
                print("\nCriando tabela 'ciclo_historico'...")
                # Criar usando SQLAlchemy metadata / create_all
                from qualidade_flask.models import CicloHistorico
                db.create_all()  # create_all é idempotente, só cria tabelas que não existem
                print("Tabela 'ciclo_historico' criada!")
            else:
                # Verificar colunas da ciclo_historico
                colunas_ch = [col['name'] for col in inspector.get_columns('ciclo_historico')]
                print(f"\nTabela 'ciclo_historico' ja existe. Colunas: {colunas_ch}")
        except Exception as e:
            print(f"Erro ao verificar/criar 'ciclo_historico': {e}")

        # ==========================================
        # 3. RESUMO FINAL
        # ==========================================
        if colunas_adicionadas:
            print(f"\nMigracao concluida! Colunas adicionadas: {colunas_adicionadas}")
        else:
            print(f"\nNenhuma coluna nova necessaria. Schema ja estah atualizado.")

        # Verificar schema final
        for tabela in TABELAS_COLUNAS:
            try:
                colunas_atuais = [col['name'] for col in inspector.get_columns(tabela)]
                print(f"\nSchema final da tabela '{tabela}': {colunas_atuais}")
            except Exception as e:
                print(f"Erro ao verificar schema final de '{tabela}': {e}")

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

        colunas_adicionadas = []

        for tabela, colunas in TABELAS_COLUNAS.items():
            if tabela not in inspector.get_table_names():
                continue  # Tabela ainda não existe; será criada pelo db.create_all()

            colunas_existentes = [col['name'] for col in inspector.get_columns(tabela)]
            colunas_faltando = [c for c in colunas if c not in colunas_existentes]

            if not colunas_faltando:
                continue

            print(f"Migracao automatica: adicionando colunas {colunas_faltando} em '{tabela}'...")

            with engine.connect() as conn:
                for col_name in colunas_faltando:
                    col_type = colunas[col_name].get(dialect, colunas[col_name].get('sqlite'))
                    if col_type:
                        try:
                            # Aspas duplas: 'user' é palavra reservada no PostgreSQL
                            conn.execute(text(f'ALTER TABLE "{tabela}" ADD COLUMN "{col_name}" {col_type}'))
                            print(f"Coluna '{col_name}' adicionada em '{tabela}'")
                            colunas_adicionadas.append(f"{tabela}.{col_name}")
                        except Exception as e:
                            print(f"Erro ao adicionar '{tabela}.{col_name}': {e}")
                conn.commit()

        db.create_all()  # Garante que ciclo_historico e tabelas novas existam
        if colunas_adicionadas:
            print(f"Migracao automatica concluida! Colunas adicionadas: {colunas_adicionadas}")
        else:
            print("Migracao automatica: schema ja estah atualizado.")

    except Exception as e:
        print(f"Migracao automatica ignorada: {e}")
    finally:
        _migration_running = False


if __name__ == '__main__':
    run_migration()

