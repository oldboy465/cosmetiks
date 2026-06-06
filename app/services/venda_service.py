from app.repositories.venda_repository import VendaRepository
from app.repositories.produto_repository import ProdutoRepository
from app.repositories.estoque_repository import EstoqueRepository
from app.services.estoque_service import EstoqueService
from app.models.venda import Venda, ItemVenda
from app.models.financeiro import Financeiro
from app.models.parcelamento import Parcelamento
from decimal import Decimal
from datetime import datetime, timedelta

class VendaService:
    def __init__(self):
        self.venda_repo = VendaRepository()
        self.produto_repo = ProdutoRepository()
        self.estoque_repo = EstoqueRepository()
        self.estoque_service = EstoqueService()

    def criar_venda(self, revendedor_id, cliente_id, produtos_lista, desconto_valor, desconto_percentual, forma_pagamento, situacao, qtd_parcelas=1, data_venda_escolhida=None, observacoes=None, data_prevista_pagamento=None):
        if not produtos_lista or len(produtos_lista) == 0:
            raise ValueError("Uma venda deve conter pelo menos um produto.")

        # Conversão estruturada da data escolhida pelo usuário nativo do front-end
        if data_venda_escolhida:
            try:
                data_final_venda = datetime.strptime(data_venda_escolhida, '%Y-%m-%d')
            except ValueError:
                data_final_venda = datetime.utcnow()
        else:
            data_final_venda = datetime.utcnow()

        # Injeção da Data Prevista de Pagamento para os cálculos de longo prazo
        data_prev_pagto = None
        if data_prevista_pagamento:
            try:
                data_prev_pagto = datetime.strptime(data_prevista_pagamento, '%Y-%m-%d').date()
            except ValueError:
                pass

        valor_bruto = Decimal('0.00')
        itens_para_salvar = []

        for p in produtos_lista:
            produto = self.produto_repo.get_by_id_and_revendedor(p['produto_id'], revendedor_id)
            if not produto:
                raise ValueError("Produto nao encontrado.")
            
            qtd = int(p['quantidade'])
            if produto.quantidade_estoque < qtd:
                raise ValueError(f"Estoque insuficiente para o produto {produto.nome}. Estoque atual: {produto.quantidade_estoque}")
            
            total_item = Decimal(str(produto.preco_venda)) * qtd
            valor_bruto += total_item
            
            itens_para_salvar.append({
                'produto_id': produto.id,
                'quantidade': qtd,
                'valor_unitario': produto.preco_venda,
                'valor_total': total_item
            })

        desc_v = Decimal(str(desconto_valor)) if desconto_valor else Decimal('0.00')
        desc_p = Decimal(str(desconto_percentual)) if desconto_percentual else Decimal('0.00')
        
        if desc_p > 0:
            valor_liquido = valor_bruto - (valor_bruto * (desc_p / Decimal('100.00')))
        else:
            valor_liquido = valor_bruto - desc_v

        if valor_liquido < 0:
            valor_liquido = Decimal('0.00')

        nova_venda = Venda(
            revendedor_id=revendedor_id,
            cliente_id=cliente_id,
            data_venda=data_final_venda,
            valor_total=valor_liquido,
            desconto_valor=desc_v,
            desconto_percentual=desc_p,
            situacao=situacao,
            forma_pagamento=forma_pagamento,
            observacoes=observacoes,
            data_prevista_pagamento=data_prev_pagto
        )
        self.venda_repo.add(nova_venda)
        self.venda_repo.commit()

        for item in itens_para_salvar:
            iv = ItemVenda(
                venda_id=nova_venda.id,
                produto_id=item['produto_id'],
                quantidade=item['quantidade'],
                valor_unitario=item['valor_unitario'],
                valor_total=item['valor_total']
            )
            self.venda_repo.add_item(iv)
            
            self.estoque_service.registrar_movimentacao(
                revendedor_id=revendedor_id,
                produto_id=item['produto_id'],
                tipo='Saida',
                motivo='Venda',
                quantidade=item['quantidade'],
                venda_id=nova_venda.id,
                observacoes=f"Venda id {nova_venda.id}",
                data_movimentacao=data_final_venda
            )

        if qtd_parcelas and int(qtd_parcelas) > 0:
            parcelas_n = int(qtd_parcelas)
            valor_parc = valor_liquido / Decimal(str(parcelas_n))
            
            for i in range(1, parcelas_n + 1):
                # Se há uma data prevista específica, ela serve como âncora para as parcelas
                if data_prev_pagto:
                    venc = data_prev_pagto + timedelta(days=30 * (i - 1))
                else:
                    venc = (data_final_venda + timedelta(days=30 * i)).date()
                    
                p_status = 'Paga' if situacao == 'Pago' else 'Aberta'
                
                parc = Parcelamento(
                    revendedor_id=revendedor_id,
                    venda_id=nova_venda.id,
                    quantidade_parcelas=parcelas_n,
                    valor_parcela=valor_parc,
                    data_vencimento=venc,
                    situacao_parcela=p_status
                )
                from app import db
                db.session.add(parc)

        fin_status = 'Pago' if situacao == 'Pago' else ('Parcialmente pago' if situacao == 'Parcialmente pago' else 'Em aberto')
        pag_data = data_final_venda if situacao == 'Pago' else None
        
        # Define o vencimento final do contas a receber baseado na prioridade da data prevista
        venc_fin = data_prev_pagto if data_prev_pagto else (data_final_venda + timedelta(days=30)).date()
        
        conta = Financeiro(
            revendedor_id=revendedor_id,
            cliente_id=cliente_id,
            venda_id=nova_venda.id,
            valor=valor_liquido,
            vencimento=venc_fin,
            pagamento=pag_data,
            status=fin_status
        )
        from app import db
        db.session.add(conta)
        db.session.commit()

        return nova_venda

    def excluir_venda(self, id_venda, revendedor_id):
        venda = self.venda_repo.get_by_id_and_revendedor(id_venda, revendedor_id)
        if not venda:
            raise ValueError("Venda nao encontrada.")

        for item in venda.itens:
            self.estoque_service.registrar_movimentacao(
                revendedor_id=revendedor_id,
                produto_id=item.produto_id,
                tipo='Entrada',
                motivo='Devolucao',
                quantidade=item.quantidade,
                observacoes=f"Estorno automatico por exclusao de venda id {venda.id}"
            )

        self.estoque_repo.delete_por_venda(revendedor_id, venda.id)
        self.venda_repo.delete(venda)
        self.venda_repo.commit()
        return True

    def editar_venda(self, id_venda, revendedor_id, cliente_id, produtos_lista, desconto_valor, desconto_percentual, forma_pagamento, situacao, qtd_parcelas=1, data_venda_escolhida=None, observacoes=None, data_prevista_pagamento=None):
        self.excluir_venda(id_venda, revendedor_id)
        return self.criar_venda(revendedor_id, cliente_id, produtos_lista, desconto_valor, desconto_percentual, forma_pagamento, situacao, qtd_parcelas, data_venda_escolhida, observacoes, data_prevista_pagamento)