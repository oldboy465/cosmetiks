from app.repositories.financeiro_repository import FinanceiroRepository
from app.repositories.venda_repository import VendaRepository
from datetime import datetime
from decimal import Decimal

class FinanceiroService:
    def __init__(self):
        self.financeiro_repo = FinanceiroRepository()
        self.venda_repo = VendaRepository()

    def obter_contas_em_aberto(self, revendedor_id):
        return self.financeiro_repo.get_contas_em_aberto(revendedor_id)

    def obter_contas_vencidas(self, revendedor_id):
        return self.financeiro_repo.get_contas_vencidas(revendedor_id)

    def obter_contas_pagas(self, revendedor_id):
        return self.financeiro_repo.get_contas_pagas(revendedor_id)

    def registrar_pagamento(self, id_financeiro, revendedor_id, valor_pago):
        conta = self.financeiro_repo.get_by_id_and_revendedor(id_financeiro, revendedor_id)
        if not conta:
            raise ValueError("Conta a receber nao encontrada.")

        v_pago = Decimal(str(valor_pago))
        if v_pago <= 0:
            raise ValueError("O valor pago deve ser maior que zero.")

        if v_pago >= conta.valor:
            conta.status = 'Pago'
            conta.pagamento = datetime.utcnow()
        else:
            conta.status = 'Parcialmente pago'
            conta.valor -= v_pago

        venda = self.venda_repo.get_by_id_and_revendedor(conta.venda_id, revendedor_id)
        if venda:
            venda.situacao = conta.status

        self.financeiro_repo.commit()
        self.venda_repo.commit()
        return conta