from app import create_app, db
from flask_migrate import Migrate
import sys

# Script de gerenciamento de banco de dados e utilitários de CLI
app = create_app()

def init_db():
    """Inicializa o banco de dados e cria as tabelas baseadas nos modelos."""
    with app.app_context():
        db.create_all()
        print("Banco de dados CosmetiKS inicializado com sucesso.")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'init':
        init_db()
    else:
        print("Uso: python manage.py init")