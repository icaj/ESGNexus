# esg_ml/infraestrutura/inicializacao_banco.py
import argparse
import os

from sqlalchemy.orm import Session

from esg_ml.infraestrutura.banco_dados import (
    Base, SessaoLocal, criar_tabelas, engine, obter_url_banco_mascarada,
)
from esg_ml.infraestrutura.modelos_banco import UsuarioBanco
from esg_ml.infraestrutura.seguranca import gerar_hash_senha
from esg_ml.infraestrutura.registro_log import obter_registrador

registrador = obter_registrador(__name__)

EMAIL_ADMIN_PADRAO = 'admin@esgnexus.example'
SENHA_ADMIN_PADRAO = 'admin123'


# ── helpers ───────────────────────────────────────────────────────────────────

def _criar_usuario_se_ausente(
    sessao: Session,
    email: str,
    senha: str,
    nome: str,
    perfil: str,
) -> tuple[UsuarioBanco, bool]:
    """Cria o usuário se não existir. Retorna (usuario, criado)."""
    existente = sessao.query(UsuarioBanco).filter(
        UsuarioBanco.email == email
    ).first()
    if existente is not None:
        return existente, False
    usuario = UsuarioBanco(
        nome=nome,
        email=email,
        senha_hash=gerar_hash_senha(senha),
        perfil=perfil,
        ativo=True,
    )
    sessao.add(usuario)
    sessao.commit()
    sessao.refresh(usuario)
    return usuario, True


# ── API pública ───────────────────────────────────────────────────────────────

def semear_banco() -> None:
    """Cria tabelas e seeds de usuários padrão.

    Chamado no startup da API (lifespan). Idempotente — seguro para rodar
    a cada reinicialização do contêiner.
    """
    registrador.info('semear_banco_inicio', banco=obter_url_banco_mascarada())

    # 1) Cria tabelas se não existirem
    criar_tabelas()

    with SessaoLocal() as sessao:
        # 2) Administrador padrão (variáveis USUARIO_ADMIN_*)
        admin_email = os.getenv('USUARIO_ADMIN_EMAIL', EMAIL_ADMIN_PADRAO)
        admin_senha = os.getenv('USUARIO_ADMIN_SENHA', SENHA_ADMIN_PADRAO)
        admin_nome  = os.getenv('USUARIO_ADMIN_NOME',  'Administrador ESG Nexus')
        usuario, criado = _criar_usuario_se_ausente(
            sessao, admin_email, admin_senha, admin_nome, 'administrador',
        )
        if criado:
            registrador.info('admin_criado', email=usuario.email)
            if admin_email == EMAIL_ADMIN_PADRAO:
                registrador.warning(
                    'senha_padrao_em_uso',
                    aviso='Altere USUARIO_ADMIN_SENHA antes de usar em produção',
                )
        else:
            registrador.info('admin_ja_existe', email=usuario.email)

        # 3) Conta de serviço do Airflow (variáveis ESG_ADMIN_*)
        airflow_email = os.getenv('ESG_ADMIN_EMAIL')
        airflow_senha = os.getenv('ESG_ADMIN_SENHA')
        if airflow_email and airflow_senha:
            svc, criado_svc = _criar_usuario_se_ausente(
                sessao,
                email=airflow_email,
                senha=airflow_senha,
                nome='Airflow Service Account',
                perfil='administrador',
            )
            if criado_svc:
                registrador.info('conta_servico_criada', email=svc.email)
            else:
                registrador.info('conta_servico_ja_existe', email=svc.email)

    registrador.info('semear_banco_concluido')


# ── CLI (manutenção / migrations) ─────────────────────────────────────────────

def criar_usuario_admin(sessao: Session) -> UsuarioBanco:
    """Atalho legado usado pelo CLI."""
    email = os.getenv('USUARIO_ADMIN_EMAIL', EMAIL_ADMIN_PADRAO)
    senha = os.getenv('USUARIO_ADMIN_SENHA', SENHA_ADMIN_PADRAO)
    nome  = os.getenv('USUARIO_ADMIN_NOME',  'Administrador ESG Nexus')
    usuario, _ = _criar_usuario_se_ausente(sessao, email, senha, nome, 'administrador')
    return usuario


def executar() -> None:
    parser = argparse.ArgumentParser(description='Inicializa o banco ESG Nexus Enterprise.')
    parser.add_argument('--recriar', action='store_true',
                        help='Drop + create all (APAGA TODOS OS DADOS)')
    parser.add_argument('--sem-admin', action='store_true',
                        help='Não cria usuário administrador padrão')
    args = parser.parse_args()

    print(f'Banco: {obter_url_banco_mascarada()}')
    from sqlalchemy import text
    with engine.connect() as c:
        c.execute(text('select 1'))
    print('Conexão OK.')

    if args.recriar:
        from esg_ml.infraestrutura import modelos_banco  # noqa: F401
        print('Recriando tabelas (drop all)...')
        Base.metadata.drop_all(bind=engine)

    criar_tabelas()
    print('Tabelas criadas/verificadas.')

    if not args.sem_admin:
        with SessaoLocal() as sessao:
            u, criado = _criar_usuario_se_ausente(
                sessao,
                os.getenv('USUARIO_ADMIN_EMAIL', EMAIL_ADMIN_PADRAO),
                os.getenv('USUARIO_ADMIN_SENHA', SENHA_ADMIN_PADRAO),
                os.getenv('USUARIO_ADMIN_NOME',  'Administrador ESG Nexus'),
                'administrador',
            )
            status = 'criado' if criado else 'já existia'
            print(f'Usuário admin ({status}): {u.email}')
            if criado and u.email == EMAIL_ADMIN_PADRAO:
                print(f'  Senha inicial: {SENHA_ADMIN_PADRAO}  ← altere antes de usar em produção')

    print('Banco inicializado com sucesso.')


if __name__ == '__main__':
    executar()
