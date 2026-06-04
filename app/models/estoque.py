from app import db
from datetime import datetime

class Estoque(db.Model):
    __tablename__ = 'movimentacoes_estoque'
    
    id = db.Column(db.Integer, primary_key=True)
    revendedor_id = db.Column(db.Integer, db.ForeignKey('revendedores.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    venda_id = db.Column(db.Integer, db.ForeignKey('vendas.id'), nullable=True)
    
    tipo = db.Column(db.String(20), nullable=False)  # Entrada, Saída
    motivo = db.Column(db.String(50), nullable=False)  # Compra, Ajuste, Venda, Perda, Devolução
    quantidade = db.Column(db.Integer, nullable=False)
    data_movimentacao = db.Column(db.DateTime, default=datetime.utcnow)
    observacoes = db.Column(db.Text, nullable=True)