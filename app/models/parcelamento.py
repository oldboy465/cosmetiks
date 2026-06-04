from app import db

class Parcelamento(db.Model):
    __tablename__ = 'parcelamentos'
    
    id = db.Column(db.Integer, primary_key=True)
    revendedor_id = db.Column(db.Integer, db.ForeignKey('revendedores.id'), nullable=False)
    venda_id = db.Column(db.Integer, db.ForeignKey('vendas.id'), nullable=False)
    
    quantidade_parcelas = db.Column(db.Integer, nullable=False)
    valor_parcela = db.Column(db.Numeric(10, 2), nullable=False)
    data_vencimento = db.Column(db.Date, nullable=False)
    situacao_parcela = db.Column(db.String(20), default='Aberta', nullable=False)