# Modelo Conceitual de Banco de Dados
---

## Entidades

### 1. **FORNECEDOR**
Armazena informações principais sobre cada fornecedor.

**Atributos:**
- `id` (PRIMARY KEY): Identificador
- `nome`: Nome da empresa
- `receita_anual`: Receita anual em reais
- `numero_funcionarios`: Quantidade de funcionários
- `nivel_risco`: Enum (baixo, médio, alto)
- `status`: Enum (ativo, inativo, suspenso)
- `data_cadastro`: Data de cadastro no sistema
- `data_atualizacao`: Data da última atualização

**Relacionamentos:**
- N:1 com CATEGORIA
- 1:N com SCORE_ESG
- 1:N com AUDITORIA
- N:N com CERTIFICACAO (via FORNECEDOR_CERTIFICACAO)

---

### 2. **SCORE_ESG**
Registra histórico de pontuações ESG dos fornecedores.

**Atributos:**
- `id` (PRIMARY KEY): Identificador
- `score_total`: Score ESG total (0-100)
- `score_ambiental`: Score do pilar Ambiental (0-100)
- `score_social`: Score do pilar Social (0-100)
- `score_governanca`: Score do pilar Governança (0-100)
- `ranking_posicao`: Posição no ranking geral
- `data_avaliacao`: Data da avaliação
- `periodo_referencia`: Período de referência (mês/ano)
- `observacoes`: Texto com observações

**Relacionamentos:**
- N:1 com FORNECEDOR
- 1:N com CRITERIO_AVALIACAO

---

### 3. **CRITERIO_AVALIACAO** 
Detalha os critérios específicos avaliados em cada score.

**Atributos:**
- `id` (PRIMARY KEY): Identificador
- `pilar`: Enum (ambiental, social, governança)
- `nome_criterio`: Nome do critério (ex: "Emissões de Carbono", "Resíduos", "Diversidade", "Ética", "Conselho Fiscal", etc)
- `pontuacao`: Pontuação obtida (0-100)
- `peso`: Peso do critério na avaliação
- `evidencias`: Texto com evidências coletadas
- `recomendacoes`: Recomendações de melhoria

**Relacionamentos:**
- N:1 com SCORE_ESG

---

### 4. **AUDITORIA** 
Registra auditorias realizadas nos fornecedores.

**Atributos:**
- `id` (PRIMARY KEY): Identificador
- `data_realizada`: Data efetivamente realizada
- `status`: Enum (agendada, em andamento, concluída, cancelada)
- `resultado`: Enum (aprovado, aprovado com ressalvas, reprovado)
- `relatorio_url`: URL do relatório da auditoria
- `pontos_criticos`: Texto com pontos críticos identificados
- `prazo_correcao`: Data limite para correções
- `observacoes`: Observações gerais

**Relacionamentos:**
- N:1 com FORNECEDOR
- N:1 com USUARIO (auditor)
- 1:N com NAO_CONFORMIDADE

---

### 5. **NAO_CONFORMIDADE** 
Registra não conformidades identificadas em auditorias.

**Atributos:**
- `id` (PRIMARY KEY): Identificador 
- `pilar_esg`: Enum (ambiental, social, governança)
- `descricao`: Descrição da não conformidade
- `severidade`: Enum (baixa, média, alta, crítica)
- `status`: Enum (aberta, em correção, corrigida, não corrigida)
- `data_identificacao`: Data de identificação
- `prazo_correcao`: Prazo para correção
- `data_correcao`: Data efetiva da correção
- `evidencia_correcao`: URL ou descrição da evidência

**Relacionamentos:**
- N:1 com AUDITORIA

---

### 6. **CERTIFICACAO** 
Catálogo de certificações ESG disponíveis.

**Atributos:**
- `id` (PRIMARY KEY): Identificador
- `nome`: Nome da certificação (ex: "ISO 14001")
- `descricao`: Descrição da certificação
- `orgao_emissor`: Órgão que emite a certificação
- `tipo`: Enum (ambiental, social, governança, integrada)
- `validade_anos`: Período de validade em anos
- `logo_url`: URL do logo da certificação
- `status`: Enum (ativa, descontinuada)

