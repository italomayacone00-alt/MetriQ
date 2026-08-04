from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta
from ..models import User, Analise, Projeto, ProjetoFerramenta, CicloHistorico, Empresa, PlantaBaixa, ChecklistNR, ChecklistISO
from .. import db, limiter
from ..utils.security import validar_email, validar_forca_senha, gerar_token, verificar_token
from ..utils.email import enviar_email
from ..utils.oauth import google

auth = Blueprint('auth', __name__)

# ============================================
# HELPER: Verifica se o usuário está bloqueado
# ============================================
def _verificar_bloqueio(user):
    """Verifica se o usuário está temporariamente bloqueado por excesso de tentativas."""
    if user.bloqueio_ate and user.bloqueio_ate > datetime.now():
        return True
    if user.bloqueio_ate and user.bloqueio_ate <= datetime.now():
        # Bloqueio expirou, reseta
        user.tentativas_login = 0
        user.bloqueio_ate = None
        db.session.commit()
    return False

# ============================================
# HELPER: Registra tentativa de login falha
# ============================================
def _registrar_tentativa_falha(user):
    """Incrementa tentativas falhas e bloqueia se exceder o limite."""
    MAX_TENTATIVAS = 5
    TEMPO_BLOQUEIO_MINUTOS = 15

    user.tentativas_login = (user.tentativas_login or 0) + 1
    if user.tentativas_login >= MAX_TENTATIVAS:
        user.bloqueio_ate = datetime.now() + timedelta(minutes=TEMPO_BLOQUEIO_MINUTOS)
        flash(f'Conta bloqueada temporariamente por excesso de tentativas. Tente novamente em {TEMPO_BLOQUEIO_MINUTOS} minutos.', 'danger')
    db.session.commit()

# ============================================
# LOGIN
# ============================================
@auth.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
@limiter.limit("10 per minute")  # Máximo 10 tentativas de login por minuto por IP
def login_post():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    remember = request.form.get('remember', False)
    
    if not username or not password:
        flash('Preencha usuário e senha.', 'danger')
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(username=username).first()
    
    # Verifica se o usuário existe
    if not user:
        flash('Usuário ou senha inválidos.', 'danger')
        return redirect(url_for('auth.login'))
    
    # Verifica se a conta está ativa
    if user.status == 'inativo':
        flash('Esta conta está inativa. Contate o suporte.', 'danger')
        return redirect(url_for('auth.login'))
    if user.status == 'bloqueado':
        flash('Esta conta foi bloqueada. Contate o suporte.', 'danger')
        return redirect(url_for('auth.login'))
    
    # Verifica bloqueio temporário por força bruta
    if _verificar_bloqueio(user):
        flash('Conta temporariamente bloqueada. Tente novamente mais tarde.', 'danger')
        return redirect(url_for('auth.login'))
    
    # Verifica a senha
    if not check_password_hash(user.password, password):
        _registrar_tentativa_falha(user)
        flash('Usuário ou senha inválidos.', 'danger')
        return redirect(url_for('auth.login'))
    
    # --- Login bem-sucedido ---
    # Reseta tentativas falhas
    user.tentativas_login = 0
    user.bloqueio_ate = None
    user.ultimo_login = datetime.now()
    db.session.commit()
    
    login_user(user, remember=bool(remember))
    
    # Redireciona para o `next` se for seguro
    next_page = request.args.get('next')
    if next_page and next_page.startswith('/'):
        return redirect(next_page)
    
    return redirect(url_for('main.index'))

# ============================================
# LOGOUT (via POST - seguro contra CSRF)
# ============================================
@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('Sessão encerrada com sucesso.', 'info')
    return redirect(url_for('auth.login'))

# ============================================
# REGISTRO
# ============================================
@auth.route('/registro')
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    return render_template('registro.html')

