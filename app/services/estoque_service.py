from app.repositories.estoque_repository import EstoqueRepository
from app.repositories.produto_repository import ProdutoRepository
from app.models.estoque import Estoque
from datetime import datetime

class EstoqueService:
    def __init__(self):
        self.estoque_repo = EstoqueRepository()
        self.produto_repo = ProdutoRepository()

    def registrar_movimentacao(self, revendedor_id, produto_id, tipo, motivo, quantidade, observacoes=None, venda_id=None, data_movimentacao=None):
        if int(quantidade) <= 0:
            raise ValueError("A quantidade da movimentacao deve ser maior que zero.")
        if tipo not in ['Entrada', 'Saida']:
            raise ValueError("Tipo de movimentacao invalido.")
        if motivo not in ['Compra', 'Ajuste', 'Venda', 'Perda', 'Devolucao']:
            raise ValueError("Motivo de movimentacao invalido.")

        produto = self.produto_repo.get_by_id_and_revendedor(produto_id, revendedor_id)
        if not produto:
            raise ValueError("Produto nao encontrado para movimentacao.")

        if tipo == 'Entrada':
            produto.quantidade_estoque += int(quantidade)
        elif tipo == 'Saida':
            if produto.quantidade_estoque < int(quantidade) and motivo == 'Venda':
                raise ValueError(f"Estoque insuficiente para o produto {produto.nome}. Disponivel: {produto.quantidade_estoque}.")
            produto.quantidade_estoque -= int(quantidade)

        # Processamento e injeção da data informada manualmente
        data_mov = datetime.utcnow()
        if data_movimentacao:
            if isinstance(data_movimentacao, str):
                try:
                    data_mov = datetime.strptime(data_movimentacao, '%Y-%m-%d')
                except ValueError:
                    pass
            elif isinstance(data_movimentacao, datetime):
                data_mov = data_movimentacao

        movimentacao = Estoque(
            revendedor_id=revendedor_id,
            produto_id=produto_id,
            venda_id=venda_id,
            tipo=tipo,
            motivo=motivo,
            quantidade=int(quantidade),
            data_movimentacao=data_mov,
            observacoes=observacoes
        )
        
        self.estoque_repo.add(movimentacao)
        self.estoque_repo.commit()
        self.produto_repo.commit()
        return movimentacao

    def obter_historico_produto(self, revendedor_id, produto_id):
        return self.estoque_repo.get_historico_produto(revendedor_id, produto_id)

    def obter_historico_completo(self, revendedor_id):
        return self.estoque_repo.get_historico_completo(revendedor_id)