from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
from app.repositories.revendedor_repository import RevendedorRepository
from app.repositories.auditoria_repository import AuditoriaRepository
from datetime import datetime

class AuthService:
    def __init__(self):
        self.revendedor_repo = RevendedorRepository()
        self.auditoria_repo = AuditoriaRepository()

    def autenticar(self, usuario, senha, ip_usuario):
        if usuario == "admin" and senha == "AdminCosmetiKS2026!":
            session['usuario_logado'] = 'admin'
            session['is_admin'] = True
            session['revendedor_id'] = None
            return True

        revendedor = self.revendedor_repo.get_by_usuario(usuario)
        if revendedor and check_password_hash(revendedor.senha_criptografada, senha):
            if revendedor.situacao != 'Ativo':
                return False
            
            session['usuario_logado'] = revendedor.usuario
            session['is_admin'] = False
            session['revendedor_id'] = revendedor.id
            
            revendedor.ultimo_acesso = datetime.utcnow()
            self.revendedor_repo.commit()
            
            from app.models.auditoria import Auditoria
            log = Auditoria(
                revendedor_id=revendedor.id,
                usuario=revendedor.usuario,
                ip=ip_usuario,
                acao='Login',
                detalhes='Autenticacao efetuada com sucesso.'
            )
            self.auditoria_repo.add(log)
            self.auditoria_repo.commit()
            return True
        return False

    def logout(self, usuario, revendedor_id, ip_usuario):
        if usuario:
            from app.models.auditoria import Auditoria
            log = Auditoria(
                revendedor_id=revendedor_id,
                usuario=usuario,
                ip=ip_usuario,
                acao='Logout',
                detalhes='Sessao encerrada voluntariamente.'
            )
            self.auditoria_repo.add(log)
            self.auditoria_repo.commit()
        session.clear()

    def esta_logado(self):
        return 'usuario_logado' in session