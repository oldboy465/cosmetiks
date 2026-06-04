from app import db
from datetime import datetime

class Cobranca(db.Model):
    __tablename__ = 'cobrancas_historico'
    
    id = db.Column(db.Integer, primary_key=True)
    revendedor_id = db.Column(db.Integer, db.ForeignKey('revendedores.id'), nullable=False)
    financeiro_id = db.Column(db.Integer, db.ForeignKey('financeiro_contas_receber.id'), nullable=False)
    
    modelo_utilizado = db.Column(db.String(30), nullable=False)
    mensagem_conteudo = db.Column(db.Text, nullable=False)
    data_disparo = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)