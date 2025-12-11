import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Instancia o banco de dados globalmente
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # ==============================================================================
    # CORREÇÃO 1: CAMINHO ABSOLUTO DO BANCO
    # Isso garante que o Python encontre o arquivo qualidade.db na pasta 'app'
    # ==============================================================================
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, 'qualidade.db')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # CORREÇÃO 2: SECRET_KEY
    # Necessária para o Flask processar sessões e mensagens sem erros silenciosos
    app.config['SECRET_KEY'] = 'chave_de_seguranca_essencial'
    
    db.init_app(app)

    # Importar e registrar Blueprints
    # Certifique-se de que a pasta se chama 'blueprints' e o arquivo 'main.py'
    from .blueprints.main import main as main_bp
    app.register_blueprint(main_bp)

    # (Se você tiver o tools, descomente abaixo)
    from .blueprints.tools import tools as tools_bp
    app.register_blueprint(tools_bp, url_prefix='/ferramenta')

    # Criar tabelas
    from .models import Analise
    with app.app_context():
        db.create_all()
        # Debug: Mostra no terminal onde o banco foi criado
        print(f"--> Banco de dados conectado em: {db_path}")

    return app
#d63c0b752307dc531f2941255d0779d0