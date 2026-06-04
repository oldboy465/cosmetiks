from app.models.estoque import Estoque
from app.repositories.base_repository import BaseRepository

class EstoqueRepository(BaseRepository):
    def __init__(self):
        super().__init__(Estoque)

    def get_historico_produto(self, revendedor_id, produto_id):
        return self.model.query.filter_by(
            revendedor_id=revendedor_id, 
            produto_id=produto_id
        ).order_by(self.model.data_movimentacao.desc()).all()

    def get_historico_completo(self, revendedor_id):
        return self.model.query.filter_by(
            revendedor_id=revendedor_id
        ).order_by(self.model.data_movimentacao.desc()).all()

    def delete_por_venda(self, revendedor_id, venda_id):
        movimentacoes = self.model.query.filter_by(revendedor_id=revendedor_id, venda_id=venda_id).all()
        for mov in movimentacoes:
            self.delete(mov)