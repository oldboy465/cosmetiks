from app.repositories.auditoria_repository import AuditoriaRepository
from app.models.auditoria import Auditoria

class AuditoriaService:
    def __init__(self):
        self.auditoria_repo = AuditoriaRepository()

    def registrar_acao(self, revendedor_id, usuario, ip, acao, detalhes):
        log = Auditoria(
            revendedor_id=revendedor_id,
            usuario=usuario,
            ip=ip,
            acao=acao,
            detalhes=detalhes
        )
        self.auditoria_repo.add(log)
        self.auditoria_repo.commit()
        return log

    def obter_logs(self, is_admin, revendedor_id=None):
        if is_admin:
            return self.auditoria_repo.get_historico_global()
        return self.auditoria_repo.get_por_revendedor(revendedor_id)