import os
import sys

# Add parent directory to path to import qualidade_flask package
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from qualidade_flask import create_app, db
from qualidade_flask.models import NormaRegulamentadora

def update_schema():
    """Add glossario column to database"""
    app = create_app()
    
    with app.app_context():
        try:
            # Add the glossario column if it doesn't exist
            with db.engine.connect() as conn:
                # Check if column exists
                result = conn.execute(db.text("PRAGMA table_info(norma_regulamentadora)"))
                columns = [row[1] for row in result]
                
                if 'glossario' not in columns:
                    print("Adicionando coluna glossario...")
                    conn.execute(db.text("ALTER TABLE norma_regulamentadora ADD COLUMN glossario JSON"))
                    conn.commit()
                    print("Coluna glossario adicionada com sucesso!")
                else:
                    print("Coluna glossario já existe no banco de dados.")
                    
        except Exception as e:
            print(f"Erro ao atualizar esquema: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    update_schema()
