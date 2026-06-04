from app import db
from datetime import datetime

class Cliente(db.Model):
    __tablename__ = 'clientes'
    
    id = db.Column(db.Integer, primary_key=True)
    revendedor_id = db.Column(db.Integer, db.ForeignKey('revendedores.id'), nullable=False)
    
    nome = db.Column(db.String(150), nullable=False)
    telefone = db.Column(db.String(20), nullable=True)
    whatsapp = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    endereco = db.Column(db.Text, nullable=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    observacoes = db.Column(db.Text, nullable=True)