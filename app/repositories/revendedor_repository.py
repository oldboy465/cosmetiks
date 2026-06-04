from app.models.revendedor import Revendedor
from app.repositories.base_repository import BaseRepository

class RevendedorRepository(BaseRepository):
    def __init__(self):
        super().__init__(Revendedor)

    def get_by_usuario(self, usuario):
        return self.model.query.filter_by(usuario=usuario).first()

    def get_by_cpf(self, cpf):
        return self.model.query.filter_by(cpf=cpf).first()

    def get_by_email(self, email):
        return self.model.query.filter_by(email=email).first()

    def get_todos_ordenados(self):
        return self.model.query.order_by(self.model.nome_completo.asc()).all()