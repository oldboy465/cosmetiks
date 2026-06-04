from app.models.marca import Marca
from app.repositories.base_repository import BaseRepository

class MarcaRepository(BaseRepository):
    def __init__(self):
        super().__init__(Marca)

    def buscar_por_nome(self, revendedor_id, nome_termo):
        return self.model.query.filter(
            self.model.revendedor_id == revendedor_id,
            self.model.nome.ilike(f'%{nome_termo}%')
        ).order_by(self.model.nome.asc()).all()

    def verificar_duplicada(self, revendedor_id, nome):
        return self.model.query.filter_by(revendedor_id=revendedor_id, nome=nome).first()

    def get_todas_ordenadas(self, revendedor_id):
        return self.model.query.filter_by(revendedor_id=revendedor_id).order_by(self.model.nome.asc()).all()