import os
import sys
from datetime import date
from decimal import Decimal
import pandas as pd

# Garante que o script standalone consiga enxergar a pasta 'app' no Windows
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from app.models.produto import Produto
from app.models.categoria import Categoria
from app.models.marca import Marca
from app.models.fornecedor import Fornecedor

# Definições de caminhos e chaves do ambiente
REVENDEDOR_ID = 1
MARCA_BOTICARIO_ID = 1  # ID fixo travado para a marca Boticário conforme solicitado
CAMINHO_PLANILHA = r"C:\Users\noteboy\Desktop\add.xlsx"

def executar_cadastro_custos():
    app = create_app()
    with app.app_context():
        print(f"\n🚀 Iniciando importação com custos unificados para 'Boticário': {CAMINHO_PLANILHA}")
        
        if not os.path.exists(CAMINHO_PLANILHA):
            print(f"❌ Erro: O arquivo não foi localizado em {CAMINHO_PLANILHA}")
            return

        try:
            # Carrega a planilha usando o Pandas
            df = pd.read_excel(CAMINHO_PLANILHA, sheet_name='Plan1')
        except Exception as e:
            print(f"❌ Falha ao processar o arquivo Excel: {str(e)}")
            return

        # Recupera o fornecedor padrão cadastrado na sua base (ID 1)
        fornecedor_padrao = Fornecedor.query.filter_by(revendedor_id=REVENDEDOR_ID).first()
        if not fornecedor_padrao:
            print("❌ Erro: Nenhum fornecedor de vínculo localizado para o revendedor 1.")
            return

        produtos_cadastrados = 0
        produtos_ignorados = 0

        # Varredura linha por linha da planilha add.xlsx
        for index, row in df.iterrows():
            cod_prod_raw = row['Cód. Produto']
            descricao_prod_raw = row['Descrição do Produto']
            valor_unitario_raw = row['Valor Unitário']
            categoria_raw = row['Categoria']

            # Pula linhas vazias
            if pd.isna(descricao_prod_raw) or str(descricao_prod_raw).strip() == "":
                continue

            nome_produto = str(descricao_prod_raw).strip()
            categoria_nome = str(categoria_raw).strip() if not pd.isna(categoria_raw) else "Geral"
            
            # Sanitização do código de barras (remove decimais de float do Excel)
            if pd.isna(cod_prod_raw):
                codigo_barras = None
            else:
                try:
                    codigo_barras = str(int(float(cod_prod_raw))).strip()
                except ValueError:
                    codigo_barras = str(cod_prod_raw).strip()

            # Tratamento e conversão segura do Valor Unitário (Preço de Custo)
            try:
                preco_custo = Decimal(str(valor_unitario_raw)) if not pd.isna(valor_unitario_raw) else Decimal('0.00')
            except Exception:
                preco_custo = Decimal('0.00')

            # 1. Resolução Dinâmica de Categorias (Busca ou cria se não existir)
            categoria = Categoria.query.filter_by(revendedor_id=REVENDEDOR_ID, nome=categoria_nome).first()
            if not categoria:
                categoria = Categoria(revendedor_id=REVENDEDOR_ID, nome=categoria_nome)
                db.session.add(categoria)
                db.session.commit()  # Gera o ID da nova categoria imediatamente

            # 2. CONTROLE DE DUPLICIDADE (Garante a integridade sem alterar registros antigos)
            produto_existente = None
            if codigo_barras:
                produto_existente = Produto.query.filter_by(revendedor_id=REVENDEDOR_ID, codigo_barras=codigo_barras).first()
            if not produto_existente:
                produto_existente = Produto.query.filter_by(revendedor_id=REVENDEDOR_ID, nome=nome_produto).first()

            if produto_existente:
                produtos_ignorados += 1
                continue

            # 3. Construção e persistência do novo produto com custo associado
            novo_produto = Produto(
                revendedor_id=REVENDEDOR_ID,
                categoria_id=categoria.id,
                marca_id=MARCA_BOTICARIO_ID,  # Vinculado 100% à marca Boticário
                fornecedor_id=fornecedor_padrao.id,
                nome=nome_produto,
                codigo_barras=codigo_barras,
                quantidade_estoque=0,
                estoque_minimo=3,
                preco_custo=preco_custo,      # Custo unitário injetado dinamicamente do Excel
                preco_venda=Decimal('0.00'),   # Preço de venda zerado para definição posterior
                data_compra=date.today(),
                situacao='Ativo',
                descricao="Importado com sucesso via add.xlsx"
            )
            db.session.add(novo_produto)
            produtos_cadastrados += 1

        # Confirma as alterações do lote no banco de dados
        db.session.commit()
        
        print("\n=======================================================")
        print("🎉 PROCESSAMENTO UNIFICADO CONCLUÍDO COM SUCESSO!")
        print(f"🔹 Produtos Boticário cadastrados com custo: {produtos_cadastrados}")
        print(f"🔹 Itens ignorados por já constarem na base: {produtos_ignorados}")
        print("=======================================================\n")

if __name__ == '__main__':
    executar_cadastro_custos()