from app import db

class Produto(db.Model):
    __tablename__ = 'produtos'
    
    id = db.Column(db.Integer, primary_key=True)
    revendedor_id = db.Column(db.Integer, db.ForeignKey('revendedores.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    marca_id = db.Column(db.Integer, db.ForeignKey('marcas.id'), nullable=False)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedores.id'), nullable=False)
    
    nome = db.Column(db.String(150), nullable=False)
    codigo_barras = db.Column(db.String(50), nullable=True)
    descricao = db.Column(db.Text, nullable=True)
    quantidade_estoque = db.Column(db.Integer, default=0, nullable=False)
    estoque_minimo = db.Column(db.Integer, default=0, nullable=False)
    preco_custo = db.Column(db.Numeric(10, 2), nullable=False)
    preco_venda = db.Column(db.Numeric(10, 2), nullable=False)
    data_compra = db.Column(db.Date, nullable=True)
    situacao = db.Column(db.String(20), default='Ativo')

    movimentacoes_estoque = db.relationship('Estoque', backref='produto', lazy=True)