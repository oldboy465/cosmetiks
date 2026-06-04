from app import db

class Fornecedor(db.Model):
    __tablename__ = 'fornecedores'
    
    id = db.Column(db.Integer, primary_key=True)
    revendedor_id = db.Column(db.Integer, db.ForeignKey('revendedores.id'), nullable=False)
    
    nome = db.Column(db.String(150), nullable=False)
    telefone = db.Column(db.String(20), nullable=True)
    whatsapp = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    observacoes = db.Column(db.Text, nullable=True)

    # Relacionamento reverso para mapeamento nos módulos subsequentes
    produtos = db.relationship('Produto', backref='fornecedor', lazy=True)