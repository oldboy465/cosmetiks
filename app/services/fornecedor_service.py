from app.repositories.fornecedor_repository import FornecedorRepository
from app.models.fornecedor import Fornecedor

class FornecedorService:
    def __init__(self):
        self.fornecedor_repo = FornecedorRepository()

    def listar_todos(self, revendedor_id):
        return self.fornecedor_repo.get_todos_ordenados(revendedor_id)

    def criar_fornecedor(self, revendedor_id, nome, telefone, whatsapp, email, observacoes):
        if not nome or str(nome).strip() == "":
            raise ValueError("O nome do fornecedor e obrigatorio.")
        
        existente = self.fornecedor_repo.verificar_duplicado(revendedor_id, nome)
        if existente:
            raise ValueError("Ja existe um fornecedor cadastrado com este nome.")

        novo_fornecedor = Fornecedor(
            revendedor_id=revendedor_id,
            nome=nome.strip(),
            telefone=telefone.strip() if telefone else None,
            whatsapp=whatsapp.strip() if whatsapp else None,
            email=email.strip() if email else None,
            observacoes=observacoes.strip() if observacoes else None
        )
        self.fornecedor_repo.add(novo_fornecedor)
        self.fornecedor_repo.commit()
        return novo_fornecedor

    def atualizar_fornecedor(self, id_fornecedor, revendedor_id, nome, telefone, whatsapp, email, observacoes):
        fornecedor = self.fornecedor_repo.get_by_id_and_revendedor(id_fornecedor, revendedor_id)
        if not fornecedor:
            raise ValueError("Fornecedor nao encontrado.")
        
        if not nome or str(nome).strip() == "":
            raise ValueError("O nome do fornecedor e obrigatorio.")

        existente = self.fornecedor_repo.verificar_duplicado(revendedor_id, nome)
        if existente and existente.id != id_fornecedor:
            raise ValueError("Ja existe outro fornecedor com este nome.")

        fornecedor.nome = nome.strip()
        fornecedor.telefone = telefone.strip() if telefone else None
        fornecedor.whatsapp = whatsapp.strip() if whatsapp else None
        fornecedor.email = email.strip() if email else None
        fornecedor.observacoes = observacoes.strip() if observacoes else None
        
        self.fornecedor_repo.commit()
        return fornecedor

    def excluir_fornecedor(self, id_fornecedor, revendedor_id):
        fornecedor = self.fornecedor_repo.get_by_id_and_revendedor(id_fornecedor, revendedor_id)
        if not fornecedor:
            raise ValueError("Fornecedor nao encontrado.")
        
        if fornecedor.produtos:
            raise ValueError("Nao e possivel excluir um fornecedor associado a produtos.")

        self.fornecedor_repo.delete(fornecedor)
        self.fornecedor_repo.commit()
        return True