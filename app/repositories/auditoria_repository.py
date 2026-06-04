from app.models.auditoria import Auditoria
from app.repositories.base_repository import BaseRepository

class AuditoriaRepository(BaseRepository):
    def __init__(self):
        super().__init__(Auditoria)

    def get_por_revendedor(self, revendedor_id):
        return self.model.query.filter_by(revendedor_id=revendedor_id).order_by(self.model.data_hora.desc()).all()

    def get_historico_global(self):
        return self.model.query.order_by(self.model.data_hora.desc()).all()

    def filtrar_auditoria(self, revendedor_id=None, usuario=None, acao=None):
        query = self.model.query
        if revendedor_id:
            query = query.filter_by(revendedor_id=revendedor_id)
        if usuario:
            query = query.filter_by(usuario=usuario)
        if acao:
            query = query.filter_by(acao=acao)
        return query.order_by(self.model.data_hora.desc()).all()