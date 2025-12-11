from . import db
from datetime import datetime

class Analise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50))
    titulo = db.Column(db.String(100))
    dados = db.Column(db.JSON)
    data_criacao = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'tipo': self.tipo,
            'titulo': self.titulo,
            'dados': self.dados,
            # Alteração aqui: Formata para Dia/Mês/Ano Hora:Minuto
            'data_criacao': self.data_criacao.strftime('%d/%m/%Y %H:%M') if self.data_criacao else ""
        }
