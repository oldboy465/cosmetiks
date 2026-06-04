from flask import Blueprint, render_template, request, session, redirect, url_for, flash, Response
from app.models.cliente import Cliente
from app.models.produto import Produto
from app.models.venda import Venda
from app.models.financeiro import Financeiro
from functools import wraps
import openpyxl
from io import BytesIO

relatorio_bp = Blueprint('relatorio', __name__, url_prefix='/relatorios')

def revendedor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('usuario_logado') or session.get('is_admin'):
            flash('Acesso restrito a revendedores autenticados.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@relatorio_bp.route('/')
@revendedor_required
def index():
    return render_template('relatorios/index.html')

@relatorio_bp.route('/exportar/xlsx', methods=['GET'])
@revendedor_required
def exportar_xlsx():
    revendedor_id = session.get('revendedor_id')
    modulo = request.args.get('modulo', 'produtos')
    
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = f"Relatorio {modulo.capitalize()}"
    
    if modulo == 'produtos':
        ws.append(["Nome do Produto", "Estoque Atual", "Estoque Minimo", "Preco Custo", "Preco Venda", "Situacao"])
        dados = Produto.query.filter_by(revendedor_id=revendedor_id).all()
        for item in dados:
            ws.append([item.nome, item.quantidade_estoque, item.estoque_minimo, item.preco_custo, item.preco_venda, item.situacao])
            
    elif modulo == 'vendas':
        ws.append(["ID Venda", "Data", "Valor Liquido", "Forma Pagamento", "Situacao"])
        dados = Venda.query.filter_by(revendedor_id=revendedor_id).all()
        for item in dados:
            ws.append([item.id, item.data_venda.strftime('%d/%m/%Y'), item.valor_total, item.forma_pagamento, item.situacao])
            
    elif modulo == 'financeiro':
        ws.append(["Cliente", "Valor devido", "Vencimento", "Status"])
        dados = Financeiro.query.filter_by(revendedor_id=revendedor_id).all()
        for item in dados:
            ws.append([item.venda.cliente.nome, item.valor, item.vencimento.strftime('%d/%m/%Y'), item.status])

    output = BytesIO()
    wb.save(output)
    output.seek(0)
    
    return Response(
        output.read(),
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=cosmetiks_{modulo}_export.xlsx"}
    )