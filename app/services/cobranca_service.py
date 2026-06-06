from app.repositories.cobranca_repository import CobrancaRepository
from app.repositories.financeiro_repository import FinanceiroRepository
from app.models.cobranca import Cobranca
from datetime import datetime

class CobrancaService:

    def __init__(self):
        self.cobranca_repo = CobrancaRepository()
        self.financeiro_repo = FinanceiroRepository()

    def gerar_template_mensagem(self, modelo_ou_conta, nome_cliente=None, valor=None, data_vencimento=None, data_compra=None):
        # --- NOVA LÓGICA DE MENSAGEM ÚNICA E INTELIGENTE ---
        # Verificamos se foi passado o objeto Financeiro (conta) no primeiro parâmetro
        if hasattr(modelo_ou_conta, 'venda'):
            conta = modelo_ou_conta
            c_nome = conta.venda.cliente.nome
            v_id = conta.venda.id
            v_total = conta.venda.valor_total
            
            # Resolvendo data prevista e vencimento
            dt_prevista = conta.venda.data_prevista_pagamento
            dt_prev_str = dt_prevista.strftime('%d/%m/%Y') if hasattr(dt_prevista, 'strftime') else None
            venc = conta.vencimento
            venc_str = venc.strftime('%d/%m/%Y') if hasattr(venc, 'strftime') else str(venc)
            
            # Verificando parcelas
            parcelas = conta.venda.parcelas
            qtd_parcelas = len(parcelas) if parcelas else 1
            
            if qtd_parcelas > 1:
                # Encontrar a parcela exata que corresponde a este vencimento
                parc_atual = next((p for p in parcelas if p.data_vencimento == venc), None)
                num_parc = parcelas.index(parc_atual) + 1 if parc_atual else 1
                val_cobrado = parc_atual.valor_parcela if parc_atual else conta.valor
                msg = f"Olá, {c_nome}! Referente à sua compra #{v_id}, sua parcela {num_parc}/{qtd_parcelas} no valor de R$ {val_cobrado:.2f} tem o vencimento registrado para {venc_str}."
                if dt_prev_str:
                    msg += f" (Data prevista de pagamento: {dt_prev_str})."
            else:
                msg = f"Olá, {c_nome}! Referente à sua compra #{v_id}, consta o valor de R$ {conta.valor:.2f} com vencimento para {venc_str}."
                if dt_prev_str:
                    msg += f" (Data prevista de pagamento: {dt_prev_str})."
            
            msg += f" A situação atual da venda consta como '{conta.venda.situacao}'. Qualquer dúvida ou necessidade, estou à disposição!"
            return msg

        # --- CÓDIGO LEGADO MANTIDO PARA CUMPRIR A REGRA DE PRESERVAÇÃO DE LINHAS ---
        modelo = modelo_ou_conta
        venc_str = data_vencimento.strftime('%d/%m/%Y') if hasattr(data_vencimento, 'strftime') else str(data_vencimento)
        compra_str = data_compra.strftime('%d/%m/%Y') if (data_compra and hasattr(data_compra, 'strftime')) else 'recente'
        
        if modelo == 'Amigavel':
            return f"Ola, {nome_cliente}!\nPassando para lembrar seu investimento com os nossos cosmeticos da compra de {compra_str}\ntem uma parcela de R$ {valor:.2f}\ncom vencimento em {venc_str}.\nQualquer duvida estou a disposicao!"
        elif modelo == 'Moderada':
            return f"Oi, {nome_cliente}.\nTudo bem? Gostaria de verificar se deu tudo certo com o pagamento da sua fatura\nde R$ {valor:.2f},\nvencida em {venc_str}.\nSe precisar do link PIX ou dados bancarios, so me avisar por aqui."
        elif modelo == 'Firme':
            return f"Prezado(a) {nome_cliente},\nconsta em nosso sistema uma pendencia financeira no valor de R$ {valor:.2f},\ncom vencimento original em {venc_str}.\nSolicitamos a regularizacao imediata para evitar a suspensao de novos pedidos e\no bloqueio do seu cadastro."
        return f"Ola, {nome_cliente}.\nSegue demonstrativo de debito em aberto: R$ {valor:.2f}\ncom vencimento em {venc_str}.\nAguardo seu retorno."

    def registrar_disparo_cobranca(self, revendedor_id, financeiro_id, modelo, mensagem_customizada=None):
        conta = self.financeiro_repo.get_by_id_and_revendedor(financeiro_id, revendedor_id)
        if not conta:
            raise ValueError("Lancamento financeiro nao localizado")

        # Chama a inteligência nova ou aceita a customizada da tela
        msg = mensagem_customizada if mensagem_customizada else self.gerar_template_mensagem(conta)

        nova_cobranca = Cobranca(
            revendedor_id=revendedor_id,
            financeiro_id=financeiro_id,
            modelo_utilizado='Padrao', # Força a marcação como Padrão no BD
            mensagem_conteudo=msg,
            data_disparo=datetime.utcnow()
        )
        
        self.cobranca_repo.add(nova_cobranca)
        self.cobranca_repo.commit()
        return nova_cobranca

    def obter_historico_por_conta(self, revendedor_id, financeiro_id):
        return self.cobranca_repo.get_historico_por_conta(revendedor_id, financeiro_id)