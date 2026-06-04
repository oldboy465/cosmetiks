from app import db

class Marca(db.Model):
    __tablename__ = 'marcas'
    
    id = db.Column(db.Integer, primary_key=True)
    revendedor_id = db.Column(db.Integer, db.ForeignKey('revendedores.id'), nullable=False)
    
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)

    produtos = db.relationship('Produto', backref='marca', lazy=True)