from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Inicialização central das extensões do ecossistema para evitar importações circulares
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class='config.Config'):
    """
    Application Factory para o ecossistema CosmetiKS.
    Inicializa as extensões, injeta variáveis globais e registra todos os controladores.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializa persistência de dados e o motor de migrações estruturais (Alembic)
    db.init_app(app)
    migrate.init_app(app, db)

    # Injeção automática de variáveis globais de template para uniformidade da marca
    @app.context_processor
    def inject_global_template_vars():
        return {
            'saas_name': 'CosmetiKS',
            'current_year': 2026
        }

    # Registro de todos os Blueprints (Controllers) da arquitetura MVC
    from app.controllers.auth_controller import auth_bp
    from app.controllers.admin_controller import admin_bp
    from app.controllers.dashboard_controller import dashboard_bp
    from app.controllers.cliente_controller import cliente_bp
    from app.controllers.produto_controller import produto_bp
    from app.controllers.categoria_controller import categoria_bp
    from app.controllers.marca_controller import marca_bp
    from app.controllers.fornecedor_controller import fornecedor_bp
    from app.controllers.estoque_controller import estoque_bp
    from app.controllers.venda_controller import venda_bp
    from app.controllers.financeiro_controller import financeiro_bp
    from app.controllers.cobranca_controller import cobranca_bp
    from app.controllers.relatorio_controller import relatorio_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(cliente_bp)
    app.register_blueprint(produto_bp)
    app.register_blueprint(categoria_bp)
    app.register_blueprint(marca_bp)
    app.register_blueprint(fornecedor_bp)
    app.register_blueprint(estoque_bp)
    app.register_blueprint(venda_bp)
    app.register_blueprint(financeiro_bp)
    app.register_blueprint(cobranca_bp)
    app.register_blueprint(relatorio_bp)

    return app