"""
Script de migração: Adiciona colunas PDCA ao banco de dados existente
Execute: python qualidade_flask/migrate_pdca.py
"""
import sqlite3
import os

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'qualidade.db')

print(f"Conectando ao banco: {db_path}")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Verificar colunas existentes na tabela projeto
cursor.execute('PRAGMA table_info(projeto)')
cols = [c[1] for c in cursor.fetchall()]
print(f"Colunas atuais em 'projeto': {cols}")

# Colunas que precisam existir
required = [
    ('fase_atual', "VARCHAR(20) DEFAULT 'plan'"),
    ('ciclo_atual', 'INTEGER DEFAULT 1'),
    ('documento_padronizacao', 'JSON'),
    ('data_conclusao_ciclo', 'DATETIME')
]

added = []
for col_name, col_type in required:
    if col_name not in cols:
        try:
            cursor.execute(f'ALTER TABLE projeto ADD COLUMN {col_name} {col_type}')
            added.append(col_name)
            print(f"  + Coluna '{col_name}' adicionada!")
        except Exception as e:
            print(f"  ! Erro ao adicionar '{col_name}': {e}")
    else:
        print(f"  - Coluna '{col_name}' ja existe.")

# Verificar se tabela ciclo_historico existe
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ciclo_historico'")
if not cursor.fetchone():
    cursor.execute('''
        CREATE TABLE ciclo_historico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            projeto_id INTEGER NOT NULL,
            ciclo INTEGER NOT NULL,
            fase_concluida VARCHAR(20) DEFAULT 'act',
            ferramentas_snapshot JSON,
            documento_padronizacao JSON,
            data_conclusao DATETIME DEFAULT CURRENT_TIMESTAMP,
            metricas_ciclo JSON,
            FOREIGN KEY (projeto_id) REFERENCES projeto(id)
        )
    ''')
    print("  + Tabela 'ciclo_historico' criada!")
else:
    print("  - Tabela 'ciclo_historico' ja existe.")

conn.commit()
conn.close()
print(f"\nMigracao concluida! Colunas adicionadas: {added}")
