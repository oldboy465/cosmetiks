from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services.financeiro_service import FinanceiroService
from functools import wraps

financeiro_bp = Blueprint('financeiro', __name__, url_prefix='/financeiro')
financeiro_service = FinanceiroService()

def revendedor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('usuario_logado') or session.get('is_admin'):
            flash('Acesso restrito a revendedores autenticados.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@financeiro_bp.route('/contas')
@revendedor_required
def contas_receber():
    revendedor_id = session.get('revendedor_id')
    filtro = request.args.get('filtro', 'aberto')
    
    if filtro == 'vencidas':
        contas = financeiro_service.obter_contas_vencidas(revendedor_id)
    elif filtro == 'pagas':
        contas = financeiro_service.obter_contas_pagas(revendedor_id)
    else:
        contas = financeiro_service.obter_contas_em_aberto(revendedor_id)
        
    return render_template('financeiro/index.html', contas=contas, filtro_atual=filtro)

@financeiro_bp.route('/contas/baixa/<int:id_financeiro>', methods=['POST'])
@revendedor_required
def receber_pagamento(id_financeiro):
    revendedor_id = session.get('revendedor_id')
    valor_pago = request.form.get('valor_pago')
    try:
        financeiro_service.registrar_pagamento(id_financeiro, revendedor_id, valor_pago)
        flash('Fluxo de caixa atualizado com a entrada do pagamento.', 'success')
    except ValueError as e:
        flash(str(e), 'danger')
    return redirect(url_for('financeiro.contas_receber'))