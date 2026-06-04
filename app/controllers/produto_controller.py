from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services.produto_service import ProdutoService
from app.services.categoria_service import CategoriaService
from app.services.marca_service import MarcaService
from app.services.fornecedor_service import FornecedorService
from functools import wraps
from datetime import datetime

produto_bp = Blueprint('produto', __name__, url_prefix='/produtos')
produto_service = ProdutoService()
categoria_service = CategoriaService()
marca_service = MarcaService()
fornecedor_service = FornecedorService()

def revendedor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('usuario_logado') or session.get('is_admin'):
            flash('Acesso restrito a revendedores autenticados.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@produto_bp.route('/')
@revendedor_required
def index():
    revendedor_id = session.get('revendedor_id')
    nome = request.args.get('nome')
    categoria_id = request.args.get('categoria_id')
    marca_id = request.args.get('marca_id')
    fornecedor_id = request.args.get('fornecedor_id')
    
    lista = produto_service.buscar_com_filtros(revendedor_id, nome, categoria_id, marca_id, fornecedor_id)
    categorias = categoria_service.listar_todas(revendedor_id)
    marcas = marca_service.listar_todas(revendedor_id)
    fornecedores = fornecedor_service.listar_todos(revendedor_id)
    
    return render_template('produtos/index.html', produtos=lista, categorias=categorias, marcas=marcas, fornecedores=fornecedores)

@produto_bp.route('/novo', methods=['GET', 'POST'])
@revendedor_required
def novo():
    revendedor_id = session.get('revendedor_id')
    if request.method == 'POST':
        categoria_id = request.form.get('categoria_id')
        marca_id = request.form.get('marca_id')
        fornecedor_id = request.form.get('fornecedor_id')
        nome = request.form.get('nome')
        codigo_barras = request.form.get('codigo_barras')
        descricao = request.form.get('descricao')
        estoque_minimo = request.form.get('estoque_minimo')
        preco_custo = request.form.get('preco_custo')
        preco_venda = request.form.get('preco_venda')
        
        dt_compra = request.form.get('data_compra')
        data_compra = datetime.strptime(dt_compra, '%Y-%m-%d').date() if dt_compra else None
        situacao = request.form.get('situacao')

        try:
            produto_service.criar_produto(revendedor_id, categoria_id, marca_id, fornecedor_id, nome, codigo_barras, descricao, estoque_minimo, preco_custo, preco_venda, data_compra, situacao)
            flash('Produto catalogado operacionalmente com sucesso.', 'success')
            return redirect(url_for('produto.index'))
        except ValueError as e:
            flash(str(e), 'danger')

    categorias = categoria_service.listar_todas(revendedor_id)
    marcas = marca_service.listar_todas(revendedor_id)
    fornecedores = fornecedor_service.listar_todos(revendedor_id)
    return render_template('produtos/form.html', produto=None, categorias=categorias, marcas=marcas, fornecedores=fornecedores)

@produto_bp.route('/editar/<int:id_produto>', methods=['GET', 'POST'])
@revendedor_required
def editar(id_produto):
    revendedor_id = session.get('revendedor_id')
    if request.method == 'POST':
        categoria_id = request.form.get('categoria_id')
        marca_id = request.form.get('marca_id')
        fornecedor_id = request.form.get('fornecedor_id')
        nome = request.form.get('nome')
        codigo_barras = request.form.get('codigo_barras')
        descricao = request.form.get('descricao')
        estoque_minimo = request.form.get('estoque_minimo')
        preco_custo = request.form.get('preco_custo')
        preco_venda = request.form.get('preco_venda')
        
        dt_compra = request.form.get('data_compra')
        data_compra = datetime.strptime(dt_compra, '%Y-%m-%d').date() if dt_compra else None
        situacao = request.form.get('situacao')

        try:
            produto_service.atualizar_produto(id_produto, revendedor_id, categoria_id, marca_id, fornecedor_id, nome, codigo_barras, descricao, estoque_minimo, preco_custo, preco_venda, data_compra, situacao)
            flash('Produto atualizado com sucesso.', 'success')
            return redirect(url_for('produto.index'))
        except ValueError as e:
            flash(str(e), 'danger')

    prod = produto_service.produto_repo.get_by_id_and_revendedor(id_produto, revendedor_id)
    categorias = categoria_service.listar_todas(revendedor_id)
    marcas = marca_service.listar_todas(revendedor_id)
    fornecedores = fornecedor_service.listar_todos(revendedor_id)
    return render_template('produtos/form.html', produto=prod, categorias=categorias, marcas=marcas, fornecedores=fornecedores)

@produto_bp.route('/excluir/<int:id_produto>', methods=['POST'])
@revendedor_required
def excluir(id_produto):
    revendedor_id = session.get('revendedor_id')
    try:
        produto_service.excluir_produto(id_produto, revendedor_id)
        flash('Produto removido do catalogo operacional.', 'success')
    except ValueError as e:
        flash(str(e), 'danger')
    return redirect(url_for('produto.index'))