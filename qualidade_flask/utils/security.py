"""
Utilitários de segurança: validação de e-mail, força de senha e tokens.

Tokens usam itsdangerous (já incluído no Flask) com assinatura baseada na SECRET_KEY.
"""
import re
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from flask import current_app

EMAIL_RE = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')


def validar_email(email):
    """Valida um endereço de e-mail de forma simples e eficaz."""
    return bool(EMAIL_RE.match(email or ''))


def validar_forca_senha(senha):
    """
    Valida a força da senha.
    Política: mínimo 8 caracteres, contendo letras e números.
    Retorna (bool, mensagem).
    """
    if not senha or len(senha) < 8:
        return False, 'A senha deve ter pelo menos 8 caracteres.'
    if not re.search(r'[A-Za-z]', senha) or not re.search(r'\d', senha):
        return False, 'A senha deve conter letras e números.'
    return True, ''


def gerar_token(dados, salt='default', max_age=86400):
    """Gera um token assinado com expiração (padrão 24h)."""
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'], salt=salt)
    return s.dumps(dados)


def verificar_token(token, salt='default', max_age=86400):
    """
    Verifica um token assinado.
    Retorna os dados originais se válido, ou None se inválido/expirado.
    """
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'], salt=salt)
    try:
        return s.loads(token, max_age=max_age)
    except (BadSignature, SignatureExpired):
        return None

