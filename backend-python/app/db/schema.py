from passlib.hash import bcrypt
from app.db.connection import get_connection
import logging

logger = logging.getLogger(__name__)

DDL = [
    '''CREATE TABLE IF NOT EXISTS perfis (
        id BIGSERIAL PRIMARY KEY,
        nome VARCHAR(80) NOT NULL UNIQUE,
        descricao VARCHAR(255)
    )''',
    '''CREATE TABLE IF NOT EXISTS usuarios (
        id BIGSERIAL PRIMARY KEY,
        nome VARCHAR(150) NOT NULL,
        email VARCHAR(180) NOT NULL UNIQUE,
        senha_hash VARCHAR(255) NOT NULL,
        perfil_id BIGINT NOT NULL,
        ativo BOOLEAN NOT NULL DEFAULT TRUE,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT fk_usuarios_perfis FOREIGN KEY (perfil_id) REFERENCES perfis(id)
    )''',
    '''CREATE TABLE IF NOT EXISTS fornecedores (
        id BIGSERIAL PRIMARY KEY,
        razao_social VARCHAR(255) NOT NULL,
        nome_fantasia VARCHAR(255),
        cnpj VARCHAR(20) UNIQUE,
        email VARCHAR(150),
        telefone VARCHAR(50),
        nome_contato VARCHAR(150),
        segmento VARCHAR(100),
        categoria VARCHAR(100),
        pais VARCHAR(100),
        estado VARCHAR(100),
        cidade VARCHAR(100),
        nivel_risco VARCHAR(50) DEFAULT 'MEDIO',
        status VARCHAR(50) DEFAULT 'ATIVO',
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''',
    '''CREATE TABLE IF NOT EXISTS certificacoes (
        id BIGSERIAL PRIMARY KEY,
        nome VARCHAR(120) NOT NULL UNIQUE,
        descricao VARCHAR(255),
        orgao_emissor VARCHAR(120)
    )''',
    '''CREATE TABLE IF NOT EXISTS certificacoes_fornecedor (
        id BIGSERIAL PRIMARY KEY,
        fornecedor_id BIGINT NOT NULL,
        certificacao_id BIGINT NOT NULL,
        data_emissao DATE,
        data_validade DATE,
        status VARCHAR(50) DEFAULT 'VALIDA',
        url_arquivo VARCHAR(500),
        CONSTRAINT fk_cert_fornecedor FOREIGN KEY (fornecedor_id) REFERENCES fornecedores(id),
        CONSTRAINT fk_cert_certificacao FOREIGN KEY (certificacao_id) REFERENCES certificacoes(id)
    )''',
    '''CREATE TABLE IF NOT EXISTS avaliacoes_fornecedor (
        id BIGSERIAL PRIMARY KEY,
        fornecedor_id BIGINT NOT NULL,
        data_avaliacao DATE NOT NULL,
        nota_ambiental NUMERIC(6,2) NOT NULL DEFAULT 0,
        nota_social NUMERIC(6,2) NOT NULL DEFAULT 0,
        nota_governanca NUMERIC(6,2) NOT NULL DEFAULT 0,
        nota_final NUMERIC(6,2) NOT NULL DEFAULT 0,
        observacoes TEXT,
        criado_por BIGINT,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT fk_avaliacoes_fornecedor FOREIGN KEY (fornecedor_id) REFERENCES fornecedores(id)
    )''',
    '''CREATE TABLE IF NOT EXISTS alertas (
        id BIGSERIAL PRIMARY KEY,
        fornecedor_id BIGINT,
        tipo_alerta VARCHAR(80) NOT NULL,
        severidade VARCHAR(30) NOT NULL,
        titulo VARCHAR(180) NOT NULL,
        descricao TEXT,
        data_limite DATE,
        status VARCHAR(40) DEFAULT 'ABERTO',
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        data_resolucao TIMESTAMP NULL,
        CONSTRAINT fk_alertas_fornecedor FOREIGN KEY (fornecedor_id) REFERENCES fornecedores(id)
    )''',
    '''CREATE TABLE IF NOT EXISTS configuracoes (
        id BIGSERIAL PRIMARY KEY,
        chave VARCHAR(100) NOT NULL UNIQUE,
        valor VARCHAR(255) NOT NULL
    )'''
]

