from app.models.financeiro import Financeiro
from app.repositories.base_repository import BaseRepository
from datetime import date

class FinanceiroRepository(BaseRepository):
    def __init__(self):
        super().__init__(Financeiro)

    def get_contas_em_aberto(self, revendedor_id):
        return self.model.query.filter(
            self.model.revendedor_id == revendedor_id,
            self.model.status.in_(['Em aberto', 'Parcialmente pago'])
        ).all()

    def get_contas_vencidas(self, revendedor_id):
        return self.model.query.filter(
            self.model.revendedor_id == revendedor_id,
            self.model.status.in_(['Em aberto', 'Parcialmente pago']),
            self.model.vencimento < date.today()
        ).all()

    def get_contas_pagas(self, revendedor_id):
        return self.model.query.filter_by(
            revendedor_id=revendedor_id, 
            status='Pago'
        ).all()

    def get_por_cliente(self, revendedor_id, cliente_id):
        return self.model.query.filter_by(
            revendedor_id=revendedor_id, 
            cliente_id=cliente_id
        ).all()