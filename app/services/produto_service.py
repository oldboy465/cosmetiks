from app.repositories.produto_repository import ProdutoRepository
from app.models.produto import Produto
from decimal import Decimal

class ProdutoService:
    def __init__(self):
        self.produto_repo = ProdutoRepository()

    def listar_todos(self, revendedor_id):
        return self.produto_repo.get_todos_ordenados(revendedor_id)

    def buscar_com_filtros(self, revendedor_id, nome=None, categoria_id=None, marca_id=None, fornecedor_id=None):
        return self.produto_repo.buscar_com_filtros(revendedor_id, nome, categoria_id, marca_id, fornecedor_id)

    def criar_produto(self, revendedor_id, categoria_id, marca_id, fornecedor_id, nome, codigo_barras, descricao, estoque_minimo, preco_custo, preco_venda, data_compra, situacao):
        if not nome or str(nome).strip() == "":
            raise ValueError("O nome do produto e obrigatorio.")
        if preco_custo is None or Decimal(preco_custo) < 0:
            raise ValueError("O preco de custo deve ser maior ou igual a zero.")
        if preco_venda is None or Decimal(preco_venda) < 0:
            raise ValueError("O preco de venda deve ser maior ou igual a zero.")

        novo_produto = Produto(
            revendedor_id=revendedor_id,
            categoria_id=categoria_id,
            marca_id=marca_id,
            fornecedor_id=fornecedor_id,
            nome=nome.strip(),
            codigo_barras=codigo_barras.strip() if codigo_barras else None,
            descricao=descricao.strip() if descricao else None,
            quantidade_estoque=0,
            estoque_minimo=int(estoque_minimo) if estoque_minimo else 0,
            preco_custo=Decimal(preco_custo),
            preco_venda=Decimal(preco_venda),
            data_compra=data_compra,
            situacao=situacao if situacao else 'Ativo'
        )
        self.produto_repo.add(novo_produto)
        self.produto_repo.commit()
        return novo_produto

    def atualizar_produto(self, id_produto, revendedor_id, categoria_id, marca_id, fornecedor_id, nome, codigo_barras, descricao, estoque_minimo, preco_custo, preco_venda, data_compra, situacao):
        produto = self.produto_repo.get_by_id_and_revendedor(id_produto, revendedor_id)
        if not produto:
            raise ValueError("Produto nao encontrado.")
        
        if not nome or str(nome).strip() == "":
            raise ValueError("O nome do produto e obrigatorio.")
        if preco_custo is None or Decimal(preco_custo) < 0:
            raise ValueError("O preco de custo deve ser maior ou igual a zero.")
        if preco_venda is None or Decimal(preco_venda) < 0:
            raise ValueError("O preco de venda deve ser maior ou igual a zero.")

        produto.categoria_id = categoria_id
        produto.marca_id = marca_id
        produto.fornecedor_id = fornecedor_id
        produto.nome = nome.strip()
        produto.codigo_barras = codigo_barras.strip() if codigo_barras else None
        produto.descricao = descricao.strip() if descricao else None
        produto.estoque_minimo = int(estoque_minimo) if estoque_minimo else 0
        produto.preco_custo = Decimal(preco_custo)
        produto.preco_venda = Decimal(preco_venda)
        produto.data_compra = data_compra
        produto.situacao = situacao

        self.produto_repo.commit()
        return produto

    def excluir_produto(self, id_produto, revendedor_id):
        produto = self.produto_repo.get_by_id_and_revendedor(id_produto, revendedor_id)
        if not produto:
            raise ValueError("Produto nao encontrado.")
        
        if produto.movimentacoes_estoque:
            raise ValueError("Nao e possivel excluir um produto que possui movimentacoes de estoque registradas.")

        self.produto_repo.delete(produto)
        self.produto_repo.commit()
        return True

    def verificar_produtos_estoque_baixo(self, revendedor_id):
        return self.produto_repo.verificar_estoque_baixo(revendedor_id)