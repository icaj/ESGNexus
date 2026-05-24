import os
from contextlib import contextmanager
from urllib.parse import urlparse, parse_qs

import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL nao configurada. Crie o arquivo .env com a string do NeonDB.")


def get_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)


@contextmanager
def db_cursor(commit: bool = False):
    conn = get_connection()
    try:
        cur = conn.cursor()
        yield cur
        if commit:
            conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    with db_cursor(commit=True) as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id BIGSERIAL PRIMARY KEY,
                nome VARCHAR(120) NOT NULL,
                email VARCHAR(160) UNIQUE NOT NULL,
                senha_hash VARCHAR(255) NOT NULL,
                perfil VARCHAR(40) NOT NULL DEFAULT 'ADMIN',
                ativo BOOLEAN NOT NULL DEFAULT TRUE,
                data_criacao TIMESTAMP NOT NULL DEFAULT NOW()
            );

            CREATE TABLE IF NOT EXISTS fornecedores (
                id BIGSERIAL PRIMARY KEY,
                razao_social VARCHAR(255) NOT NULL,
                nome_fantasia VARCHAR(255),
                cnpj VARCHAR(20) UNIQUE,
                email VARCHAR(160),
                telefone VARCHAR(50),
                nome_contato VARCHAR(160),
                segmento VARCHAR(100),
                categoria VARCHAR(100),
                estado VARCHAR(50),
                cidade VARCHAR(100),
                nivel_risco VARCHAR(30) DEFAULT 'MEDIO',
                status VARCHAR(30) DEFAULT 'ATIVO',
                data_criacao TIMESTAMP NOT NULL DEFAULT NOW(),
                data_atualizacao TIMESTAMP NOT NULL DEFAULT NOW()
            );

            CREATE TABLE IF NOT EXISTS avaliacoes_fornecedor (
                id BIGSERIAL PRIMARY KEY,
                fornecedor_id BIGINT NOT NULL REFERENCES fornecedores(id) ON DELETE CASCADE,
                data_avaliacao DATE NOT NULL DEFAULT CURRENT_DATE,
                nota_ambiental NUMERIC(6,2) NOT NULL DEFAULT 0,
                nota_social NUMERIC(6,2) NOT NULL DEFAULT 0,
                nota_governanca NUMERIC(6,2) NOT NULL DEFAULT 0,
                nota_final NUMERIC(6,2) NOT NULL DEFAULT 0,
                classificacao VARCHAR(5),
                observacoes TEXT,
                data_criacao TIMESTAMP NOT NULL DEFAULT NOW()
            );

            CREATE TABLE IF NOT EXISTS certificacoes_fornecedor (
                id BIGSERIAL PRIMARY KEY,
                fornecedor_id BIGINT NOT NULL REFERENCES fornecedores(id) ON DELETE CASCADE,
                nome VARCHAR(160) NOT NULL,
                orgao_emissor VARCHAR(160),
                data_emissao DATE,
                data_validade DATE,
                status VARCHAR(30) DEFAULT 'VALIDA',
                url_arquivo TEXT,
                data_criacao TIMESTAMP NOT NULL DEFAULT NOW()
            );

            CREATE TABLE IF NOT EXISTS alertas (
                id BIGSERIAL PRIMARY KEY,
                fornecedor_id BIGINT REFERENCES fornecedores(id) ON DELETE CASCADE,
                tipo_alerta VARCHAR(80) NOT NULL,
                severidade VARCHAR(30) NOT NULL DEFAULT 'MEDIA',
                titulo VARCHAR(180) NOT NULL,
                descricao TEXT,
                status VARCHAR(30) NOT NULL DEFAULT 'ABERTO',
                data_criacao TIMESTAMP NOT NULL DEFAULT NOW(),
                data_resolucao TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS configuracoes (
                id BIGSERIAL PRIMARY KEY,
                chave VARCHAR(120) UNIQUE NOT NULL,
                valor TEXT NOT NULL
            );
            """
        )

        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        senha_hash = pwd_context.hash("admin123")
        cur.execute(
            """
            INSERT INTO usuarios (nome, email, senha_hash, perfil)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (email) DO NOTHING
            """,
            ("Administrador", "admin@esgnexus.com", senha_hash, "ADMIN"),
        )

        configuracoes = {
            "peso_ambiental": "0.35",
            "peso_social": "0.30",
            "peso_governanca": "0.35",
            "score_minimo_aceitavel": "60",
            "dias_alerta_certificacao": "30",
        }
        for chave, valor in configuracoes.items():
            cur.execute(
                """
                INSERT INTO configuracoes (chave, valor)
                VALUES (%s, %s)
                ON CONFLICT (chave) DO NOTHING
                """,
                (chave, valor),
            )
