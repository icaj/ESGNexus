INSERT INTO usuarios (nome, email, senha_hash, perfil, ativo)
VALUES ('Administrador ESG', 'admin@esgnexus.com', '$2a$10$m8MQHRLe3Nveo2o2lz4jwe0yKk.Ks5PX3s4s1ux8WbOHB4buR2sQm', 'ADMIN', true);
-- senha padrão: admin123

INSERT INTO configuracoes (chave, valor) VALUES
('esg.peso.ambiental', '35'),
('esg.peso.social', '30'),
('esg.peso.governanca', '35');

INSERT INTO fornecedores (razao_social, nome_fantasia, cnpj, email, telefone, nome_contato, segmento, categoria, cidade, estado, pais, nivel_risco, status)
VALUES
('Fornecedor Verde Ltda', 'Fornecedor Verde', '11111111000101', 'contato@verde.com', '81999990001', 'Maria Silva', 'Industrial', 'Energia', 'Recife', 'PE', 'Brasil', 'BAIXO', 'ATIVO'),
('Eco Social Servicos SA', 'Eco Social', '22222222000102', 'contato@ecosocial.com', '81999990002', 'Joao Souza', 'Servicos', 'Facilities', 'Sao Paulo', 'SP', 'Brasil', 'MEDIO', 'ATIVO');

INSERT INTO avaliacoes_fornecedor (fornecedor_id, data_avaliacao, nota_ambiental, nota_social, nota_governanca, nota_final, observacoes)
VALUES
(1, '2026-04-10', 92, 88, 90, 90.10, 'Fornecedor com alto nivel de aderencia ESG'),
(2, '2026-04-12', 75, 82, 70, 75.35, 'Necessita fortalecer governanca');

INSERT INTO certificacoes_fornecedor (fornecedor_id, nome, orgao_emissor, data_emissao, data_validade, status, url_arquivo)
VALUES
(1, 'ISO 14001', 'ABNT', '2025-01-15', '2027-01-15', 'VALIDA', 'https://example.com/cert1.pdf'),
(2, 'ISO 45001', 'Bureau Veritas', '2024-08-01', '2026-08-01', 'VALIDA', 'https://example.com/cert2.pdf');

INSERT INTO alertas (fornecedor_id, tipo_alerta, severidade, titulo, descricao, status)
VALUES
(2, 'NOTA_GOVERNANCA_BAIXA', 'ALTA', 'Governanca abaixo da meta', 'Fornecedor com score de governanca abaixo da meta minima.', 'ABERTO');