TRIGGERS = [
    '''CREATE OR REPLACE FUNCTION atualizar_data_atualizacao()
       RETURNS TRIGGER AS $$
       BEGIN
           NEW.data_atualizacao = CURRENT_TIMESTAMP;
           RETURN NEW;
       END;
       $$ LANGUAGE plpgsql''',
    '''DROP TRIGGER IF EXISTS trg_usuarios_data_atualizacao ON usuarios''',
    '''CREATE TRIGGER trg_usuarios_data_atualizacao
       BEFORE UPDATE ON usuarios
       FOR EACH ROW EXECUTE FUNCTION atualizar_data_atualizacao()''',
    '''DROP TRIGGER IF EXISTS trg_fornecedores_data_atualizacao ON fornecedores''',
    '''CREATE TRIGGER trg_fornecedores_data_atualizacao
       BEFORE UPDATE ON fornecedores
       FOR EACH ROW EXECUTE FUNCTION atualizar_data_atualizacao()'''
]

SEED = [
    '''INSERT INTO fornecedores (razao_social, nome_fantasia, cnpj, email, telefone, nome_contato, segmento, categoria, cidade, estado, pais, nivel_risco, status)
       VALUES 
       ('Fornecedor Verde Ltda', 'Fornecedor Verde', '11111111000101', 'contato@verde.com', '81999990001', 'Maria Silva', 'Industrial', 'Energia', 'Recife', 'PE', 'Brasil', 'BAIXO', 'ATIVO'),
       ('Eco Social Servicos SA', 'Eco Social', '22222222000102', 'contato@ecosocial.com', '81999990002', 'Joao Souza', 'Servicos', 'Facilities', 'Sao Paulo', 'SP', 'Brasil', 'MEDIO', 'ATIVO');''',
    '''INSERT INTO avaliacoes_fornecedor (fornecedor_id, data_avaliacao, nota_ambiental, nota_social, nota_governanca, nota_final, observacoes)
       VALUES 
       (1, '2026-04-10', 92, 88, 90, 90.10, 'Fornecedor com alto nivel de aderencia ESG'),
       (2, '2026-04-12', 75, 82, 70, 75.35, 'Necessita fortalecer governanca');''',
    '''INSERT INTO certificacoes (id, nome, descricao, orgao_emissor)
       VALUES 
       (1, 'ISO 14001', 'Certificação ambiental', 'ABNT'),
       (2, 'ISO 45001', 'Certificação de segurança e saúde no trabalho', 'Bureau Veritas');''',
    '''INSERT INTO certificacoes_fornecedor (fornecedor_id, certificacao_id, data_emissao, data_validade, status, url_arquivo)
       VALUES 
       (1, 1, '2025-01-15', '2027-01-15', 'VALIDA', 'https://example.com/cert1.pdf'),
       (2, 2, '2024-08-01', '2026-08-01', 'VALIDA', 'https://example.com/cert2.pdf');''',
    '''INSERT INTO alertas (fornecedor_id, tipo_alerta, severidade, titulo, descricao, status)
       VALUES 
       (2, 'NOTA_GOVERNANCA_BAIXA', 'ALTA', 'Governanca abaixo da meta', 'Fornecedor com score de governanca abaixo da meta minima.', 'ABERTO');'''
]

def init_db():
    with get_connection() as conn:
        cur = conn.cursor()
        for ddl in DDL:
            cur.execute(ddl)
        for sql in TRIGGERS:
            cur.execute(sql)

        cur.execute("""
            INSERT INTO perfis (id, nome, descricao)
            VALUES (1, 'ADMINISTRADOR', 'Administrador do sistema')
            ON CONFLICT (id) DO NOTHING
        """)
        cur.execute("""
            INSERT INTO perfis (id, nome, descricao)
            VALUES (2, 'ANALISTA_ESG', 'Analista ESG')
            ON CONFLICT (id) DO NOTHING
        """)
        cur.execute("SELECT setval(pg_get_serial_sequence('perfis', 'id'), GREATEST((SELECT MAX(id) FROM perfis), 1))")

        cur.execute("SELECT id FROM usuarios WHERE email = %s", ('admin@esgnexus.com',))
        if cur.fetchone() is None:
            cur.execute(
                """INSERT INTO usuarios (nome, email, senha_hash, perfil_id, ativo)
                   VALUES (%s, %s, %s, %s, %s)""",
                ('Administrador', 'admin@esgnexus.com', bcrypt.hash('admin123'), 1, True)
            )

        configuracoes_iniciais = [
            ('peso_ambiental', '0.35'),
            ('peso_social', '0.30'),
            ('peso_governanca', '0.35'),
        ]
        for chave, valor in configuracoes_iniciais:
            cur.execute(
                """INSERT INTO configuracoes (chave, valor)
                   VALUES (%s, %s)
                   ON CONFLICT (chave) DO NOTHING""",
                (chave, valor)
            )
            
        for seed in SEED:
            print(f"Executando seed: {seed[:50]}...")
            logger.info(f"Executando seed: {seed[:50]}...")
            cur.execute(seed)
            
        cur.close()
