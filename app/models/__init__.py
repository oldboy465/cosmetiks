# Importação centralizada para garantir que o Flask-Migrate e SQLAlchemy 
# mapeiem todas as entidades do ecossistema CosmetiKS.
from app.models.revendedor import Revendedor
from app.models.auditoria import Auditoria
from app.models.cliente import Cliente
from app.models.fornecedor import Fornecedor
from app.models.categoria import Categoria
from app.models.marca import Marca
from app.models.produto import Produto
from app.models.estoque import Estoque
from app.models.venda import Venda, ItemVenda
from app.models.parcelamento import Parcelamento
from app.models.financeiro import Financeiro
from app.models.cobranca import Cobranca