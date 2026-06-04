from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services.estoque_service import EstoqueService
from app.services.produto_service import ProdutoService
from functools import wraps
from datetime import datetime, time

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
    
    # Parâmetros de Paginação e Filtros Dinâmicos
    page = request.args.get('page', 1, type=int)
    produto_id = request.args.get('produto_id')
    tipo = request.args.get('tipo')
    motivo = request.args.get('motivo')
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    
    from app.models.estoque import Estoque
    from app.models.produto import Produto
    
    # Construção da Query filtrada isolada por Revendedor
    query = Estoque.query.filter_by(revendedor_id=revendedor_id)
    
    if produto_id:
        query = query.filter_by(produto_id=produto_id)
    if tipo:
        query = query.filter_by(tipo=tipo)
    if motivo:
        query = query.filter_by(motivo=motivo)
    if data_inicio:
        try:
            dt_ini = datetime.strptime(data_inicio, '%Y-%m-%d')
            query = query.filter(Estoque.data_movimentacao >= dt_ini)
        except ValueError:
            pass
    if data_fim:
        try:
            dt_fim = datetime.strptime(data_fim, '%Y-%m-%d')
            dt_fim_completo = datetime.combine(dt_fim.date(), time(23, 59, 59))
            query = query.filter(Estoque.data_movimentacao <= dt_fim_completo)
        except ValueError:
            pass
            
    # Execução da paginação nativa limitando estritamente a 10 linhas por página
    pagination_obj = query.order_by(Estoque.data_movimentacao.desc()).paginate(
        page=page, 
        per_page=10, 
        error_out=False
    )
    
    # Lista de produtos para popular o dropdown de filtros do template
    lista_produtos = Produto.query.filter_by(revendedor_id=revendedor_id).order_by(Produto.nome.asc()).all()
    
    return render_template(
        'produtos/historico_estoque.html', 
        movimentacoes=pagination_obj.items,
        pagination=pagination_obj,
        produtos=lista_produtos
    )

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