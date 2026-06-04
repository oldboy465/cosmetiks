from app.models.cobranca import Cobranca
from app.repositories.base_repository import BaseRepository

class CobrancaRepository(BaseRepository):
    def __init__(self):
        super().__init__(Cobranca)

    def get_historico_por_conta(self, revendedor_id, financeiro_id):
        return self.model.query.filter_by(
            revendedor_id=revendedor_id,
            financeiro_id=financeiro_id
        ).order_by(self.model.data_disparo.desc()).all()