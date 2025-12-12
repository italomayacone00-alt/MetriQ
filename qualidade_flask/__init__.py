import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_talisman import Talisman

# Inicializa as extensões fora da função para serem globais
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    
    # ==================================================
    # 1. CONFIGURAÇÕES
    # ==================================================
    # Chave secreta (Tenta pegar do Render, senão usa a padrão)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'chave_desenvolvimento_123')
    
    # Segurança de Cookies (Só ativa se estiver no Render/Produção)
    if os.environ.get('RENDER'):
        app.config['SESSION_COOKIE_SECURE'] = True
        app.config['SESSION_COOKIE_HTTPONLY'] = True
        app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
        # Força HTTPS
        Talisman(app, content_security_policy=None)

    # Configuração do Banco de Dados SQLite
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, 'qualidade.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ==================================================
    # 2. INICIALIZAÇÃO DAS EXTENSÕES
    # ==================================================
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app) # Proteção contra ataques de formulário
    
    # Define qual é a rota de login (para onde ir se não estiver logado)
    # 'auth.login' significa: Blueprint 'auth', função 'login'
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Por favor, faça login para acessar o sistema."
    login_manager.login_message_category = "warning"

    # ==================================================
    # 3. REGISTRO DOS BLUEPRINTS (ROTAS)
    # ==================================================
    
    # A. Módulo Principal (Dashboard, Salvar, Excluir)
    from .blueprints.main import main as main_bp
    app.register_blueprint(main_bp)

    # B. Módulo de Ferramentas (Pareto, Ishikawa, etc)
    from .blueprints.tools import tools as tools_bp
    app.register_blueprint(tools_bp)

    # C. Módulo de Autenticação (Login, Registro)
    from .blueprints.auth import auth as auth_bp
    app.register_blueprint(auth_bp)

    # ==================================================
    # 4. CARREGAMENTO DO USUÁRIO
    # ==================================================
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Cria as tabelas do banco se não existirem
    with app.app_context():
        db.create_all()

    return app
#36f852241dca82a3e9ff61ed31d62323