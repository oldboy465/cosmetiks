from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services.fornecedor_service import FornecedorService
from functools import wraps

fornecedor_bp = Blueprint('fornecedor', __name__, url_prefix='/fornecedores')
fornecedor_service = FornecedorService()

def revendedor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('usuario_logado') or session.get('is_admin'):
            flash('Acesso restrito a revendedores autenticados.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@fornecedor_bp.route('/')
@revendedor_required
def index():
    revendedor_id = session.get('revendedor_id')
    lista = fornecedor_service.listar_todos(revendedor_id)
    return render_template('produtos/fornecedores.html', fornecedores=lista)

@fornecedor_bp.route('/novo', methods=['POST'])
@revendedor_required
def novo():
    revendedor_id = session.get('revendedor_id')
    nome = request.form.get('nome')
    telefone = request.form.get('telefone')
    whatsapp = request.form.get('whatsapp')
    email = request.form.get('email')
    observacoes = request.form.get('observacoes')
    try:
        fornecedor_service.criar_fornecedor(revendedor_id, nome, telefone, whatsapp, email, observacoes)
        flash('Fornecedor cadastrado com sucesso.', 'success')
    except ValueError as e:
        flash(str(e), 'danger')
    return redirect(url_for('fornecedor.index'))

@fornecedor_bp.route('/editar/<int:id_fornecedor>', methods=['POST'])
@revendedor_required
def editar(id_fornecedor):
    revendedor_id = session.get('revendedor_id')
    nome = request.form.get('nome')
    telefone = request.form.get('telefone')
    whatsapp = request.form.get('whatsapp')
    email = request.form.get('email')
    observacoes = request.form.get('observacoes')
    try:
        fornecedor_service.atualizar_fornecedor(id_fornecedor, revendedor_id, nome, telefone, whatsapp, email, observacoes)
        flash('Fornecedor atualizado com sucesso.', 'success')
    except ValueError as e:
        flash(str(e), 'danger')
    return redirect(url_for('fornecedor.index'))

@fornecedor_bp.route('/excluir/<int:id_fornecedor>', methods=['POST'])
@revendedor_required
def excluir(id_fornecedor):
    revendedor_id = session.get('revendedor_id')
    try:
        fornecedor_service.excluir_fornecedor(id_fornecedor, revendedor_id)
        flash('Fornecedor excluido com sucesso.', 'success')
    except ValueError as e:
        flash(str(e), 'danger')
    return redirect(url_for('fornecedor.index'))