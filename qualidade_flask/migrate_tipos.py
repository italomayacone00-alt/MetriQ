"""Migração: Adiciona colunas tipo e norma_associada ao banco"""
import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'qualidade.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Verificar colunas existentes
cursor.execute('PRAGMA table_info(projeto)')
cols = [c[1] for c in cursor.fetchall()]

if 'tipo' not in cols:
    cursor.execute("ALTER TABLE projeto ADD COLUMN tipo VARCHAR(20) DEFAULT 'pdca'")
    print('✅ Coluna tipo adicionada')
else:
    print('ℹ️ Coluna tipo já existe')

if 'norma_associada' not in cols:
    cursor.execute('ALTER TABLE projeto ADD COLUMN norma_associada VARCHAR(50)')
    print('✅ Coluna norma_associada adicionada')
else:
    print('ℹ️ Coluna norma_associada já existe')

conn.commit()
conn.close()
print('Migração concluída!')
