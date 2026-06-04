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

@estoque_bp.route('/geral')
@revendedor_required
def geral():
    revendedor_id = session.get('revendedor_id')
    
    # Parâmetros de Paginação e Ordenação
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    order_by = request.args.get('order_by', 'nome')
    order_dir = request.args.get('order_dir', 'asc')
    
    # Dicionário de Filtros Dinâmicos
    filters = {
        'nome': request.args.get('nome', '').strip(),
        'id': request.args.get('id', type=int),
        'codigo_barras': request.args.get('codigo_barras', '').strip(),
        'marca_id': request.args.get('marca_id', type=int),
        'categoria_id': request.args.get('categoria_id', type=int),
        'fornecedor_id': request.args.get('fornecedor_id', type=int),
        'situacao': request.args.get('situacao', ''),
        'estoque_baixo': request.args.get('estoque_baixo') == '1',
        'estoque_zerado': request.args.get('estoque_zerado') == '1',
        'qtd_min': request.args.get('qtd_min', type=int) if request.args.get('qtd_min') else None,
        'qtd_max': request.args.get('qtd_max', type=int) if request.args.get('qtd_max') else None,
        'custo_min': request.args.get('custo_min', type=float) if request.args.get('custo_min') else None,
        'custo_max': request.args.get('custo_max', type=float) if request.args.get('custo_max') else None,
        'venda_min': request.args.get('venda_min', type=float) if request.args.get('venda_min') else None,
        'venda_max': request.args.get('venda_max', type=float) if request.args.get('venda_max') else None
    }
    
    # Chamada corrigida ao repositório
    pagination_obj = produto_service.produto_repo.listar_avancado(
        revendedor_id=revendedor_id, 
        filters=filters, 
        order_by_field=order_by, 
        order_dir=order_dir, 
        page=page, 
        per_page=per_page
    )
    
    # Cálculo de Indicadores em Tempo Real
    todos_produtos = produto_service.produto_repo.get_all_by_revendedor(revendedor_id)
    kpis = {
        'total_produtos': len(todos_produtos),
        'total_estoque': sum(p.quantidade_estoque for p in todos_produtos),
        'total_investido': sum(p.preco_custo * p.quantidade_estoque for p in todos_produtos),
        'total_potencial': sum(p.preco_venda * p.quantidade_estoque for p in todos_produtos),
        'estoque_critico': sum(1 for p in todos_produtos if p.quantidade_estoque <= p.estoque_minimo),
        'estoque_zerado': sum(1 for p in todos_produtos if p.quantidade_estoque == 0)
    }
    
    from app.services.categoria_service import CategoriaService
    from app.services.marca_service import MarcaService
    from app.services.fornecedor_service import FornecedorService
    
    return render_template(
        'produtos/estoque_geral.html',
        produtos=pagination_obj.items,
        pagination=pagination_obj,
        kpis=kpis,
        categorias=CategoriaService().listar_todas(revendedor_id),
        marcas=MarcaService().listar_todas(revendedor_id),
        fornecedores=FornecedorService().listar_todos(revendedor_id),
        current_filters=request.args,
        order_by=order_by, 
        order_dir=order_dir, 
        per_page=per_page
    )

@estoque_bp.route('/geral/novo', methods=['POST'])
@revendedor_required
def geral_novo():
    revendedor_id = session.get('revendedor_id')
    try:
        dt = request.form.get('data_compra')
        data_compra = datetime.strptime(dt, '%Y-%m-%d').date() if dt else None
        
        produto_service.criar_produto_avancado(
            revendedor_id=revendedor_id,
            categoria_id=request.form.get('categoria_id', type=int),
            marca_id=request.form.get('marca_id', type=int),
            fornecedor_id=request.form.get('fornecedor_id', type=int),
            nome=request.form.get('nome'),
            codigo_barras=request.form.get('codigo_barras'),
            descricao=request.form.get('descricao'),
            estoque_minimo=request.form.get('estoque_minimo', 0, type=int),
            preco_custo=request.form.get('preco_custo', 0),
            preco_venda=request.form.get('preco_venda', 0),
            data_compra=data_compra,
            situacao=request.form.get('situacao', 'Ativo'),
            quantidade_estoque=request.form.get('quantidade_estoque', 0)
        )
        flash('Produto cadastrado com sucesso!', 'success')
    except Exception as e:
        flash(str(e), 'danger')
    return redirect(url_for('estoque.geral'))

@estoque_bp.route('/geral/editar/<int:id_produto>', methods=['POST'])
@revendedor_required
def geral_editar(id_produto):
    revendedor_id = session.get('revendedor_id')
    try:
        dt = request.form.get('data_compra')
        data_compra = datetime.strptime(dt, '%Y-%m-%d').date() if dt else None
        
        produto_service.atualizar_produto_avancado(
            id_produto=id_produto,
            revendedor_id=revendedor_id,
            categoria_id=request.form.get('categoria_id', type=int),
            marca_id=request.form.get('marca_id', type=int),
            fornecedor_id=request.form.get('fornecedor_id', type=int),
            nome=request.form.get('nome'),
            codigo_barras=request.form.get('codigo_barras'),
            descricao=request.form.get('descricao'),
            estoque_minimo=request.form.get('estoque_minimo', 0, type=int),
            preco_custo=request.form.get('preco_custo', 0),
            preco_venda=request.form.get('preco_venda', 0),
            data_compra=data_compra,
            situacao=request.form.get('situacao'),
            quantidade_estoque=request.form.get('quantidade_estoque')
        )
        flash('Produto atualizado com sucesso!', 'success')
    except Exception as e:
        flash(str(e), 'danger')
    return redirect(url_for('estoque.geral'))

@estoque_bp.route('/geral/excluir/<int:id_produto>', methods=['POST'])
@revendedor_required
def geral_excluir(id_produto):
    revendedor_id = session.get('revendedor_id')
    try:
        produto_service.excluir_produto(id_produto, revendedor_id)
        flash('Produto removido com sucesso!', 'success')
    except Exception as e:
        flash(str(e), 'danger')
    return redirect(url_for('estoque.geral'))

@estoque_bp.route('/historico')
@revendedor_required
def historico():
    revendedor_id = session.get('revendedor_id')
    page = request.args.get('page', 1, type=int)
    from app.models.estoque import Estoque
    from app.models.produto import Produto
    
    query = Estoque.query.filter_by(revendedor_id=revendedor_id)
    pagination_obj = query.order_by(Estoque.data_movimentacao.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
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
        try:
            estoque_service.registrar_movimentacao(
                revendedor_id, 
                request.form.get('produto_id'), 
                request.form.get('tipo'), 
                request.form.get('motivo'), 
                request.form.get('quantidade'), 
                request.form.get('observacoes')
            )
            flash('Movimentação processada!', 'success')
            return redirect(url_for('estoque.historico'))
        except Exception as e:
            flash(str(e), 'danger')

    produtos = produto_service.listar_todos(revendedor_id)
    return render_template('produtos/movimentar_estoque.html', produtos=produtos)