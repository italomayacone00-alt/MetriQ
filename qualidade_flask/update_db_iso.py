import os
import sys

# Add parent directory to path to import qualidade_flask package
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from qualidade_flask import create_app, db
from qualidade_flask.models import NormaISO, ChecklistISO

def update_database():
    app = create_app()
    with app.app_context():
        # Criar as novas tabelas
        db.create_all()
        print("Tabelas ISO criadas com sucesso!")
        
        # Verificar se as tabelas foram criadas
        try:
            # Teste de inserção para verificar se as tabelas existem
            test_iso = NormaISO(
                numero='ISO 9001',
                titulo='Sistemas de Gestão da Qualidade',
                descricao='Norma internacional para sistemas de gestão da qualidade',
                setor='Qualidade'
            )
            db.session.add(test_iso)
            db.session.commit()
            
            # Remover o teste
            db.session.delete(test_iso)
            db.session.commit()
            
            print("Verificação: Tabelas ISO estão funcionando corretamente!")
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao verificar tabelas: {e}")

if __name__ == '__main__':
    update_database()
