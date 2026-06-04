from app.repositories.cobranca_repository import CobrancaRepository
from app.repositories.financeiro_repository import FinanceiroRepository
from app.models.cobranca import Cobranca
from datetime import datetime

class CobrancaService:
    def __init__(self):
        self.cobranca_repo = CobrancaRepository()
        self.financeiro_repo = FinanceiroRepository()

    def gerar_template_mensagem(self, modelo, nome_cliente, valor, data_vencimento, data_compra=None):
        venc_str = data_vencimento.strftime('%d/%m/%Y') if hasattr(data_vencimento, 'strftime') else str(data_vencimento)
        compra_str = data_compra.strftime('%d/%m/%Y') if (data_compra and hasattr(data_compra, 'strftime')) else 'recente'
        
        if modelo == 'Amigavel':
            return f"Ola, {nome_cliente}! Passando para lembrar seu investimento com os nossos cosmeticos da compra de {compra_str} tem uma parcela de R$ {valor:.2f} com vencimento em {venc_str}. Qualquer duvida estou a disposicao!"
        elif modelo == 'Moderada':
            return f"Oi, {nome_cliente}. Tudo bem? Gostaria de verificar se deu tudo certo com o pagamento da sua fatura de R$ {valor:.2f}, vencida em {venc_str}. Se precisar do link PIX ou dados bancarios, so me avisar por aqui."
        elif modelo == 'Firme':
            return f"Prezado(a) {nome_cliente}, consta em nosso sistema uma pendencia financeira no valor de R$ {valor:.2f}, com vencimento original em {venc_str}. Solicitamos a regularizacao imediata para evitar a suspensao de novos pedidos e o bloqueio do seu cadastro."
        return f"Ola, {nome_cliente}. Segue demonstrativo de debito em aberto: R$ {valor:.2f} com vencimento em {venc_str}. Aguardo seu retorno."

    def registrar_disparo_cobranca(self, revendedor_id, financeiro_id, modelo, mensagem_customizada=None):
        conta = self.financeiro_repo.get_by_id_and_revendedor(financeiro_id, revendedor_id)
        if not conta:
            raise ValueError("Lancamento financeiro nao localizado.")

        msg = mensagem_customizada if mensagem_customizada else self.gerar_template_mensagem(
            modelo, conta.venda.cliente.nome, conta.valor, conta.vencimento, conta.venda.data_venda
        )

        nova_cobranca = Cobranca(
            revendedor_id=revendedor_id,
            financeiro_id=financeiro_id,
            modelo_utilizado=modelo,
            mensagem_conteudo=msg,
            data_disparo=datetime.utcnow()
        )
        
        self.cobranca_repo.add(nova_cobranca)
        self.cobranca_repo.commit()
        return nova_cobranca

    def obter_historico_por_conta(self, revendedor_id, financeiro_id):
        return self.cobranca_repo.get_historico_por_conta(revendedor_id, financeiro_id)