from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Inicialização central das extensões do ecossistema
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class='config.Config'):
    """
    Application Factory para o ecossistema CosmetiKS.
    Inicializa extensões, injeta variáveis globais e gerencia o ciclo de vida do app.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializa persistência e migrações estruturais
    db.init_app(app)
    migrate.init_app(app, db)

    # Injeção de variáveis globais de template para uniformidade da marca
    @app.context_processor
    def inject_global_template_vars():
        return {
            'saas_name': 'CosmetiKS',
            'current_year': 2026
        }

    # Os Blueprints (Controllers) serão registrados sequencialmente aqui 
    # conforme cada módulo for acoplado na arquitetura.

    return app