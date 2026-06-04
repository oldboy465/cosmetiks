from app import db
from datetime import datetime

class Venda(db.Model):
    __tablename__ = 'vendas'
    
    id = db.Column(db.Integer, primary_key=True)
    revendedor_id = db.Column(db.Integer, db.ForeignKey('revendedores.id'), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    
    data_venda = db.Column(db.DateTime, default=datetime.utcnow)
    valor_total = db.Column(db.Numeric(10, 2), nullable=False)
    desconto_valor = db.Column(db.Numeric(10, 2), default=0.00, nullable=False)
    desconto_percentual = db.Column(db.Numeric(5, 2), default=0.00, nullable=False)
    situacao = db.Column(db.String(30), default='Não pago', nullable=False)
    forma_pagamento = db.Column(db.String(50), nullable=False)
    
    itens = db.relationship('ItemVenda', backref='venda', cascade='all, delete-orphan', lazy=True)
    parcelas = db.relationship('Parcelamento', backref='venda', cascade='all, delete-orphan', lazy=True)
    financeiro = db.relationship('Financeiro', backref='venda', cascade='all, delete-orphan', lazy=True)
    movimentacoes_estoque = db.relationship('Estoque', backref='venda', lazy=True)

class ItemVenda(db.Model):
    __tablename__ = 'itens_venda'
    
    id = db.Column(db.Integer, primary_key=True)
    venda_id = db.Column(db.Integer, db.ForeignKey('vendas.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    
    quantidade = db.Column(db.Integer, nullable=False)
    valor_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    valor_total = db.Column(db.Numeric(10, 2), nullable=False)