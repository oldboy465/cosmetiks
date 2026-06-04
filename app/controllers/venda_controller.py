from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.services.venda_service import VendaService
from app.services.cliente_service import ClienteService
from app.services.produto_service import ProdutoService
from functools import wraps
import json

venda_bp = Blueprint('venda', __name__, url_prefix='/vendas')
venda_service = VendaService()
cliente_service = ClienteService()
produto_service = ProdutoService()

def revendedor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('usuario_logado') or session.get('is_admin'):
            flash('Acesso restrito a revendedores autenticados.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@venda_bp.route('/')
@revendedor_required
def index():
    revendedor_id = session.get('revendedor_id')
    lista = venda_service.venda_repo.get_todas_ordenadas(revendedor_id)
    return render_template('vendas/index.html', vendas=lista)

@venda_bp.route('/nova', methods=['GET', 'POST'])
@revendedor_required
def nova():
    revendedor_id = session.get('revendedor_id')
    if request.method == 'POST':
        cliente_id = request.form.get('cliente_id')
        forma_pagamento = request.form.get('forma_pagamento')
        situacao = request.form.get('situacao')
        desconto_valor = request.form.get('desconto_valor') or 0
        desconto_percentual = request.form.get('desconto_percentual') or 0
        qtd_parcelas = request.form.get('quantidade_parcelas') or 1
        
        produtos_json = request.form.get('produtos_json')
        try:
            # Correção operacional da verificação do JSON de itens
            produtos_lista = json.loads(produtos_json) if produtos_json else []
            venda_service.criar_venda(
                revendedor_id=revendedor_id,
                cliente_id=cliente_id,
                produtos_lista=produtos_lista,
                desconto_valor=desconto_valor,
                desconto_percentual=desconto_percentual,
                forma_pagamento=forma_pagamento,
                situacao=situacao,
                qtd_parcelas=qtd_parcelas
            )
            flash('Operação de venda processada e estoque movimentado.', 'success')
            return redirect(url_for('venda.index'))
        except ValueError as e:
            flash(str(e), 'danger')

    clientes = cliente_service.listar_todos(revendedor_id)
    produtos = produto_service.listar_todos(revendedor_id)
    return render_template('vendas/form.html', venda=None, clientes=clientes, produtos=produtos)

@venda_bp.route('/detalhes/<int:id_venda>')
@revendedor_required
def detalhes(id_venda):
    revendedor_id = session.get('revendedor_id')
    venda = venda_service.venda_repo.get_by_id_and_revendedor(id_venda, revendedor_id)
    if not venda:
        flash('Registro de venda nao localizado.', 'danger')
        return redirect(url_for('venda.index'))
    return render_template('vendas/detalhes.html', venda=venda)

@venda_bp.route('/excluir/<int:id_venda>', methods=['POST'])
@revendedor_required
def excluir(id_venda):
    revendedor_id = session.get('revendedor_id')
    try:
        venda_service.excluir_venda(id_venda, revendedor_id)
        flash('Venda excluida e estoque retornado automaticamente.', 'success')
    except ValueError as e:
        flash(str(e), 'danger')
    return redirect(url_for('venda.index'))