@auth.route('/registro', methods=['POST'])
@limiter.limit("5 per minute")  # Máximo 5 registros por minuto por IP
def registro_post():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    confirmar_senha = request.form.get('confirmar_senha', '')
    nome_completo = request.form.get('nome_completo', '').strip()
    email = request.form.get('email', '').strip()
    telefone = request.form.get('telefone', '').strip()
    cargo = request.form.get('cargo', '').strip()
    
    # --- Validações ---
    if not username or not password:
        flash('Usuário e senha são obrigatórios.', 'danger')
        return redirect(url_for('auth.registro'))
    
    if len(username) < 3:
        flash('O usuário deve ter pelo menos 3 caracteres.', 'danger')
        return redirect(url_for('auth.registro'))
    
    if not email:
        flash('O e-mail é obrigatório.', 'danger')
        return redirect(url_for('auth.registro'))
    
    if not validar_email(email):
        flash('E-mail inválido. Verifique o endereço informado.', 'danger')
        return redirect(url_for('auth.registro'))
    
    if password != confirmar_senha:
        flash('A confirmação da senha não confere.', 'danger')
        return redirect(url_for('auth.registro'))
    
    valido, msg = validar_forca_senha(password)
    if not valido:
        flash(msg, 'danger')
        return redirect(url_for('auth.registro'))
    
    # Verifica duplicidade de usuário
    if User.query.filter_by(username=username).first():
        flash('Este nome de usuário já está em uso.', 'warning')
        return redirect(url_for('auth.registro'))
    
    # Verifica duplicidade de e-mail
    if User.query.filter_by(email=email).first():
        flash('Este e-mail já está cadastrado.', 'warning')
        return redirect(url_for('auth.registro'))
    
    # --- Cria o usuário ---
    new_user = User(
        username=username,
        password=generate_password_hash(password, method='scrypt'),
        nome_completo=nome_completo,
        email=email,
        telefone=telefone,
        cargo=cargo,
        # Plano 'free' por padrão
        plano='free',
        status='ativo',
        email_confirmado=False
    )
    db.session.add(new_user)
    db.session.commit()
    
    # --- Tenta enviar e-mail de confirmação (opcional) ---
    token = gerar_token(new_user.id, salt='confirmacao_email')
    link = url_for('auth.confirmar_email', token=token, _external=True)
    
    enviado = enviar_email(
        email,
        'Bem-vindo ao MetriQ - Confirme seu e-mail',
        'email/confirmacao.html',
        {'usuario': new_user, 'link': link}
    )
    
    if enviado:
        flash('Conta criada! Verifique seu e-mail para confirmar o cadastro.', 'success')
    else:
        # Se não conseguiu enviar e-mail (sem SMTP), mostra o link no console/log
        current_app.logger.info(f"Link de confirmação para {username}: {link}")
        flash('Conta criada com sucesso!', 'success')
    
    return redirect(url_for('auth.login'))

# ============================================
# CONFIRMAÇÃO DE E-MAIL
# ============================================
@auth.route('/confirmar-email/<token>')
def confirmar_email(token):
    user_id = verificar_token(token, salt='confirmacao_email', max_age=86400)  # 24h
    if not user_id:
        flash('Link de confirmação inválido ou expirado. Solicite um novo.', 'danger')
        return redirect(url_for('auth.login'))
    
    user = User.query.get(user_id)
    if not user:
        flash('Usuário não encontrado.', 'danger')
        return redirect(url_for('auth.login'))
    
    if user.email_confirmado:
        flash('E-mail já confirmado. Faça login.', 'info')
    else:
        user.email_confirmado = True
        db.session.commit()
        flash('E-mail confirmado com sucesso!', 'success')
    
    return redirect(url_for('auth.login'))

