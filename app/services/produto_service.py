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
            raise ValueError("O nome do produto é obrigatório.")
        
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
            preco_custo=Decimal(str(preco_custo or 0)),
            preco_venda=Decimal(str(preco_venda or 0)),
            data_compra=data_compra,
            situacao=situacao if situacao else 'Ativo'
        )
        self.produto_repo.add(novo_produto)
        self.produto_repo.commit()
        return novo_produto

    def criar_produto_avancado(self, revendedor_id, **kwargs):
        """Cria o produto e registra saldo inicial no histórico se houver quantidade informada."""
        quantidade_inicial = int(kwargs.pop('quantidade_estoque', 0))
        novo_prod = self.criar_produto(revendedor_id, **kwargs)
        
        if quantidade_inicial > 0:
            from app.services.estoque_service import EstoqueService
            EstoqueService().registrar_movimentacao(
                revendedor_id=revendedor_id,
                produto_id=novo_prod.id,
                tipo='Entrada',
                motivo='Compra',
                quantidade=quantidade_inicial,
                observacoes="Lançamento de saldo inicial via Estoque Geral."
            )
        return novo_prod

    def atualizar_produto_avancado(self, id_produto, revendedor_id, **kwargs):
        """Atualiza o produto e gera movimentação de ajuste se a quantidade mudar."""
        produto = self.produto_repo.get_by_id_and_revendedor(id_produto, revendedor_id)
        if not produto:
            raise ValueError("Produto não encontrado.")
            
        nova_qtd = kwargs.get('quantidade_estoque')
        if nova_qtd is not None:
            nova_qtd = int(nova_qtd)
            if nova_qtd != produto.quantidade_estoque:
                diff = nova_qtd - produto.quantidade_estoque
                from app.services.estoque_service import EstoqueService
                EstoqueService().registrar_movimentacao(
                    revendedor_id=revendedor_id,
                    produto_id=id_produto,
                    tipo='Entrada' if diff > 0 else 'Saida',
                    motivo='Ajuste',
                    quantidade=abs(diff),
                    observacoes=f"Ajuste manual de saldo via Estoque Geral (de {produto.quantidade_estoque} para {nova_qtd})."
                )
                produto.quantidade_estoque = nova_qtd

        # Atualização dos demais campos
        produto.nome = kwargs.get('nome', produto.nome)
        produto.codigo_barras = kwargs.get('codigo_barras', produto.codigo_barras)
        produto.categoria_id = kwargs.get('categoria_id', produto.categoria_id)
        produto.marca_id = kwargs.get('marca_id', produto.marca_id)
        produto.fornecedor_id = kwargs.get('fornecedor_id', produto.fornecedor_id)
        produto.preco_custo = Decimal(str(kwargs.get('preco_custo', produto.preco_custo)))
        produto.preco_venda = Decimal(str(kwargs.get('preco_venda', produto.preco_venda)))
        produto.estoque_minimo = int(kwargs.get('estoque_minimo', produto.estoque_minimo))
        produto.data_compra = kwargs.get('data_compra', produto.data_compra)
        produto.situacao = kwargs.get('situacao', produto.situacao)
        produto.descricao = kwargs.get('descricao', produto.descricao)
        
        self.produto_repo.commit()
        return produto

    def excluir_produto(self, id_produto, revendedor_id):
        produto = self.produto_repo.get_by_id_and_revendedor(id_produto, revendedor_id)
        if not produto:
            raise ValueError("Produto não encontrado.")
        
        if produto.movimentacoes_estoque:
            # Em vez de bloquear, apagamos o histórico ou validamos se pode ser apagado
            # Aqui respeitamos o isolamento por revendedor_id conforme requisitado
            from app.models.estoque import Estoque
            Estoque.query.filter_by(produto_id=id_produto, revendedor_id=revendedor_id).delete()

        self.produto_repo.delete(produto)
        self.produto_repo.commit()
        return True

    def verificar_produtos_estoque_baixo(self, revendedor_id):
        return self.produto_repo.verificar_estoque_baixo(revendedor_id)