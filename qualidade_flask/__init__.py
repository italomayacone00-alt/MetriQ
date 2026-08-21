import os
import secrets
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Configura logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Inicializa as extensões fora da função para serem globais
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
limiter = Limiter(key_func=get_remote_address)

def create_app():
    app = Flask(__name__)
    
    # ==================================================
    # 1. CONFIGURAÇÕES DE SEGURANÇA
    # ==================================================
    # Detecta se estamos em produção (Render, DATABASE_URL, ou variável explícita)
    is_production = bool(os.environ.get('RENDER') or os.environ.get('DATABASE_URL') or os.environ.get('ENV') == 'production')

    # Chave secreta: obrigatória em produção. Em desenvolvimento, gera/usa um arquivo local para persistência.
    secret_key = os.environ.get('SECRET_KEY')
    if is_production and not secret_key:
        # Em produção, falhar rapidamente para evitar iniciar com segredo fraco ou ausente
        raise RuntimeError('SECRET_KEY obrigatória em produção. Defina a variável de ambiente SECRET_KEY.')

    if not secret_key:
        # Tenta carregar chave de um arquivo local (para persistir entre reinícios em dev)
        key_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '.secret_key')
        if os.path.exists(key_file):
            with open(key_file, 'r') as f:
                secret_key = f.read().strip()
        else:
            # Gera nova chave aleatória para desenvolvimento
            secret_key = secrets.token_hex(32)
            with open(key_file, 'w') as f:
                f.write(secret_key)
            logger.warning("⚠️ SECRET_KEY não configurada. Gerada chave aleatória local para desenvolvimento.")
            logger.warning("⚠️ Em produção, defina a variável de ambiente SECRET_KEY.")

    app.config['SECRET_KEY'] = secret_key

    # Configuração de sessão (valores seguros por padrão)
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['REMEMBER_COOKIE_DURATION'] = 30 * 24 * 3600  # 30 dias
    app.config['REMEMBER_COOKIE_HTTPONLY'] = True
    app.config['REMEMBER_COOKIE_SAMESITE'] = 'Lax'

    # Em produção força cookies seguros e Talisman (HTTPS)
    if is_production:
        app.config['SESSION_COOKIE_SECURE'] = True
        app.config['SESSION_COOKIE_HTTPONLY'] = True
        app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
        # Força HTTPS
        Talisman(app, content_security_policy=None, force_https=True)
        logger.info("🔒 Modo PRODUÇÃO: HTTPS e Talisman ativos.")
    else:
        logger.info("🔓 Modo DESENVOLVIMENTO: segurança simplificada.")
    
    # ==================================================
    # CONFIGURAÇÃO DE E-MAIL (para confirmação/recuperação)
    # ==================================================
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
    app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'true').lower() == 'true'
    app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL', 'false').lower() == 'true'
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'nao-responda@metriq.com.br')

    # ==================================================
    # BANCO DE DADOS
    # ==================================================
    database_url = os.environ.get('DATABASE_URL')

    if database_url:
        # Se estiver no Render, usa o PostgreSQL
        # Correção necessária: O Render entrega "postgres://", mas o SQLAlchemy pede "postgresql://"
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        # Se estiver no seu PC, usa o SQLite local (como era antes)
        base_dir = os.path.abspath(os.path.dirname(__file__))
        db_path = os.path.join(base_dir, 'qualidade.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ==================================================
    # 2. INICIALIZAÇÃO DAS EXTENSÕES
    # ==================================================
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)  # Proteção CSRF em formulários
    limiter.init_app(app)  # Rate limiting
    
# ==================================================
    # OAuth (Google Login)
    # ==================================================
    from .utils.oauth import configurar_oauth, google
    oauth_configurado = configurar_oauth(app)
    if oauth_configurado:
        app.logger.info("✅ Google OAuth configurado com sucesso!")
    else:
        app.logger.warning(
            "⚠️ Google OAuth não configurado. "
            "Defina GOOGLE_CLIENT_ID e GOOGLE_CLIENT_SECRET no ambiente."
        )
    
    # Define qual é a rota de login
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

    # D. Módulo de Projetos
    from .blueprints.projects import projects as projects_bp
    app.register_blueprint(projects_bp)

    # E. Módulo de Normas Regulamentadoras (NRs)
    from .blueprints.nr import nr as nr_bp
    app.register_blueprint(nr_bp)

# F. Módulo de Normas ISO
    from .blueprints.iso import iso as iso_bp
    app.register_blueprint(iso_bp)

# G. Módulo de Planta Baixa
    from .blueprints.planta_baixa import planta_baixa as planta_baixa_bp
    app.register_blueprint(planta_baixa_bp)

# H. Módulo de Gestão da Empresa
    from .blueprints.empresa import empresa as empresa_bp
    app.register_blueprint(empresa_bp)

    # ==================================================
    # 4. CARREGAMENTO DO USUÁRIO
    # ==================================================
    from .models import User, NormaRegulamentadora, NormaISO

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Cria as tabelas do banco se não existirem
    with app.app_context():
        db.create_all()
        
        # ==================================================
        # POPULAÇÃO AUTOMÁTICA - Primeira execução
        # ==================================================
        # Verifica se o banco já tem dados
        from .seed_data import iso_9001_data, iso_14001_data, iso_45001_data, nrs_basicas_data
        
        # Popula ISOs automaticamente se não existirem
        if NormaISO.query.count() == 0:
            print("Populando ISOs automaticamente...")
            for iso_data in [iso_9001_data, iso_14001_data, iso_45001_data]:
                existing = NormaISO.query.filter_by(numero=iso_data['numero']).first()
                if not existing:
                    new_iso = NormaISO(**iso_data)
                    db.session.add(new_iso)
            db.session.commit()
            print(f"{NormaISO.query.count()} ISOs populadas automaticamente!")
        
        # Popula NRs automaticamente se não existirem
        if NormaRegulamentadora.query.count() == 0:
            print("Populando NRs automaticamente...")
            for nr_data in nrs_basicas_data:
                existing = NormaRegulamentadora.query.filter_by(numero=nr_data['numero']).first()
                if not existing:
                    new_nr = NormaRegulamentadora(**nr_data)
                    db.session.add(new_nr)
            db.session.commit()
            print(f"{NormaRegulamentadora.query.count()} NRs populadas automaticamente!")

        # ==================================================
        # 5. MIGRAÇÃO AUTOMÁTICA DO BANCO DE DADOS
        # ==================================================
        # Verifica se o schema está atualizado e adiciona colunas faltantes
        try:
            from .migrate_projeto_columns import run_migration_auto
            run_migration_auto()
        except Exception as e:
            print(f"Erro na migração automática (ignorado): {e}")

    # Registrar comandos CLI personalizados
    from .seed_data import register_commands
    register_commands(app)

    return app
