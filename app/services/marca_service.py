from app.repositories.marca_repository import MarcaRepository
from app.models.marca import Marca

class MarcaService:
    def __init__(self):
        self.marca_repo = MarcaRepository()

    def listar_todas(self, revendedor_id):
        return self.marca_repo.get_todas_ordenadas(revendedor_id)

    def criar_marca(self, revendedor_id, nome, descricao):
        if not nome or str(nome).strip() == "":
            raise ValueError("O nome da marca e obrigatorio.")
        
        existente = self.marca_repo.verificar_duplicada(revendedor_id, nome)
        if existente:
            raise ValueError("Ja existe uma marca cadastrada com este nome.")

        nova_marca = Marca(
            revendedor_id=revendedor_id,
            nome=nome.strip(),
            descricao=descricao.strip() if descricao else None
        )
        self.marca_repo.add(nova_marca)
        self.marca_repo.commit()
        return nova_marca

    def atualizar_marca(self, id_marca, revendedor_id, nome, descricao):
        marca = self.marca_repo.get_by_id_and_revendedor(id_marca, revendedor_id)
        if not marca:
            raise ValueError("Marca nao encontrada.")
        
        if not nome or str(nome).strip() == "":
            raise ValueError("O nome da marca e obrigatorio.")

        existente = self.marca_repo.verificar_duplicada(revendedor_id, nome)
        if existente and existente.id != id_marca:
            raise ValueError("Ja existe outra marca com este nome.")

        marca.nome = nome.strip()
        marca.descricao = descricao.strip() if descricao else None
        self.marca_repo.commit()
        return marca

    def excluir_marca(self, id_marca, revendedor_id):
        marca = self.marca_repo.get_by_id_and_revendedor(id_marca, revendedor_id)
        if not marca:
            raise ValueError("Marca nao encontrada.")
        
        if marca.produtos:
            raise ValueError("Nao e possivel excluir uma marca associada a produtos.")

        self.marca_repo.delete(marca)
        self.marca_repo.commit()
        return True