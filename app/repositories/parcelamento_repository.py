from app.models.parcelamento import Parcelamento
from app.repositories.base_repository import BaseRepository

class ParcelamentoRepository(BaseRepository):
    def __init__(self):
        super().__init__(Parcelamento)

    def get_por_venda(self, revendedor_id, venda_id):
        return self.model.query.filter_by(
            revendedor_id=revendedor_id, 
            venda_id=venda_id
        ).all()

    def get_por_status(self, revendedor_id, status):
        return self.model.query.filter_by(
            revendedor_id=revendedor_id, 
            situacao_parcela=status
        ).all()