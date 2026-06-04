from app.repositories.cliente_repository import ClienteRepository
from app.models.cliente import Cliente
from app.models.venda import Venda
from app.models.financeiro import Financeiro
from datetime import datetime

class ClienteService:
    def __init__(self):
        self.cliente_repo = ClienteRepository()

    def listar_todos(self, revendedor_id):
        return self.cliente_repo.get_todos_ordenados(revendedor_id)

    def criar_cliente(self, revendedor_id, nome, telefone, whatsapp, email, endereco, observacoes):
        if not nome or str(nome).strip() == "":
            raise ValueError("O nome do cliente e obrigatorio.")
        
        existente = self.cliente_repo.verificar_duplicado(revendedor_id, nome)
        if existente:
            raise ValueError("Ja existe um cliente cadastrado com este nome.")

        novo_cliente = Cliente(
            revendedor_id=revendedor_id,
            nome=nome.strip(),
            telefone=telefone.strip() if telefone else None,
            whatsapp=whatsapp.strip() if whatsapp else None,
            email=email.strip() if email else None,
            endereco=endereco.strip() if endereco else None,
            observacoes=observacoes.strip() if observacoes else None,
            data_cadastro=datetime.utcnow()
        )
        self.cliente_repo.add(novo_cliente)
        self.cliente_repo.commit()
        return novo_cliente

    def atualizar_cliente(self, id_cliente, revendedor_id, nome, telefone, whatsapp, email, endereco, observacoes):
        cliente = self.cliente_repo.get_by_id_and_revendedor(id_cliente, revendedor_id)
        if not cliente:
            raise ValueError("Cliente nao encontrado.")
        
        if not nome or str(nome).strip() == "":
            raise ValueError("O nome do cliente e obrigatorio.")

        existente = self.cliente_repo.verificar_duplicado(revendedor_id, nome)
        if existente and existente.id != id_cliente:
            raise ValueError("Ja existe outro cliente com este nome.")

        cliente.nome = nome.strip()
        cliente.telefone = telefone.strip() if telefone else None
        cliente.whatsapp = whatsapp.strip() if whatsapp else None
        cliente.email = email.strip() if email else None
        cliente.endereco = endereco.strip() if endereco else None
        cliente.observacoes = observacoes.strip() if observacoes else None
        
        self.cliente_repo.commit()
        return cliente

    def excluir_cliente(self, id_cliente, revendedor_id):
        cliente = self.cliente_repo.get_by_id_and_revendedor(id_cliente, revendedor_id)
        if not cliente:
            raise ValueError("Cliente nao encontrado.")
        
        from app.models.venda import Venda
        vendas_associadas = Venda.query.filter_by(cliente_id=id_cliente, revendedor_id=revendedor_id).first()
        if vendas_associadas:
            raise ValueError("Nao e possivel excluir um cliente que possui historico de vendas.")

        self.cliente_repo.delete(cliente)
        self.cliente_repo.commit()
        return True

    def obter_indicadores_cliente(self, id_cliente, revendedor_id):
        cliente = self.cliente_repo.get_by_id_and_revendedor(id_cliente, revendedor_id)
        if not cliente:
            raise ValueError("Cliente nao encontrado.")

        vendas = Venda.query.filter_by(cliente_id=id_cliente, revendedor_id=revendedor_id).all()
        quantidade_compras = len(vendas)
        valor_total_comprado = sum([venda.valor_total for venda in vendas])
        
        ultima_venda = Venda.query.filter_by(cliente_id=id_cliente, revendedor_id=revendedor_id).order_by(Venda.data_venda.desc()).first()
        ultima_compra = ultima_venda.data_venda if ultima_venda else None

        contas_atrasadas = Financeiro.query.filter_by(cliente_id=id_cliente, revendedor_id=revendedor_id, status='Atrasado').first()
        status_financeiro = "Inadimplente" if contas_atrasadas else "Regular"

        return {
            "quantidade_compras": quantidade_compras,
            "valor_total_comprado": valor_total_comprado,
            "ultima_compra": ultima_compra,
            "status_financeiro": status_financeiro
        }