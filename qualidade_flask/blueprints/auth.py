from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
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

    new_user = User(username=username, password=generate_password_hash(password, method='scrypt'))
    db.session.add(new_user)
    db.session.commit()
    
    flash('Conta criada! Faça login.', 'success')
    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))