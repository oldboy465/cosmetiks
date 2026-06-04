from app import db

class Financeiro(db.Model):
    __tablename__ = 'financeiro_contas_receber'
    
    id = db.Column(db.Integer, primary_key=True)
    revendedor_id = db.Column(db.Integer, db.ForeignKey('revendedores.id'), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    venda_id = db.Column(db.Integer, db.ForeignKey('vendas.id'), nullable=False)
    
    valor = db.Column(db.Numeric(10, 2), nullable=False)
    vencimento = db.Column(db.Date, nullable=False)
    pagamento = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(30), default='Em aberto', nullable=False)
    
    cobrancas = db.relationship('Cobranca', backref='financeiro', cascade='all, delete-orphan', lazy=True)