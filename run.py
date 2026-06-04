from app import create_app

# Instanciação central da aplicação Flask pelo factory pattern
app = create_app()

if __name__ == '__main__':
    # Inicialização local do servidor em modo de desenvolvimento.
    # Em produção (ex: HostGator Linux), o arquivo será chamado pelo gerenciador WSGI.
    app.run(host='127.0.0.1', port=5000, debug=True)