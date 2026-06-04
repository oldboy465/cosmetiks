from app import db
from datetime import datetime

class Auditoria(db.Model):
    __tablename__ = 'auditorias'
    
    id = db.Column(db.Integer, primary_key=True)
    revendedor_id = db.Column(db.Integer, db.ForeignKey('revendedores.id'), nullable=True)
    usuario = db.Column(db.String(50), nullable=False)
    data_hora = db.Column(db.DateTime, default=datetime.utcnow)
    ip = db.Column(db.String(45), nullable=False)
    acao = db.Column(db.String(20), nullable=False)  # Login, Logout, Inclusão, Alteração, Exclusão
    detalhes = db.Column(db.Text, nullable=False)