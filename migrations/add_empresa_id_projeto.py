"""
Migration script to add empresa_id column to Projeto table.

Run this after the migration is reviewed:
    flask shell < migrations/add_empresa_id_projeto.py
"""

from qualidade_flask import create_app, db
from qualidade_flask.models import Projeto

app = create_app()

with app.app_context():
    # Check if column already exists
    import sqlalchemy as sa
    inspector = sa.inspect(db.engine)
    columns = [col['name'] for col in inspector.get_columns('projeto')]
    
    if 'empresa_id' not in columns:
        print("Adding empresa_id column to projeto table...")
        db.engine.execute(
            'ALTER TABLE projeto ADD COLUMN empresa_id INTEGER REFERENCES empresa(id)'
        )
        print("Column added successfully!")
    else:
        print("Column empresa_id already exists in projeto table. Skipping.")
    
    print("Migration completed.")

