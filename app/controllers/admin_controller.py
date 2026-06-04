from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services.revendedor_service import RevendedorService
from app.services.auditoria_service import AuditoriaService
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
revendedor_service = RevendedorService()
auditoria_service = AuditoriaService()

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            flash('Acesso restrito ao perfil Administrador do ecossistema.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/revendedores')
@admin_required
def listar_revendedores():
    lista = revendedor_service.listar_todos()
    return render_template('revendedores/index.html', revendedores=lista)

@admin_bp.route('/revendedores/novo', methods=['GET', 'POST'])
@admin_required
def novo_revendedor():
    if request.method == 'POST':
        try:
            revendedor_service.cadastrar_revendedor(request.form)
            flash('Entidade de negocio Revendedor cadastrada com sucesso.', 'success')
            return redirect(url_for('admin.listar_revendedores'))
        except ValueError as e:
            flash(str(e), 'danger')
    return render_template('revendedores/form.html', revendedor=None)

@admin_bp.route('/revendedores/status/<int:id_revendedor>', methods=['POST'])
@admin_required
def alterar_status(id_revendedor):
    nova_situacao = request.form.get('situacao')
    try:
        revendedor_service.alterar_situacao(id_revendedor, nova_situacao)
        flash('Situacao operacional do revendedor alterada com sucesso.', 'success')
    except ValueError as e:
        flash(str(e), 'danger')
    return redirect(url_for('admin.listar_revendedores'))

@admin_bp.route('/auditoria')
@admin_required
def trilha_auditoria():
    logs = auditoria_service.obter_logs(is_admin=True)
    return render_template('admin/auditoria.html', logs=logs)