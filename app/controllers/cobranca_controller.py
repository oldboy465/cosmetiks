from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.services.cobranca_service import CobrancaService
from app.services.financeiro_service import FinanceiroService
from functools import wraps

cobranca_bp = Blueprint('cobranca', __name__, url_prefix='/cobrancas')
cobranca_service = CobrancaService()
financeiro_service = FinanceiroService()

def revendedor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('usuario_logado') or session.get('is_admin'):
            flash('Acesso restrito a revendedores autenticados.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@cobranca_bp.route('/gerar/<int:id_financeiro>', methods=['GET'])
@revendedor_required
def visualizar_modelos(id_financeiro):
    revendedor_id = session.get('revendedor_id')
    conta = financeiro_service.financeiro_repo.get_by_id_and_revendedor(id_financeiro, revendedor_id)
    if not conta:
        flash('Registro financeiro nao encontrado.', 'danger')
        return redirect(url_for('financeiro.contas_receber'))
        
    # Removido o loop e o array de modelos. Passamos a gerar apenas a mensagem de cobrança inteligente e unificada.
    mensagem_padrao = cobranca_service.gerar_template_mensagem(conta)
    
    # Injetado dentro de um dicionário para não quebrar a tela atual antes do template ser atualizado
    mensagens = {'Padrao': mensagem_padrao}
        
    historico = cobranca_service.obter_historico_por_conta(revendedor_id, id_financeiro)
    return render_template('cobrancas/index.html', conta=conta, mensagens=mensagens, historico=historico)

@cobranca_bp.route('/registrar/<int:id_financeiro>', methods=['POST'])
@revendedor_required
def registrar_disparo(id_financeiro):
    revendedor_id = session.get('revendedor_id')
    # O modelo não é mais lido, pois a cobrança agora é unificada
    mensagem_customizada = request.form.get('mensagem')
    try:
        cobranca_service.registrar_disparo_cobranca(revendedor_id, id_financeiro, mensagem_customizada)
        return jsonify({"status": "success", "message": "Disparo registrado na auditoria de cobranca."})
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400