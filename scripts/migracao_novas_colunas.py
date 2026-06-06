import os
import sqlite3

# Resolve o caminho absoluto para o banco de dados localizado na raiz do projeto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_PATH = os.path.join(BASE_DIR, 'cosmetiks.db')

def rodar_migracao_segura():
    print(f"🚀 Iniciando injeção segura de colunas no banco de dados...")
    print(f"📂 Alvo: {DB_PATH}")

    if not os.path.exists(DB_PATH):
        print("❌ Erro Crítico: O arquivo cosmetiks.db não foi localizado na raiz do projeto.")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # 1. Injeção segura da coluna 'observacoes'
        try:
            cursor.execute("ALTER TABLE vendas ADD COLUMN observacoes TEXT;")
            print("✅ Sucesso: Coluna 'observacoes' (TEXT) adicionada à tabela 'vendas'.")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print("⚠️ Aviso: A coluna 'observacoes' já existe na tabela. Pulo realizado.")
            else:
                print(f"❌ Erro ao processar a coluna 'observacoes': {e}")

        # 2. Injeção segura da coluna 'data_prevista_pagamento'
        try:
            cursor.execute("ALTER TABLE vendas ADD COLUMN data_prevista_pagamento DATE;")
            print("✅ Sucesso: Coluna 'data_prevista_pagamento' (DATE) adicionada à tabela 'vendas'.")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print("⚠️ Aviso: A coluna 'data_prevista_pagamento' já existe na tabela. Pulo realizado.")
            else:
                print(f"❌ Erro ao processar a coluna 'data_prevista_pagamento': {e}")

        conn.commit()
        print("🎉 Migração finalizada. Estrutura atualizada sem perda de dados operacionais.")
        
    except sqlite3.Error as e:
        print(f"❌ Ocorreu um erro crítico ao tentar manipular o banco de dados: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == '__main__':
    rodar_migracao_segura()