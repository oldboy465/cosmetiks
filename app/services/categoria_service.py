from app.repositories.categoria_repository import CategoriaRepository
from app.models.categoria import Categoria

class CategoriaService:
    def __init__(self):
        self.categoria_repo = CategoriaRepository()

    def listar_todas(self, revendedor_id):
        return self.categoria_repo.get_todas_ordenadas(revendedor_id)

    def criar_categoria(self, revendedor_id, nome, descricao):
        if not nome or str(nome).strip() == "":
            raise ValueError("O nome da categoria e obrigatorio.")
        
        existente = self.categoria_repo.verificar_duplicada(revendedor_id, nome)
        if existente:
            raise ValueError("Ja existe uma categoria cadastrada com este nome.")

        nova_categoria = Categoria(
            revendedor_id=revendedor_id,
            nome=nome.strip(),
            descricao=descricao.strip() if descricao else None
        )
        self.categoria_repo.add(nova_categoria)
        self.categoria_repo.commit()
        return nova_categoria

    def atualizar_categoria(self, id_categoria, revendedor_id, nome, descricao):
        categoria = self.categoria_repo.get_by_id_and_revendedor(id_categoria, revendedor_id)
        if not categoria:
            raise ValueError("Categoria nao encontrada.")
        
        if not nome or str(nome).strip() == "":
            raise ValueError("O nome da categoria e obrigatorio.")

        existente = self.categoria_repo.verificar_duplicada(revendedor_id, nome)
        if existente and existente.id != id_categoria:
            raise ValueError("Ja existe outra categoria com este nome.")

        categoria.nome = nome.strip()
        categoria.descricao = descricao.strip() if descricao else None
        self.categoria_repo.commit()
        return categoria

    def excluir_categoria(self, id_categoria, revendedor_id):
        categoria = self.categoria_repo.get_by_id_and_revendedor(id_categoria, revendedor_id)
        if not categoria:
            raise ValueError("Categoria nao encontrada.")
        
        if categoria.produtos:
            raise ValueError("Nao e possivel excluir uma categoria associada a produtos.")

        self.categoria_repo.delete(categoria)
        self.categoria_repo.commit()
        return True