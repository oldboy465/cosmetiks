from flask import Blueprint, render_template, redirect, url_for, session, flash
from app.models.venda import Venda, ItemVenda
from app.models.produto import Produto
from app.models.cliente import Cliente
from app.models.financeiro import Financeiro
from app.repositories.produto_repository import ProdutoRepository
from functools import wraps
from decimal import Decimal
from datetime import datetime, date

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')
produto_repo = ProdutoRepository()

def revendedor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('usuario_logado'):
            return redirect(url_for('auth.login'))
        if session.get('is_admin'):
            return redirect(url_for('admin.listar_revendedores'))
        return f(*args, **kwargs)
    return decorated_function

@dashboard_bp.route('/')
@revendedor_required
def index():
    revendedor_id = session.get('revendedor_id')
    
    vendas = Venda.query.filter_by(revendedor_id=revendedor_id).all()
    produtos = Produto.query.filter_by(revendedor_id=revendedor_id).all()
    clientes = Cliente.query.filter_by(revendedor_id=revendedor_id).all()
    contas = Financeiro.query.filter_by(revendedor_id=revendedor_id).all()

    receita_bruta = sum([v.valor_total for v in vendas])
    quantidade_vendas = len(vendas)
    ticket_medio = receita_bruta / quantidade_vendas if quantidade_vendas > 0 else Decimal('0.00')

    lucro_estimado = Decimal('0.00')
    quantidade_produtos_vendidos = 0
    for v in vendas:
        for item in v.itens:
            quantidade_produtos_vendidos += item.quantidade
            prod = produto_repo.get_by_id(item.produto_id)
            if prod:
                custo_total_item = prod.preco_custo * item.quantidade
                lucro_estimado += (item.valor_total - custo_total_item)

    valor_investido = sum([p.preco_custo * p.quantidade_estoque for p in produtos])
    valor_potencial = sum([p.preco_venda * p.quantidade_estoque for p in produtos])
    estoque_atual = sum([p.quantidade_estoque for p in produtos])
    estoque_baixo = len([p for p in produtos if p.quantidade_estoque <= p.estoque_minimo])

    novos_clientes = len([c for c in clientes if c.data_cadastro.date() == date.today()])
    clientes_ativos = len(clientes)
    clientes_inadimplentes = len(set([conta.cliente_id for conta in contas if conta.status == 'Atrasado']))

    produtos_ordenados = sorted(produtos, key=lambda p: sum([i.quantidade for i in ItemVenda.query.filter_by(produto_id=p.id).all()]), reverse=True)
    mais_vendidos = produtos_ordenados[:5]
    menos_vendidos = [p for p in produtos_ordenados if p.quantidade_estoque > 0][-5:]

    kpis = {
        "receita_bruta": receita_bruta,
        "ticket_medio": ticket_medio,
        "lucro_estimado": lucro_estimado,
        "valor_investido": valor_investido,
        "valor_potencial": valor_potencial,
        "estoque_atual": estoque_atual,
        "estoque_baixo": estoque_baixo,
        "clientes_ativos": clientes_ativos,
        "clientes_inadimplentes": clientes_inadimplentes,
        "quantidade_vendas": quantidade_vendas,
        "quantidade_produtos_vendidos": quantidade_produtos_vendidos,
        "mais_vendidos": mais_vendidos,
        "menos_vendidos": menos_vendidos
    }

    return render_template('dashboard/index.html', kpis=kpis)