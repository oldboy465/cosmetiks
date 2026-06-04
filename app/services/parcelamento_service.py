from app.repositories.parcelamento_repository import ParcelamentoRepository

class ParcelamentoService:
    def __init__(self):
        self.parcelamento_repo = ParcelamentoRepository()

    def obter_por_venda(self, revendedor_id, venda_id):
        return self.parcelamento_repo.get_por_venda(revendedor_id, venda_id)

    def listar_por_status(self, revendedor_id, status):
        if status not in ['Aberta', 'Paga', 'Atrasada']:
            raise ValueError("Status de parcela invalido.")
        return self.parcelamento_repo.get_por_status(revendedor_id, status)

    def atualizar_status_parcela(self, id_parcela, revendedor_id, novo_status):
        if novo_status not in ['Aberta', 'Paga', 'Atrasada']:
            raise ValueError("Status de parcela invalido.")
            
        parcela = self.parcelamento_repo.get_by_id_and_revendedor(id_parcela, revendedor_id)
        if not parcela:
            raise ValueError("Parcela nao encontrada.")
            
        parcela.situacao_parcela = novo_status
        self.parcelamento_repo.commit()
        return parcela