# ============================================
# REENVIAR CONFIRMAÇÃO DE E-MAIL
# ============================================
@auth.route('/reenviar-confirmacao', methods=['GET', 'POST'])
def reenviar_confirmacao():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        if not email:
            flash('Informe seu e-mail.', 'danger')
            return redirect(url_for('auth.reenviar_confirmacao'))
        
        user = User.query.filter_by(email=email).first()
        if user and not user.email_confirmado:
            token = gerar_token(user.id, salt='confirmacao_email')
            link = url_for('auth.confirmar_email', token=token, _external=True)
            
            enviado = enviar_email(
                user.email,
                'MetriQ - Confirme seu e-mail',
                'email/confirmacao.html',
                {'usuario': user, 'link': link}
            )
            
            if enviado:
                flash('E-mail de confirmação reenviado! Verifique sua caixa de entrada.', 'success')
            else:
                current_app.logger.info(f"Link de confirmação para {user.username}: {link}")
                flash('E-mail de confirmação gerado (verifique o console/log do servidor).', 'success')
        else:
            # Não revela se o e-mail existe ou não (segurança)
            flash('Se o e-mail estiver cadastrado, um link de confirmação foi enviado.', 'info')
        
        return redirect(url_for('auth.login'))
    
    return render_template('reenviar_confirmacao.html')

# ============================================
# RECUPERAÇÃO DE SENHA
# ============================================
@auth.route('/recuperar-senha', methods=['GET', 'POST'])
def recuperar_senha():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        if not email:
            flash('Informe seu e-mail cadastrado.', 'danger')
            return redirect(url_for('auth.recuperar_senha'))
        
        user = User.query.filter_by(email=email).first()
        if user:
            token = gerar_token(user.id, salt='recuperacao_senha', max_age=3600)  # 1h
            link = url_for('auth.redefinir_senha', token=token, _external=True)
            
            enviado = enviar_email(
                user.email,
                'MetriQ - Recuperação de Senha',
                'email/recuperar_senha.html',
                {'usuario': user, 'link': link}
            )
            
            if enviado:
                flash('E-mail de recuperação enviado! Verifique sua caixa de entrada.', 'success')
            else:
                current_app.logger.info(f"Link de recuperação para {user.username}: {link}")
                flash('Link de recuperação gerado (verifique o console/log do servidor).', 'success')
        else:
            # Não revela se o e-mail existe
            flash('Se o e-mail estiver cadastrado, um link de recuperação foi enviado.', 'info')
        
        return redirect(url_for('auth.login'))
    
    return render_template('recuperar_senha.html')

