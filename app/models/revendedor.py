from app import db
from datetime import datetime

class Revendedor(db.Model):
    __tablename__ = 'revendedores'
    
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(150), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    data_nascimento = db.Column(db.Date, nullable=True)
    sexo = db.Column(db.String(20), nullable=True)
    telefone = db.Column(db.String(20), nullable=True)
    whatsapp = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    
    cep = db.Column(db.String(9), nullable=True)
    logradouro = db.Column(db.String(150), nullable=True)
    numero = db.Column(db.String(20), nullable=True)
    complemento = db.Column(db.String(100), nullable=True)
    bairro = db.Column(db.String(100), nullable=True)
    cidade = db.Column(db.String(100), nullable=True)
    estado = db.Column(db.String(2), nullable=True)
    
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    situacao = db.Column(db.String(20), default='Ativo')  # Ativo, Inativo, Bloqueado
    
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    senha_criptografada = db.Column(db.String(255), nullable=False)
    ultimo_acesso = db.Column(db.DateTime, nullable=True)
    observacoes = db.Column(db.Text, nullable=True)

    # Relacionamentos para garantir a integridade referencial em cascata lógica
    auditorias = db.relationship('Auditoria', backref='revendedor', lazy=True)
    clientes = db.relationship('Cliente', backref='revendedor', lazy=True)
    fornecedores = db.relationship('Fornecedor', backref='revendedor', lazy=True)