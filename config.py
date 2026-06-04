import os

class Config:
    """Configuração base do ecossistema CosmetiKS (SaaS)."""
    # Chave secreta de sessão de alta entropia para proteção de cookies
    SECRET_KEY = os.environ.get('SECRET_KEY', 'cosmetiks_secure_and_cryptographically_strong_secret_key_2026_prod')
    
    # Caminho do Banco de Dados SQLite local
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'cosmetiks.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Segurança de Cookies de Sessão
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Upload de arquivos (Configurado como segurança preventiva, sem armazenamento de fotos)
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # Limite de 2MB para uploads administrativos gerais