from app.models.produto import Produto
from app.repositories.base_repository import BaseRepository

class ProdutoRepository(BaseRepository):
    def __init__(self):
        super().__init__(Produto)

    def buscar_por_codigo_barras(self, revendedor_id, codigo_barras):
        return self.model.query.filter_by(revendedor_id=revendedor_id, codigo_barras=codigo_barras).first()

    def verificar_estoque_baixo(self, revendedor_id):
        return self.model.query.filter(
            self.model.revendedor_id == revendedor_id,
            self.model.quantidade_estoque <= self.model.estoque_minimo
        ).order_by(self.model.nome.asc()).all()

    def buscar_com_filtros(self, revendedor_id, nome=None, categoria_id=None, marca_id=None, fornecedor_id=None):
        query = self.model.query.filter_by(revendedor_id=revendedor_id)
        if nome:
            query = query.filter(self.model.nome.ilike(f'%{nome}%'))
        if categoria_id:
            query = query.filter_by(categoria_id=categoria_id)
        if marca_id:
            query = query.filter_by(marca_id=marca_id)
        if fornecedor_id:
            query = query.filter_by(fornecedor_id=fornecedor_id)
        return query.order_by(self.model.nome.asc()).all()

    def get_todos_ordenados(self, revendedor_id):
        return self.model.query.filter_by(revendedor_id=revendedor_id).order_by(self.model.nome.asc()).all()