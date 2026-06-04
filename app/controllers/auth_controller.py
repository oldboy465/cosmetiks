from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()

@auth_bp.route('/', methods=['GET', 'POST'])
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if auth_service.esta_logado():
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')
        ip_usuario = request.remote_addr or '127.0.0.1'

        if auth_service.autenticar(usuario, senha, ip_usuario):
            return redirect(url_for('dashboard.index'))
        else:
            flash('Credenciais invalidas ou usuario inativo/bloqueado no sistema.', 'danger')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    from flask import session
    usuario = session.get('usuario_logado')
    revendedor_id = session.get('revendedor_id')
    ip_usuario = request.remote_addr or '127.0.0.1'

    auth_service.logout(usuario, revendedor_id, ip_usuario)
    return redirect(url_for('auth.login'))