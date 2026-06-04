from app.models.produto import Produto
from app.repositories.base_repository import BaseRepository
from sqlalchemy import desc, asc

class ProdutoRepository(BaseRepository):
    def __init__(self):
        super().__init__(Produto)

    def buscar_por_codigo_barras(self, revendedor_id, codigo_barras):
        return self.model.query.filter_by(revendedor_id=revendedor_id, codigo_barras=codigo_barras).first()

    def verificar_estoque_baixo(self, revendedor_id):
        return self.model.query.filter(
            self.model.revendedor_id == revendedor_id,
            self.model.quantidade_estoque <= self.model.estoque_minimo
        ).order_by(self.model.nome.asc()).all()

    def buscar_com_filtros(self, revendedor_id, nome=None, categoria_id=None, marca_id=None, fornecedor_id=None):
        query = self.model.query.filter_by(revendedor_id=revendedor_id)
        if nome:
            query = query.filter(self.model.nome.ilike(f'%{nome}%'))
        if categoria_id:
            query = query.filter_by(categoria_id=categoria_id)
        if marca_id:
            query = query.filter_by(marca_id=marca_id)
        if fornecedor_id:
            query = query.filter_by(fornecedor_id=fornecedor_id)
        return query.order_by(self.model.nome.asc()).all()

    def get_todos_ordenados(self, revendedor_id):
        return self.model.query.filter_by(revendedor_id=revendedor_id).order_by(self.model.nome.asc()).all()

    def listar_avancado(self, revendedor_id, filters, order_by_field, order_dir, page, per_page):
        """Implementação da lógica de busca avançada para o painel de Estoque Geral."""
        query = self.model.query.filter_by(revendedor_id=revendedor_id)
        
        # Filtros de Identificação
        if filters.get('nome'):
            query = query.filter(self.model.nome.ilike(f"%{filters['nome']}%"))
        if filters.get('id'):
            query = query.filter(self.model.id == filters['id'])
        if filters.get('codigo_barras'):
            query = query.filter(self.model.codigo_barras.ilike(f"%{filters['codigo_barras']}%"))
            
        # Filtros de Relacionamento
        if filters.get('marca_id'):
            query = query.filter(self.model.marca_id == filters['marca_id'])
        if filters.get('categoria_id'):
            query = query.filter(self.model.categoria_id == filters['categoria_id'])
        if filters.get('fornecedor_id'):
            query = query.filter(self.model.fornecedor_id == filters['fornecedor_id'])
        if filters.get('situacao'):
            query = query.filter(self.model.situacao == filters['situacao'])
            
        # Filtros de Status de Estoque
        if filters.get('estoque_baixo'):
            query = query.filter(self.model.quantidade_estoque <= self.model.estoque_minimo)
        if filters.get('estoque_zerado'):
            query = query.filter(self.model.quantidade_estoque == 0)
            
        # Filtros por Faixas Numéricas
        if filters.get('qtd_min') is not None:
            query = query.filter(self.model.quantidade_estoque >= filters['qtd_min'])
        if filters.get('qtd_max') is not None:
            query = query.filter(self.model.quantidade_estoque <= filters['qtd_max'])
        if filters.get('custo_min') is not None:
            query = query.filter(self.model.preco_custo >= filters['custo_min'])
        if filters.get('custo_max') is not None:
            query = query.filter(self.model.preco_custo <= filters['custo_max'])
        if filters.get('venda_min') is not None:
            query = query.filter(self.model.preco_venda >= filters['venda_min'])
        if filters.get('venda_max') is not None:
            query = query.filter(self.model.preco_venda <= filters['venda_max'])

        # Lógica de Ordenação Dinâmica
        order_expression = self.model.nome
        if order_by_field == 'id':
            order_expression = self.model.id
        elif order_by_field == 'marca':
            from app.models.marca import Marca
            query = query.join(Marca, self.model.marca_id == Marca.id)
            order_expression = Marca.nome
        elif order_by_field == 'categoria':
            from app.models.categoria import Categoria
            query = query.join(Categoria, self.model.categoria_id == Categoria.id)
            order_expression = Categoria.nome
        elif order_by_field == 'quantidade_estoque':
            order_expression = self.model.quantidade_estoque
        elif order_by_field == 'preco_custo':
            order_expression = self.model.preco_custo
        elif order_by_field == 'preco_venda':
            order_expression = self.model.preco_venda
        elif order_by_field == 'valor_investido':
            order_expression = self.model.preco_custo * self.model.quantidade_estoque
        elif order_by_field == 'valor_potencial':
            order_expression = self.model.preco_venda * self.model.quantidade_estoque
        elif order_by_field == 'data_compra':
            order_expression = self.model.data_compra
            
        final_order = desc(order_expression) if order_dir == 'desc' else asc(order_expression)
        return query.order_by(final_order).paginate(page=page, per_page=per_page, error_out=False)