@auth.route('/redefinir-senha/<token>', methods=['GET', 'POST'])
def redefinir_senha(token):
    user_id = verificar_token(token, salt='recuperacao_senha', max_age=3600)  # 1h
    if not user_id:
        flash('Link de recuperação inválido ou expirado. Solicite um novo.', 'danger')
        return redirect(url_for('auth.recuperar_senha'))
    
    user = User.query.get(user_id)
    if not user:
        flash('Usuário não encontrado.', 'danger')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        nova_senha = request.form.get('nova_senha', '')
        confirmar_senha = request.form.get('confirmar_senha', '')
        
        if nova_senha != confirmar_senha:
            flash('A confirmação da senha não confere.', 'danger')
            return redirect(url_for('auth.redefinir_senha', token=token))
        
        valido, msg = validar_forca_senha(nova_senha)
        if not valido:
            flash(msg, 'danger')
            return redirect(url_for('auth.redefinir_senha', token=token))
        
        user.password = generate_password_hash(nova_senha, method='scrypt')
        user.tentativas_login = 0
        user.bloqueio_ate = None
        db.session.commit()
        
        flash('Senha redefinida com sucesso! Faça login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('redefinir_senha.html', token=token)

# ============================================
# PERFIL DO USUÁRIO
# ============================================
@auth.route('/perfil')
@login_required
def perfil():
    """Tela de perfil do usuário com dados, senha e estatísticas"""
    estatisticas = current_user.get_estatisticas()
    return render_template('perfil.html', user=current_user, estatisticas=estatisticas)

@auth.route('/perfil', methods=['POST'])
@login_required
def perfil_atualizar():
    """Atualiza os dados cadastrais do usuário"""
    usuario = current_user

    nome_completo = request.form.get('nome_completo', '').strip()
    email = request.form.get('email', '').strip()
    telefone = request.form.get('telefone', '').strip()
    cargo = request.form.get('cargo', '').strip()

    # Validação de e-mail
    if not email:
        flash('O e-mail é obrigatório.', 'danger')
        return redirect(url_for('auth.perfil'))
    
    if not validar_email(email):
        flash('E-mail inválido. Verifique o endereço informado.', 'danger')
        return redirect(url_for('auth.perfil'))
    
    # Verifica se o e-mail já está em uso por outro usuário
    if email != usuario.email:
        existente = User.query.filter_by(email=email).first()
        if existente:
            flash('Este e-mail já está em uso por outra conta.', 'danger')
            return redirect(url_for('auth.perfil'))
        usuario.email = email
        usuario.email_confirmado = False  # Precisa confirmar o novo e-mail
        flash('E-mail alterado. Confirme o novo endereço de e-mail.', 'warning')

    usuario.nome_completo = nome_completo
    usuario.telefone = telefone
    usuario.cargo = cargo
    db.session.commit()

    flash('Dados atualizados com sucesso!', 'success')
    return redirect(url_for('auth.perfil'))

@auth.route('/perfil/senha', methods=['POST'])
@login_required
def perfil_senha():
    """Altera a senha do usuário"""
    usuario = current_user

    senha_atual = request.form.get('senha_atual', '')
    nova_senha = request.form.get('nova_senha', '')
    confirmar_senha = request.form.get('confirmar_senha', '')

    # Validação da senha atual
    if not check_password_hash(usuario.password, senha_atual):
        flash('Senha atual incorreta.', 'danger')
        return redirect(url_for('auth.perfil'))

    # Confirmação
    if nova_senha != confirmar_senha:
        flash('A confirmação da nova senha não confere.', 'danger')
        return redirect(url_for('auth.perfil'))

# Força da senha
    valido, msg = validar_forca_senha(nova_senha)
    if not valido:
        flash(msg, 'danger')
        return redirect(url_for('auth.perfil'))

    usuario.password = generate_password_hash(nova_senha, method='scrypt')
    db.session.commit()

    flash('Senha alterada com sucesso!', 'success')
    return redirect(url_for('auth.perfil'))

# ============================================
# LOGIN COM GOOGLE (OAuth)
# ============================================
@auth.route('/login/google')
def login_google():
    """Redireciona para o Google para autenticação OAuth."""
    if google is None:
        flash('Login com Google não está configurado. Contate o administrador.', 'danger')
        return redirect(url_for('auth.login'))
    
    redirect_uri = url_for('auth.login_google_callback', _external=True)
    return google.authorize_redirect(redirect_uri)


# ============================================
# EXCLUSÃO DA CONTA
# ============================================
@auth.route('/excluir-conta', methods=['POST'])
@login_required
def excluir_conta():
    """Exclui permanentemente a conta do usuário e todos os dados associados."""
    usuario = current_user
    
    # Confirmação textual obrigatória (funciona para contas normais E OAuth/Google)
    confirmacao = request.form.get('confirmacao', '')
    if confirmacao.strip().lower() != 'excluir':
        flash('Para confirmar a exclusão, digite "EXCLUIR" no campo de confirmação.', 'danger')
        return redirect(url_for('auth.perfil'))
    
    try:
        # ==========================================
        # Delibera sobre os dados associados ao usuário
        # ==========================================
        user_id = usuario.id
        
        # 1. Análises (ferramentas)
        Analise.query.filter_by(user_id=user_id).delete()
        
        # 2. Projetos (que têm ferramentas e ciclos - cascade via delete)
        projetos = Projeto.query.filter_by(user_id=user_id).all()
        for projeto in projetos:
            # ProjetoFerramenta e CicloHistorico são excluídos via cascade
            db.session.delete(projeto)
        
        # 3. Empresas (que têm plantas, checklists, etc via cascade)
        empresas = Empresa.query.filter_by(user_id=user_id).all()
        for empresa in empresas:
            # Exclui plantas, checklists vinculados à empresa
            PlantaBaixa.query.filter_by(user_id=user_id, empresa_id=empresa.id).delete()
            ChecklistNR.query.filter_by(user_id=user_id, empresa_id=empresa.id).delete()
            ChecklistISO.query.filter_by(user_id=user_id, empresa_id=empresa.id).delete()
            db.session.delete(empresa)
        
        # 4. Plantas, checklists que não pertencem a uma empresa específica
        PlantaBaixa.query.filter_by(user_id=user_id, empresa_id=None).delete()
        ChecklistNR.query.filter_by(user_id=user_id, empresa_id=None).delete()
        ChecklistISO.query.filter_by(user_id=user_id, empresa_id=None).delete()
        
        # 5. Exclui o usuário
        db.session.delete(usuario)
        db.session.commit()
        
        # Encerra a sessão
        logout_user()
        flash('Conta excluída com sucesso. Sentiremos sua falta!', 'success')
        return redirect(url_for('auth.login'))
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao excluir conta {usuario.id}: {e}")
        flash('Erro ao excluir a conta. Tente novamente ou contate o suporte.', 'danger')
        return redirect(url_for('auth.perfil'))

# ============================================
# LOGIN COM GOOGLE (OAuth) - CALLBACK
# ============================================
@auth.route('/login/google/callback')
def login_google_callback():
    """Callback do Google após autenticação."""
    if google is None:
        flash('Login com Google não está configurado.', 'danger')
        return redirect(url_for('auth.login'))
    
    try:
        token = google.authorize_access_token()
        if not token:
            flash('Erro de autenticação com Google. Tente novamente.', 'danger')
            return redirect(url_for('auth.login'))
        
        # Busca informações do usuário no Google
        userinfo = google.parse_id_token(token)
        if not userinfo:
            # Fallback: usa userinfo endpoint
            resp = google.get('https://www.googleapis.com/oauth2/v3/userinfo')
            if not resp.ok:
                flash('Erro ao obter informações do Google.', 'danger')
                return redirect(url_for('auth.login'))
            userinfo = resp.json()
        
        google_id = userinfo.get('sub')
        email = userinfo.get('email', '')
        nome = userinfo.get('name', '')
        given_name = userinfo.get('given_name', '')
        
        if not email:
            flash('O Google não forneceu um e-mail. Use outro método de login.', 'danger')
            return redirect(url_for('auth.login'))
        
        # Verifica se já existe usuário com este e-mail
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Usuário já existe - faz login
            if user.status == 'inativo' or user.status == 'bloqueado':
                flash('Esta conta está inativa/bloqueada. Contate o suporte.', 'danger')
                return redirect(url_for('auth.login'))
            
            user.ultimo_login = datetime.now()
            db.session.commit()
            login_user(user)
            flash(f'Bem-vindo de volta, {user.nome_completo or user.username}!', 'success')
            return redirect(url_for('main.index'))
        
        # --- Criar novo usuário ---
        # Gera um username baseado no e-mail (parte antes do @)
        base_username = email.split('@')[0][:20]
        username = base_username
        contador = 1
        while User.query.filter_by(username=username).first():
            username = f"{base_username}{contador}"
            contador += 1
        
        # Senha aleatória (não usada, pois o login é via Google)
        senha_aleatoria = generate_password_hash(
            User.__tablename__ + str(datetime.now().timestamp()),
            method='scrypt'
        )
        
        new_user = User(
            username=username,
            password=senha_aleatoria,
            nome_completo=nome or given_name or username,
            email=email,
            email_confirmado=True,  # Google já confirmou o e-mail
            plano='free',
            status='ativo',
            ultimo_login=datetime.now()
        )
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        flash(f'Bem-vindo ao MetriQ, {new_user.nome_completo}!', 'success')
        return redirect(url_for('main.index'))
        
    except Exception as e:
        current_app.logger.error(f"Erro no login Google: {e}")
        flash('Erro ao autenticar com Google. Tente novamente.', 'danger')
        return redirect(url_for('auth.login'))
