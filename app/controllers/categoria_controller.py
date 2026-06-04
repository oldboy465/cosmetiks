from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services.categoria_service import CategoriaService
from functools import wraps

categoria_bp = Blueprint('categoria', __name__, url_prefix='/categorias')
categoria_service = CategoriaService()

def revendedor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('usuario_logado') or session.get('is_admin'):
            flash('Acesso restrito a revendedores autenticados.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@categoria_bp.route('/')
@revendedor_required
def index():
    revendedor_id = session.get('revendedor_id')
    lista = categoria_service.listar_todas(revendedor_id)
    return render_template('produtos/categorias.html', categorias=lista)

@categoria_bp.route('/nova', methods=['POST'])
@revendedor_required
def nova():
    revendedor_id = session.get('revendedor_id')
    nome = request.form.get('nome')
    descricao = request.form.get('descricao')
    try:
        categoria_service.criar_categoria(revendedor_id, nome, descricao)
        flash('Categoria cadastrada com sucesso.', 'success')
    except ValueError as e:
        flash(str(e), 'danger')
    return redirect(url_for('categoria.index'))

@categoria_bp.route('/editar/<int:id_categoria>', methods=['POST'])
@revendedor_required
def editar(id_categoria):
    revendedor_id = session.get('revendedor_id')
    nome = request.form.get('nome')
    descricao = request.form.get('descricao')
    try:
        categoria_service.atualizar_categoria(id_categoria, revendedor_id, nome, descricao)
        flash('Categoria atualizada com sucesso.', 'success')
    except ValueError as e:
        flash(str(e), 'danger')
    return redirect(url_for('categoria.index'))

@categoria_bp.route('/excluir/<int:id_categoria>', methods=['POST'])
@revendedor_required
def excluir(id_categoria):
    revendedor_id = session.get('revendedor_id')
    try:
        categoria_service.excluir_categoria(id_categoria, revendedor_id)
        flash('Categoria excluida com sucesso.', 'success')
    except ValueError as e:
        flash(str(e), 'danger')
    return redirect(url_for('categoria.index'))