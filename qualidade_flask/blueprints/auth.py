from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from ..models import User
from .. import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        flash('Login inválido.', 'danger')
        return redirect(url_for('auth.login'))

    login_user(user)
    return redirect(url_for('main.index')) # Vai para o Dashboard

@auth.route('/registro')
def registro():
    return render_template('registro.html')

@auth.route('/registro', methods=['POST'])
def registro_post():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()

    if user:
        flash('Usuário já existe!', 'warning')
        return redirect(url_for('auth.registro'))

    new_user = User(
        username=username,
        password=generate_password_hash(password, method='scrypt'),
        nome_completo=request.form.get('nome_completo', '').strip(),
        email=request.form.get('email', '').strip(),
        telefone=request.form.get('telefone', '').strip(),
        cargo=request.form.get('cargo', '').strip()
    )
    db.session.add(new_user)
    db.session.commit()
    
    flash('Conta criada! Faça login.', 'success')
    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

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

    # Validação simples de e-mail
    if email and ('@' not in email or '.' not in email.split('@')[-1]):
        flash('E-mail inválido. Verifique o endereço informado.', 'danger')
        return redirect(url_for('auth.perfil'))

    usuario.nome_completo = nome_completo
    usuario.email = email
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

    # Validação da nova senha
    if len(nova_senha) < 6:
        flash('A nova senha deve ter pelo menos 6 caracteres.', 'danger')
        return redirect(url_for('auth.perfil'))

    if nova_senha != confirmar_senha:
        flash('A confirmação da nova senha não confere.', 'danger')
        return redirect(url_for('auth.perfil'))

    usuario.password = generate_password_hash(nova_senha, method='scrypt')
    db.session.commit()

    flash('Senha alterada com sucesso!', 'success')
    return redirect(url_for('auth.perfil'))

