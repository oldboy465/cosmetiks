from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services.cliente_service import ClienteService
from functools import wraps

cliente_bp = Blueprint('cliente', __name__, url_prefix='/clientes')
cliente_service = ClienteService()

def revendedor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('usuario_logado') or session.get('is_admin'):
            flash('Acesso restrito a revendedores autenticados.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@cliente_bp.route('/')
@revendedor_required
def index():
    revendedor_id = session.get('revendedor_id')
    lista = cliente_service.listar_todos(revendedor_id)
    
    clientes_com_indicadores = []
    for clie in lista:
        ind = cliente_service.obter_indicadores_cliente(clie.id, revendedor_id)
        clientes_com_indicadores.append({
            'dados': clie,
            'indicadores': ind
        })
        
    return render_template('clientes/index.html', clientes=clientes_com_indicadores)

@cliente_bp.route('/novo', methods=['GET', 'POST'])
@revendedor_required
def novo():
    if request.method == 'POST':
        revendedor_id = session.get('revendedor_id')
        nome = request.form.get('nome')
        telefone = request.form.get('telefone')
        whatsapp = request.form.get('whatsapp')
        email = request.form.get('email')
        endereco = request.form.get('endereco')
        observacoes = request.form.get('observacoes')
        try:
            cliente_service.criar_cliente(revendedor_id, nome, telefone, whatsapp, email, endereco, observacoes)
            flash('Cliente cadastrado com sucesso.', 'success')
            return redirect(url_for('cliente.index'))
        except ValueError as e:
            flash(str(e), 'danger')
            
    return render_template('clientes/form.html', cliente=None)

@cliente_bp.route('/editar/<int:id_cliente>', methods=['GET', 'POST'])
@revendedor_required
def editar(id_cliente):
    revendedor_id = session.get('revendedor_id')
    if request.method == 'POST':
        nome = request.form.get('nome')
        telefone = request.form.get('telefone')
        whatsapp = request.form.get('whatsapp')
        email = request.form.get('email')
        endereco = request.form.get('endereco')
        observacoes = request.form.get('observacoes')
        try:
            cliente_service.atualizar_cliente(id_cliente, revendedor_id, nome, telefone, whatsapp, email, endereco, observacoes)
            flash('Cliente atualizado com sucesso.', 'success')
            return redirect(url_for('cliente.index'))
        except ValueError as e:
            flash(str(e), 'danger')

    clie = cliente_service.cliente_repo.get_by_id_and_revendedor(id_cliente, revendedor_id)
    return render_template('clientes/form.html', cliente=clie)

@cliente_bp.route('/excluir/<int:id_cliente>', methods=['POST'])
@revendedor_required
def excluir(id_cliente):
    revendedor_id = session.get('revendedor_id')
    try:
        cliente_service.excluir_cliente(id_cliente, revendedor_id)
        flash('Cliente removido com sucesso.', 'success')
    except ValueError as e:
        flash(str(e), 'danger')
    return redirect(url_for('cliente.index'))