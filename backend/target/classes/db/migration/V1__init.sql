CREATE TABLE usuarios (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(180) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    perfil VARCHAR(30) NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE fornecedores (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    razao_social VARCHAR(180) NOT NULL,
    nome_fantasia VARCHAR(180),
    cnpj VARCHAR(30) NOT NULL UNIQUE,
    email VARCHAR(180),
    telefone VARCHAR(30),
    nome_contato VARCHAR(120),
    segmento VARCHAR(120),
    categoria VARCHAR(120),
    cidade VARCHAR(120),
    estado VARCHAR(120),
    pais VARCHAR(120),
    nivel_risco VARCHAR(50),
    status VARCHAR(30) NOT NULL DEFAULT 'ATIVO',
    data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE avaliacoes_fornecedor (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    fornecedor_id BIGINT NOT NULL,
    data_avaliacao DATE NOT NULL,
    nota_ambiental DECIMAL(10,2) NOT NULL,
    nota_social DECIMAL(10,2) NOT NULL,
    nota_governanca DECIMAL(10,2) NOT NULL,
    nota_final DECIMAL(10,2) NOT NULL,
    observacoes VARCHAR(1000),
    CONSTRAINT fk_avaliacao_fornecedor FOREIGN KEY (fornecedor_id) REFERENCES fornecedores(id)
);

CREATE TABLE certificacoes_fornecedor (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    fornecedor_id BIGINT NOT NULL,
    nome VARCHAR(180) NOT NULL,
    orgao_emissor VARCHAR(180),
    data_emissao DATE,
    data_validade DATE,
    status VARCHAR(30),
    url_arquivo VARCHAR(500),
    CONSTRAINT fk_certificacao_fornecedor FOREIGN KEY (fornecedor_id) REFERENCES fornecedores(id)
);

CREATE TABLE alertas (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    fornecedor_id BIGINT NOT NULL,
    tipo_alerta VARCHAR(80) NOT NULL,
    severidade VARCHAR(30) NOT NULL,
    titulo VARCHAR(180) NOT NULL,
    descricao VARCHAR(1000) NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'ABERTO',
    data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_alerta_fornecedor FOREIGN KEY (fornecedor_id) REFERENCES fornecedores(id)
);

CREATE TABLE configuracoes (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    chave VARCHAR(120) NOT NULL UNIQUE,
    valor VARCHAR(255) NOT NULL
);
