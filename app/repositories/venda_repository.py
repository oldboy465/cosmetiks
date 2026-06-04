from app.models.venda import Venda, ItemVenda
from app.repositories.base_repository import BaseRepository

class VendaRepository(BaseRepository):
    def __init__(self):
        super().__init__(Venda)

    def get_vendas_por_periodo(self, revendedor_id, data_inicio, data_fim):
        return self.model.query.filter(
            self.model.revendedor_id == revendedor_id,
            self.model.data_venda >= data_inicio,
            self.model.data_venda <= data_fim
        ).order_by(self.model.data_venda.desc()).all()

    def get_vendas_por_cliente(self, revendedor_id, cliente_id):
        return self.model.query.filter_by(
            revendedor_id=revendedor_id, 
            cliente_id=cliente_id
        ).order_by(self.model.data_venda.desc()).all()

    def get_todas_ordenadas(self, revendedor_id):
        return self.model.query.filter_by(revendedor_id=revendedor_id).order_by(self.model.data_venda.desc()).all()

    def add_item(self, item_venda):
        from app import db
        db.session.add(item_venda)
        return item_venda