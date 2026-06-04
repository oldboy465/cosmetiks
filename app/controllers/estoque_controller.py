from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services.estoque_service import EstoqueService
from app.services.produto_service import ProdutoService
from functools import wraps

estoque_bp = Blueprint('estoque', __name__, url_prefix='/estoque')
estoque_service = EstoqueService()
produto_service = ProdutoService()

def revendedor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('usuario_logado') or session.get('is_admin'):
            flash('Acesso restrito a revendedores autenticados.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@estoque_bp.route('/historico')
@revendedor_required
def historico():
    revendedor_id = session.get('revendedor_id')
    movimentacoes = estoque_service.obter_historico_completo(revendedor_id)
    return render_template('produtos/historico_estoque.html', movimentacoes=movimentacoes)

@estoque_bp.route('/movimentar', methods=['GET', 'POST'])
@revendedor_required
def movimentar():
    revendedor_id = session.get('revendedor_id')
    if request.method == 'POST':
        produto_id = request.form.get('produto_id')
        tipo = request.form.get('tipo')
        motivo = request.form.get('motivo')
        quantidade = request.form.get('quantidade')
        observacoes = request.form.get('observacoes')
        
        try:
            estoque_service.registrar_movimentacao(revendedor_id, produto_id, tipo, motivo, quantidade, observacoes)
            flash('Movimentacao manual de estoque processada com sucesso.', 'success')
            return redirect(url_for('estoque.historico'))
        except ValueError as e:
            flash(str(e), 'danger')

    produtos = produto_service.listar_todos(revendedor_id)
    return render_template('produtos/movimentar_estoque.html', produtos=produtos)

@estoque_bp.route('/critico')
@revendedor_required
def estoque_critico():
    revendedor_id = session.get('revendedor_id')
    produtos_baixos = produto_service.verificar_produtos_estoque_baixo(revendedor_id)
    return render_template('produtos/estoque_baixo.html', produtos=produtos_baixos)