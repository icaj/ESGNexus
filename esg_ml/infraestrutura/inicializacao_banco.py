# esg_ml/infraestrutura/inicializacao_banco.py
import argparse, os
from pathlib import Path
from sqlalchemy.orm import Session
from esg_ml.infraestrutura.banco_dados import Base, SessaoLocal, criar_tabelas, engine, obter_url_banco_mascarada
from esg_ml.infraestrutura.modelos_banco import FornecedorBanco, UsuarioBanco
from esg_ml.infraestrutura.seguranca import gerar_hash_senha

EMAIL_ADMIN_PADRAO = 'admin@esgnexus.local'
SENHA_ADMIN_PADRAO = 'admin123'

def criar_usuario_admin(sessao: Session) -> UsuarioBanco:
    email = os.getenv('USUARIO_ADMIN_EMAIL', EMAIL_ADMIN_PADRAO)
    senha = os.getenv('USUARIO_ADMIN_SENHA', SENHA_ADMIN_PADRAO)
    nome  = os.getenv('USUARIO_ADMIN_NOME',  'Administrador ESG Nexus')
    usuario = sessao.query(UsuarioBanco).filter(UsuarioBanco.email == email).first()
    if usuario is not None:
        return usuario
    usuario = UsuarioBanco(nome=nome, email=email,
                           senha_hash=gerar_hash_senha(senha),
                           perfil='administrador', ativo=True)
    sessao.add(usuario); sessao.commit(); sessao.refresh(usuario)
    return usuario

def executar() -> None:
    parser = argparse.ArgumentParser(description='Inicializa o banco ESG Nexus Enterprise.')
    parser.add_argument('--recriar', action='store_true')
    parser.add_argument('--sem-admin', action='store_true')
    args = parser.parse_args()

    print(f'Banco: {obter_url_banco_mascarada()}')
    from sqlalchemy import text
    with engine.connect() as c: c.execute(text('select 1'))

    if args.recriar:
        from esg_ml.infraestrutura import modelos_banco  # noqa
        Base.metadata.drop_all(bind=engine)
    criar_tabelas()

    if not args.sem_admin:
        with SessaoLocal() as sessao:
            u = criar_usuario_admin(sessao)
            print(f'Usuário admin: {u.email}')
            if u.email == EMAIL_ADMIN_PADRAO:
                print(f'Senha inicial: {SENHA_ADMIN_PADRAO}  ← altere antes de usar em produção')

    print('Banco inicializado com sucesso.')

if __name__ == '__main__':
    executar()
