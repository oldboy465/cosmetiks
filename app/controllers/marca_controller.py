from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services.marca_service import MarcaService
from functools import wraps

marca_bp = Blueprint('marca', __name__, url_prefix='/marcas')
marca_service = MarcaService()

def revendedor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('usuario_logado') or session.get('is_admin'):
            flash('Acesso restrito a revendedores autenticados.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@marca_bp.route('/')
@revendedor_required
def index():
    revendedor_id = session.get('revendedor_id')
    lista = marca_service.listar_todas(revendedor_id)
    return render_template('produtos/marcas.html', marcas=lista)

@marca_bp.route('/nova', methods=['POST'])
@revendedor_required
def nova():
    revendedor_id = session.get('revendedor_id')
    nome = request.form.get('nome')
    descricao = request.form.get('descricao')
    try:
        marca_service.criar_marca(revendedor_id, nome, descricao)
        flash('Marca cadastrada com sucesso.', 'success')
    except ValueError as e:
        flash(str(e), 'danger')
    return redirect(url_for('marca.index'))

@marca_bp.route('/editar/<int:id_marca>', methods=['POST'])
@revendedor_required
def editar(id_marca):
    revendedor_id = session.get('revendedor_id')
    nome = request.form.get('nome')
    descricao = request.form.get('descricao')
    try:
        marca_service.atualizar_marca(id_marca, revendedor_id, nome, descricao)
        flash('Marca atualizada com sucesso.', 'success')
    except ValueError as e:
        flash(str(e), 'danger')
    return redirect(url_for('marca.index'))

@marca_bp.route('/excluir/<int:id_marca>', methods=['POST'])
@revendedor_required
def excluir(id_marca):
    revendedor_id = session.get('revendedor_id')
    try:
        marca_service.excluir_marca(id_marca, revendedor_id)
        flash('Marca excluida com sucesso.', 'success')
    except ValueError as e:
        flash(str(e), 'danger')
    return redirect(url_for('marca.index'))