**Relacionamentos:**
- N:N com FORNECEDOR (via FORNECEDOR_CERTIFICACAO)

---

### 7. **FORNECEDOR_CERTIFICACAO** 
Relacionamento entre fornecedores e suas certificações.

**Atributos:**
- `id` (PRIMARY KEY): Identificador
- `data_obtencao`: Data de obtenção da certificação
- `data_validade`: Data de validade da certificação
- `numero_certificado`: Número do certificado
- `status`: Enum (ativa, expirada, suspensa, renovando)
- `documento_url`: URL do documento da certificação

**Relacionamentos:**
- N:1 com FORNECEDOR
- N:1 com CERTIFICACAO

---

### 8. **CATEGORIA** 
Categorias de fornecedores.

**Atributos:**
- `id` (PRIMARY KEY): Identificador
- `nome`: Nome da categoria (ex: "Tecnologia")
- `descricao`: Descrição da categoria
- `score_medio`: Score ESG médio da categoria (calculado)
- `total_fornecedores`: Total de fornecedores (calculado)
- `icone`: Identificador do ícone

**Relacionamentos:**
- 1:N com FORNECEDOR

---

### 10. **USUARIO**
Usuários do sistema (analistas, auditores, administradores).

**Atributos:**
- `id` (PRIMARY KEY): Identificador
- `nome`: Nome completo
- `email`: Email (único)
- `senha_hash`: Hash da senha
- `cargo`: Cargo do usuário (ex: "Analista ESG")
- `tipo`: Enum (analista, auditor, gestor, administrador)
- `foto_url`: URL da foto de perfil
- `status`: Enum (ativo, inativo)
- `data_criacao`: Data de criação da conta
- `ultimo_acesso`: Data do último acesso

**Relacionamentos:**
- 1:N com SCORE_ESG (como avaliador)
- 1:N com AUDITORIA (como auditor)
- 1:N com NOTIFICACAO

---

### 11. **NOTIFICACAO** 
Notificações do sistema para os usuários.

**Atributos:**
- `id` (PRIMARY KEY): Identificador
- `tipo`: Enum (auditoria_vencida, score_baixo, certificacao_expirada, alerta_risco)
- `titulo`: Título da notificação
- `mensagem`: Mensagem detalhada
- `link`: Link relacionado (opcional)
- `lida`: Boolean (lida/não lida)
- `data_criacao`: Data de criação
- `data_leitura`: Data de leitura

**Relacionamentos:**
- N:1 com USUARIO

---

### 12. **HISTORICO_ALTERACAO**
Auditoria de alterações no sistema.

**Atributos:**
- `id` (PRIMARY KEY): Identificador
- `tabela`: Nome da tabela alterada
- `tipo_operacao`: Enum (insert, update, delete)
- `dados_anteriores`: JSON com dados anteriores
- `dados_novos`: JSON com dados novos
- `data_alteracao`: Data da alteração

**Relacionamentos:**
- N:1 com USUARIO

---

## Relacionamentos

```
USUARIO
  |
  |-- 1:N --> SCORE_ESG (avaliador)
  |-- 1:N --> AUDITORIA (auditor)
  |-- 1:N --> NOTIFICACAO
  |-- 1:N --> HISTORICO_ALTERACAO

FORNECEDOR
  |
  |-- 1:N --> SCORE_ESG
  |-- 1:N --> AUDITORIA
  |-- N:N --> CERTIFICACAO (via FORNECEDOR_CERTIFICACAO)
  |-- N:1 --> CATEGORIA

SCORE_ESG
  |
  |-- 1:N --> CRITERIO_AVALIACAO
  |-- N:1 --> FORNECEDOR

AUDITORIA
  |
  |-- 1:N --> NAO_CONFORMIDADE
  |-- N:1 --> FORNECEDOR
  |-- N:1 --> USUARIO (usuario auditor)

CERTIFICACAO
  |
  |-- N:N --> FORNECEDOR (via FORNECEDOR_CERTIFICACAO)

CATEGORIA
  |
  |-- 1:N --> FORNECEDOR

```

---

