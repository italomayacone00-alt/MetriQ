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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'tipo': self.tipo,
            'titulo': self.titulo,
            'dados': self.dados,
            'data_criacao': self.data_criacao.strftime('%d/%m/%Y %H:%M') if self.data_criacao else ""
        }

class Projeto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    objetivo = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    ferramentas = db.relationship('ProjetoFerramenta', backref='projeto', lazy=True, cascade="all, delete-orphan")

class ProjetoFerramenta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projeto_id = db.Column(db.Integer, db.ForeignKey('projeto.id'), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    dados = db.Column(db.JSON)
    analise_ia = db.Column(db.Text)
    data_criacao = db.Column(db.DateTime, default=datetime.now)