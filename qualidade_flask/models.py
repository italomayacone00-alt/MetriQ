from . import db
from flask_login import UserMixin
from datetime import datetime

# Tabela de Usuários
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    # Cria a relação: Um usuário tem várias análises
    analises = db.relationship('Analise', backref='dono', lazy=True)

# Tabela de Análises
class Analise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50))   # Ex: 'pareto', 'ishikawa'
    titulo = db.Column(db.String(100))
    dados = db.Column(db.JSON)        # Salva o JSON completo (com gráfico e tudo)
    data_criacao = db.Column(db.DateTime, default=datetime.now)
    
    # --- A MUDANÇA IMPORTANTE ESTÁ AQUI ---
    # Coluna que guarda o ID de quem criou
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'tipo': self.tipo,
            'titulo': self.titulo,
            'dados': self.dados,
            'data_criacao': self.data_criacao.strftime('%d/%m/%Y %H:%M') if self.data_criacao else ""
        }