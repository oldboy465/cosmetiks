from app.repositories.revendedor_repository import RevendedorRepository
from app.models.revendedor import Revendedor
from werkzeug.security import generate_password_hash
from datetime import datetime

class RevendedorService:
    def __init__(self):
        self.revendedor_repo = RevendedorRepository()

    def cadastrar_revendedor(self, dados):
        if self.revendedor_repo.get_by_usuario(dados.get('usuario')):
            raise ValueError("Nome de usuario ja utilizado no sistema.")
        if self.revendedor_repo.get_by_cpf(dados.get('cpf')):
            raise ValueError("CPF ja cadastrado no sistema.")
        if self.revendedor_repo.get_by_email(dados.get('email')):
            raise ValueError("E-mail ja cadastrado no sistema.")

        hash_senha = generate_password_hash(dados.get('senha'))
        
        # Correção operacional: Tratamento e conversão da String HTML para objeto date Python
        dt_nasc = dados.get('data_nascimento')
        data_nascimento_convertida = datetime.strptime(dt_nasc, '%Y-%m-%d').date() if dt_nasc else None
        
        novo_revendedor = Revendedor(
            nome_completo=dados.get('nome_completo'),
            cpf=dados.get('cpf'),
            data_nascimento=data_nascimento_convertida,
            sexo=dados.get('sexo'),
            telefone=dados.get('telefone'),
            whatsapp=dados.get('whatsapp'),
            email=dados.get('email'),
            cep=dados.get('cep'),
            logradouro=dados.get('logradouro'),
            numero=dados.get('numero'),
            complemento=dados.get('complemento'),
            bairro=dados.get('bairro'),
            cidade=dados.get('cidade'),
            estado=dados.get('estado'),
            usuario=dados.get('usuario'),
            senha_criptografada=hash_senha,
            situacao='Ativo',
            observacoes=dados.get('observacoes')
        )
        
        self.revendedor_repo.add(novo_revendedor)
        self.revendedor_repo.commit()
        return novo_revendedor

    def atualizar_revendedor(self, revendedor_id, dados):
        revendedor = self.revendedor_repo.get_by_id(revendedor_id)
        if not revendedor:
            raise ValueError("Revendedor nao localizado.")

        revendedor.nome_completo = dados.get('nome_completo', revendedor.nome_completo)
        revendedor.telefone = dados.get('telefone', revendedor.telefone)
        revendedor.whatsapp = dados.get('whatsapp', revendedor.whatsapp)
        revendedor.cep = dados.get('cep', revendedor.cep)
        revendedor.logradouro = dados.get('logradouro', revendedor.logradouro)
        revendedor.numero = dados.get('numero', revendedor.numero)
        revendedor.complemento = dados.get('complemento', revendedor.complemento)
        revendedor.bairro = dados.get('bairro', revendedor.bairro)
        revendedor.cidade = dados.get('cidade', revendedor.cidade)
        revendedor.estado = dados.get('estado', revendedor.estado)
        revendedor.observacoes = dados.get('observacoes', revendedor.observacoes)

        if dados.get('data_nascimento'):
            dt_nasc = dados.get('data_nascimento')
            revendedor.data_nascimento = datetime.strptime(dt_nasc, '%Y-%m-%d').date() if dt_nasc else None

        if dados.get('senha'):
            revendedor.senha_criptografada = generate_password_hash(dados.get('senha'))

        self.revendedor_repo.commit()
        return revendedor

    def alterar_situacao(self, revendedor_id, nova_situacao):
        if nova_situacao not in ['Ativo', 'Inativo', 'Bloqueado']:
            raise ValueError("Situacao comercial invalida.")
            
        revendedor = self.revendedor_repo.get_by_id(revendedor_id)
        if not revendedor:
            raise ValueError("Revendedor nao localizado.")
            
        revendedor.situacao = nova_situacao
        self.revendedor_repo.commit()
        return revendedor

    def listar_todos(self):
        return self.revendedor_repo.get_todos_ordenados()