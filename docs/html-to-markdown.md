  ESG Nexus Enterprise — Documentação de Arquitetura :root { --bg: #0f1117; --surface: #1a1d2e; --surface2: #232640; --border: #2e3254; --accent: #4f8ef7; --accent2: #7c5cbf; --green: #2ecc71; --orange: #e67e22; --red: #e74c3c; --teal: #1abc9c; --yellow: #f1c40f; --text: #e8eaf6; --text2: #9ea8d8; --text3: #5c6494; } \* { box-sizing: border-box; margin: 0; padding: 0; } body { background: var(--bg); color: var(--text); font-family: 'Segoe UI', system-ui, sans-serif; line-height: 1.6; } /\* ── Layout ── \*/ .wrapper { max-width: 1400px; margin: 0 auto; padding: 32px 24px; } header { border-bottom: 1px solid var(--border); padding-bottom: 24px; margin-bottom: 40px; } header h1 { font-size: 2rem; font-weight: 700; color: var(--accent); } header .subtitle { color: var(--text2); margin-top: 4px; font-size: 1rem; } header .meta { display: flex; gap: 20px; margin-top: 16px; flex-wrap: wrap; } header .badge { background: var(--surface2); border: 1px solid var(--border); border-radius: 20px; padding: 4px 14px; font-size: 0.78rem; color: var(--text2); } header .badge span { color: var(--accent); font-weight: 600; } section { margin-bottom: 56px; } h2 { font-size: 1.35rem; color: var(--text); border-left: 3px solid var(--accent); padding-left: 12px; margin-bottom: 20px; } h3 { font-size: 1.05rem; color: var(--accent); margin-bottom: 10px; margin-top: 18px; } p { color: var(--text2); margin-bottom: 10px; } /\* ── Diagram ── \*/ .diagram-container { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 28px; overflow-x: auto; } svg text { font-family: 'Segoe UI', system-ui, sans-serif; } /\* ── Modules grid ── \*/ .modules-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 20px; } .module-card { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 20px; transition: border-color 0.2s; } .module-card:hover { border-color: var(--accent); } .module-card .header { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; } .module-card .icon { width: 36px; height: 36px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; flex-shrink: 0; } .module-card .title { font-weight: 600; font-size: 1rem; } .module-card .port { font-size: 0.72rem; color: var(--text3); background: var(--surface2); padding: 2px 8px; border-radius: 10px; margin-left: auto; } .module-card p { font-size: 0.86rem; } .file-list { margin-top: 10px; } .file-item { font-size: 0.78rem; color: var(--text3); padding: 3px 0; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; } .file-item:last-child { border-bottom: none; } .file-item .fname { font-family: monospace; color: var(--text2); } .file-item .fdesc { color: var(--text3); font-size: 0.72rem; } /\* ── API table ── \*/ .api-table { width: 100%; border-collapse: collapse; font-size: 0.86rem; } .api-table th { background: var(--surface2); color: var(--text2); text-align: left; padding: 10px 14px; font-weight: 600; border-bottom: 2px solid var(--border); } .api-table td { padding: 9px 14px; border-bottom: 1px solid var(--border); vertical-align: top; } .api-table tr:hover td { background: var(--surface2); } .method { display: inline-block; padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: 0.75rem; min-width: 48px; text-align: center; } .get { background: #1a3a5c; color: #4f8ef7; } .post { background: #1a3a2a; color: #2ecc71; } .endpoint { font-family: monospace; color: var(--accent); } .auth-badge { font-size: 0.7rem; padding: 2px 7px; border-radius: 10px; } .auth-public { background: #2a1a0a; color: #e67e22; } .auth-user { background: #1a2a3a; color: #4f8ef7; } .auth-admin { background: #2a1a2a; color: #9b59b6; } /\* ── DB table ── \*/ .db-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 18px; } .db-table-card { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; overflow: hidden; } .db-table-card .thead { background: var(--surface2); padding: 10px 14px; font-weight: 600; font-size: 0.9rem; color: var(--teal); border-bottom: 1px solid var(--border); display: flex; align-items: center; gap: 8px; } .db-col { font-size: 0.78rem; padding: 6px 14px; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; } .db-col:last-child { border-bottom: none; } .db-col .cname { font-family: monospace; color: var(--text2); } .db-col .ctype { color: var(--text3); font-size: 0.72rem; } .pk { color: var(--yellow) !important; } /\* ── Flow ── \*/ .flow-steps { display: flex; flex-direction: column; gap: 12px; } .flow-row { display: flex; align-items: flex-start; gap: 14px; } .flow-num { width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.8rem; flex-shrink: 0; margin-top: 2px; } .flow-content { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 12px 16px; flex: 1; } .flow-content strong { color: var(--text); font-size: 0.9rem; } .flow-content p { font-size: 0.82rem; margin: 4px 0 0; } /\* ── ML section ── \*/ .ml-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; } @media (max-width: 700px) { .ml-grid { grid-template-columns: 1fr; } } .ml-card { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 18px; } .ml-card h4 { color: var(--accent2); margin-bottom: 10px; } .phase-list { display: flex; flex-direction: column; gap: 6px; } .phase { display: flex; gap: 10px; align-items: flex-start; font-size: 0.83rem; } .phase-num { background: var(--accent2); color: white; border-radius: 4px; padding: 1px 7px; font-weight: 700; font-size: 0.72rem; flex-shrink: 0; margin-top: 2px; } .phase-text { color: var(--text2); } /\* ── Tech stack ── \*/ .stack-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 12px; } .stack-item { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 12px 14px; display: flex; align-items: center; gap: 10px; } .stack-item .si-icon { font-size: 1.3rem; } .stack-item .si-info .si-name { font-size: 0.88rem; font-weight: 600; color: var(--text); } .stack-item .si-info .si-ver { font-size: 0.72rem; color: var(--text3); } /\* ── Hexagonal highlight ── \*/ .hex-note { background: var(--surface); border: 1px solid var(--accent2); border-radius: 8px; padding: 14px 18px; color: var(--text2); font-size: 0.86rem; margin-bottom: 16px; } .hex-note strong { color: var(--accent2); } /\* ── Scroll to top ── \*/ .toc { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 16px 20px; margin-bottom: 32px; } .toc h4 { color: var(--text2); font-size: 0.85rem; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 0.05em; } .toc-links { display: flex; flex-wrap: wrap; gap: 8px; } .toc-links a { color: var(--accent); font-size: 0.83rem; text-decoration: none; padding: 4px 10px; border: 1px solid var(--border); border-radius: 4px; } .toc-links a:hover { border-color: var(--accent); }

ESG Nexus Enterprise
====================

Documentação de Arquitetura de Software — Classificação ESG de Fornecedores com Machine Learning

Versão 1.0.0-merged Python ≥ 3.11 Arquitetura Hexagonal (Ports & Adapters) Pipeline CRISP-DM Data Junho 2026

#### Índice

[Diagrama de Arquitetura](#diagrama) [Visão Geral](#visao-geral) [Módulos de Software](#modulos) [Arquitetura Hexagonal](#hexagonal) [API REST — Endpoints](#api) [Banco de Dados](#banco) [Pipeline de ML](#ml) [Fluxos Principais](#fluxos) [Infraestrutura & Deploy](#infra) [Stack Tecnológico](#stack)

Diagrama de Arquitetura
-----------------------

USUÁRIO / BROWSER Navegador Web KAGGLE (Externo) ESG Ratings Dataset KaggleHub API FRONTEND Streamlit · Porta 8501 app.py UI Streamlit — Dashboards / Formulários cliente\_api.py HTTP Client (requests) → API :8000 BACKEND — FastAPI Uvicorn ASGI · Porta 8000 interfaces/api/principal.py FastAPI app · CORS · startup (criar\_tabelas) rotas\_auth.py /auth/registrar /auth/login · /auth/me dependencias\_auth.py obter\_usuario\_atual exigir\_perfil rotas\_enterprise.py POST /treinar · POST /classificar POST /classificar/lote · POST /avaliar/upload GET /fornecedores · GET /dashboard/executivo GET /dashboard/ml esquemas.py FornecedorEntrada AvaliacaoSaida · Lote esquemas\_auth.py UsuarioCriacao · LoginEntrada TokenSaida · UsuarioSaida 🔐 seguranca.py — JWT (HS256 · bcrypt) · 480 min 📋 registro\_log.py — structlog JSON ⚙️ configuracoes.py — pydantic-settings / .env CORE — esg\_ml (Arquitetura Hexagonal) Ports & Adapters · Zero dependência de infra no domínio DOMÍNIO (Núcleo Puro) entidades/ empresa.py — Empresa, ScoreESG PesosSetor, Maturidade, Quadrante PLANOS\_ACAO (E/S/G) diagnostico.py — DiagnosticoESG (23 campos) ItemPlanoAcao portas/portas.py RepositorioModelos, RepositorioDados RepositorioEmpresas (ABCs) servicos/ (domain services) preprocessamento.py — limpeza/validação feature\_engineering.py — pesos/scores treinamento.py — GridSearchCV KNN+RF predicao.py — diagnosticar() avaliacao.py — critérios Fase 5 APLICAÇÃO (Casos de Uso) servico\_treinamento.py CRISP-DM fases 2–6 · MLflow opcional servico\_avaliacao.py avaliar\_um() / avaliar() → DiagnosticoESG ADAPTADORES Entrada leitor\_kaggle.py KaggleHub → data.csv (Kaggle API) leitor\_fornecedores\_pandas.py CSV/XLSX → List\[Empresa\] Validação de colunas obrigatórias Saída repositorio\_modelo\_joblib.py salvar/carregar .joblib (knn · rf · config) csv\_resultado\_adapter.py Export DiagnosticoESG → CSV data/resultados/ MLFLOW Tracking Server · Porta 5000 Experiment Tracking Params · Metrics · Artifacts Model Registry KNN + Random Forest Backend Store: PostgreSQL · Artifacts: /mlflow/artifacts (volume) AIRFLOW Webserver :8080 · Scheduler dag\_treinamento\_esg Cron: 0 2 \* \* \* (diário 02:00) T1 verificar api → T2 treinar modelo → T3 gerar dashboards LocalExecutor · Tasks via cURL POST /treinar → API :8000 GET /saude · POST /dashboards/gerar BANCO DE DADOS PostgreSQL :5432 ou NeonDB (cloud) usuarios fornecedores avaliacoes\_esg experimentos\_ml MLflow metadata (backend-store) Airflow metadata (sql\_alchemy\_conn) ARTEFATOS DE MODELO (./artifacts/) modelo\_knn.joblib modelo\_rf.joblib config.joblib HTTPS REST API JWT Bearer calls SQLAlchemy opcional cURL POST metadata backend-store KaggleHub joblib.dump LEGENDA Chamada HTTP / REST Acesso a arquivo/API externa Integração opcional (MLflow) Airflow → API (cURL/cron) SQLAlchemy ORM Camadas Hexagonais Frontend / DB Backend FastAPI Core ML Hexagonal Airflow Scheduler MLflow Tracking Adaptadores / Artefatos Externo (Kaggle)

Visão Geral do Sistema
----------------------

O **ESG Nexus Enterprise** é uma plataforma de classificação de maturidade ESG (Environmental, Social & Governance) de fornecedores. Combina Machine Learning supervisionado com uma API REST segura, dashboard interativo e orquestração automática de retreinamento.

A lógica de negócio é estruturada em **Arquitetura Hexagonal (Ports & Adapters)** dentro do pacote `esg_ml/`, garantindo que o núcleo de domínio seja completamente independente de banco de dados, frameworks e APIs externas. O pipeline de ML segue as fases do **CRISP-DM**.

**Decisão arquitetural central:** todo código de infraestrutura (SQLAlchemy, joblib, Kaggle, requests) fica nas camadas externas (adaptadores e infraestrutura). O domínio só conhece entidades e serviços expressos em Python puro — sem imports de bibliotecas externas.

Módulos de Software
-------------------

🖥

Frontend — Streamlit :8501

Interface web interativa construída com Streamlit. Permite login, cadastro de fornecedores, classificação individual e em lote, upload de CSV/XLSX e visualização de dashboards executivos e de ML.

frontend/app.pyUI completa — páginas, formulários, gráficos Plotly

frontend/cliente\_api.pyHTTP client com requests; gerencia token JWT

.streamlit/config.tomlTema e configurações de servidor

⚡

Backend — FastAPI :8000

API REST assíncrona servida por Uvicorn. Responsável por autenticação JWT, orquestração dos casos de uso de ML e persistência no banco. CORS configurado para o Streamlit.

interfaces/api/principal.pyApp FastAPI, CORS, startup

interfaces/api/rotas\_enterprise.pyClassificação, treino, dashboards, fornecedores

interfaces/api/rotas\_auth.pyRegistro, login, /me

interfaces/api/esquemas\*.pyPydantic v2 — validação de entrada/saída

interfaces/api/dependencias\_auth.pyDependências FastAPI de autenticação/autorização

💎

Domínio (Núcleo Puro)

Núcleo da arquitetura hexagonal. Contém todas as regras de negócio ESG expressas em Python puro, sem dependências externas. Imutável, testável e independente de infraestrutura.

dominio/entidades/empresa.pyEmpresa, ScoreESG, PesosSetor, Maturidade, Quadrante

dominio/entidades/diagnostico.pyDiagnosticoESG (23 campos), ItemPlanoAcao

dominio/servicos/treinamento.pyGridSearchCV KNN (k 3–21) + RF (24 combos)

dominio/servicos/predicao.pydiagnosticar() — puro, sem I/O

dominio/servicos/feature\_engineering.pyPesos por setor, score ponderado, risco/impacto

dominio/servicos/preprocessamento.pyLimpeza e validação dos dados brutos

dominio/portas/portas.pyABCs: RepositorioModelos, RepositorioDados

🎯

Aplicação (Casos de Uso)

Orquestra o domínio, adaptadores e infraestrutura para implementar os dois casos de uso principais: treinar modelos (CRISP-DM) e avaliar fornecedores.

aplicacao/servico\_treinamento.pyCRISP-DM fases 2–6 + MLflow opcional + gráficos

aplicacao/servico\_avaliacao.pyCarrega artefatos e chama predicao.diagnosticar()

🔌

Adaptadores

Implementações concretas das portas definidas no domínio. Fazem a ponte entre o núcleo puro e o mundo externo (Kaggle, sistema de arquivos, CSV/XLSX).

adaptadores/entrada/leitor\_kaggle.pyKaggleHub download → DataFrame

adaptadores/entrada/leitor\_fornecedores\_pandas.pyCSV/XLSX → List\[Empresa\] com validação

adaptadores/saida/repositorio\_modelo\_joblib.pyPersistência de modelos em .joblib

adaptadores/saida/csv\_resultado\_adapter.pyExport DiagnosticoESG → CSV

🏗

Infraestrutura

Serviços técnicos transversais: conexão ao banco, ORM, segurança JWT/bcrypt, logging estruturado e configurações via variáveis de ambiente.

infraestrutura/banco\_dados.pySQLAlchemy engine, pool, sessão, Base declarativa

infraestrutura/modelos\_banco.pyORM: UsuarioBanco, FornecedorBanco, AvaliacaoBanco, ExperimentoMLBanco

infraestrutura/seguranca.pybcrypt (hash/verify), JWT HS256 (criar/decodificar)

infraestrutura/configuracoes.pypydantic-settings, lê .env com override

infraestrutura/registro\_log.pystructlog JSON, timestamps UTC

infraestrutura/inicializacao\_banco.pyCriação de tabelas e seed inicial

⏰

Apache Airflow :8080

Orquestrador de workflow que executa o pipeline de retreinamento automaticamente às 02:00 todo dia. Conecta-se à API via HTTP (cURL). Usa o mesmo PostgreSQL como backend.

airflow/dags/dag\_treinamento\_esg.pyDAG com 3 tasks: verificar\_api → treinar\_modelo → gerar\_dashboards

airflow-webserverUI de monitoramento das execuções (porta 8080)

airflow-schedulerDispara tasks no horário configurado

airflow-initMigra schema e cria usuário admin

📊

MLflow Tracking :5000

Servidor de rastreamento de experimentos ML. Registra hiperparâmetros, métricas e artefatos de cada execução de treino (opcional — ativado via flag `usar_mlflow=True`).

Experimento: esg-nexus-fornecedoresRuns: KNN\_GridSearch, RandomForest\_GridSearch

Params logadosn\_neighbors, n\_estimators, max\_depth, min\_samples\_leaf

Metrics logadasaccuracy, f1\_medium (KNN e RF)

Artifacts logadosanalise\_exploratoria.png, avaliacao\_modelos.png, modelo .pkl

Backend storePostgreSQL (mesma instância)

🗄

Banco de Dados :5432

PostgreSQL local (Docker) ou NeonDB serverless (cloud) configurado via variável `DATABASE_URL`. Compartilhado entre API, MLflow e Airflow. SQLAlchemy gerencia o pool de conexões.

usuariosAutenticação — email, senha\_hash (bcrypt), perfil, ativo

fornecedoresCadastro — name, industry, scores E/S/G

avaliacoes\_esg23 campos do DiagnosticoESG — resultado completo de cada classificação

experimentos\_mlHistórico de treinos — acurácias, parâmetros, mlflow\_run\_id

Arquitetura Hexagonal (Ports & Adapters)
----------------------------------------

**Princípio:** dependências sempre apontam do exterior para o interior. O domínio não importa nada do mundo externo. Cada porta (interface abstrata) é implementada por um adaptador concreto.

### ① Domínio

Entidades, regras de negócio e interfaces (portas). Não importa SQLAlchemy, FastAPI, pandas ou qualquer framework.

Depende de: Python stdlib

### ② Aplicação

Casos de uso que orquestram o domínio. Depende do domínio e das portas, mas não de adaptadores concretos diretamente.

Depende de: domínio, portas

### ③ Adaptadores / Infra

Implementações concretas das portas. FastAPI, SQLAlchemy, joblib, KaggleHub, Streamlit. Dependem do domínio e da aplicação.

Depende de: todas as camadas internas

API REST — Catálogo de Endpoints
--------------------------------

Método

Endpoint

Acesso

Descrição

GET

/saude

público

Health check — verifica modelos carregados

POST

/auth/registrar

público

Cria novo usuário (nome, email, senha, perfil)

POST

/auth/login

público

Autentica e retorna access\_token JWT + dados do usuário

GET

/auth/me

autenticado

Retorna dados do usuário logado

POST

/treinar

admin / cientista

Executa pipeline CRISP-DM completo — baixa dados Kaggle, treina KNN+RF, salva artefatos

POST

/classificar

autenticado

Classifica um fornecedor — retorna DiagnosticoESG (23 campos) e persiste no banco

POST

/classificar/lote

autenticado

Classifica lista de fornecedores em lote com rastreamento de erros por linha

POST

/avaliar/upload

autenticado

Upload CSV/XLSX — classifica todas as empresas do arquivo

GET

/fornecedores

autenticado

Lista todos os fornecedores cadastrados (ordenados por nome)

GET

/dashboard/executivo

autenticado

KPIs agregados: total, score médio, distribuição de maturidade, top risco, melhores

GET

/dashboard/ml

admin / cientista

Métricas de ML: dispersão, distribuição de confiança, concordância KNN vs RF

Perfis disponíveis: `administrador`, `cientista_dados`, `analista_esg` (padrão). Token JWT válido por 480 minutos.

Banco de Dados — Modelo de Dados
--------------------------------

PostgreSQL 16 (Docker) ou NeonDB serverless. Utilizado por três componentes: API (ORM SQLAlchemy), MLflow (backend-store) e Airflow (metadados de execução). Banco: `esg_nexus`.

🔐 usuarios

idInteger PK

nomeString(120)

emailString(180) unique idx

senha\_hashString(255) bcrypt

perfilString(30) default analista\_esg

ativoBoolean default True

criado\_emDateTime UTC

🏢 fornecedores

idInteger PK

nameString(220) idx

industryString(100)

environment\_scoreInteger 0–1000

social\_scoreInteger 0–1000

governance\_scoreInteger 0–1000

criado\_emDateTime UTC

📋 avaliacoes\_esg

idInteger PK

name, industryidentificação

environment/social/governance\_scoreInteger

total\_score, score\_ponderadoInteger / Float

grade, levelString (A–F, High/Medium)

w\_E, w\_S, w\_G, fonte\_pesosFloat / String

risco, impacto, quadranteFloat / String

maturidade\_rf, confianca\_rf\_\*String / Float

maturidade\_knn, confianca\_knn\_\*String / Float

acoes\_recomendadasText

criado\_emDateTime UTC

🧪 experimentos\_ml

idInteger PK

nome\_execucaoString(120)

knn\_acuracia, knn\_f1\_mediumFloat

rf\_acuracia, rf\_f1\_mediumFloat

knn\_params, rf\_paramsText JSON

mlflow\_run\_idString(120) nullable

criado\_emDateTime UTC

Pipeline de Machine Learning (CRISP-DM)
---------------------------------------

O modelo classifica fornecedores em dois níveis de maturidade ESG: **Avançado** (High) e **Iniciante** (Medium). Dois algoritmos são treinados e comparados a cada execução.

#### Fases CRISP-DM

F1**Entendimento do Negócio** — Vocabulário ESG definido em empresa.py: ScoreESG (0–1000/pilar), Quadrante, Maturidade, Planos de Ação

F2**Entendimento dos Dados** — Carregamento via KaggleHub (dataset: `alistairking/public-company-esg-ratings-dataset`). Raw salvo em data/raw/data.csv

F3**Preparação dos Dados** — preprocessamento.py + feature\_engineering.py. Pesos por setor calculados estatisticamente. Base bronze salva em data/bronze/

F4**Modelagem** — KNN: GridSearch k=3..21 ímpares + StandardScaler. RF: 24 combinações (n\_estimators × max\_depth × min\_samples\_leaf). StratifiedKFold 5 splits

F5**Avaliação** — Critérios: acurácia ≥ 93%, F1-Medium ≥ 88%. Falha dispara ModeloInsuficienteError e interrompe o deploy

F6**Implantação** — Modelos aprovados salvos em artifacts/. MLflow registra runs opcionalmente. Gráficos de avaliação exportados

#### Features e Saídas

**Features (4):**

environment\_score social\_score governance\_score industry\_enc

**Target:** `total_level` — High / Medium

**Saídas do DiagnosticoESG:**

Maturidade RF (principal) + confiança, Maturidade KNN (benchmark) + confiança, score ponderado por setor, grade (A–F), risco %, impacto %, quadrante (Matriz 2×2), plano de ação (até 3 ações por pilar abaixo do limiar 400)

**Artefatos gerados:**

artifacts/modelo\_knn.joblib, artifacts/modelo\_rf.joblib, artifacts/config.joblib (LabelEncoders + benchmark + pesos)

Fluxos Principais
-----------------

### ① Fluxo de Autenticação

1

**Frontend → POST /auth/login**

Envia email + senha. rotas\_auth.py consulta UsuarioBanco, verifica hash bcrypt via seguranca.py

2

**Backend → JWT HS256**

Cria token com payload {sub: email, perfil, exp: +480min}. Retorna TokenSaida com access\_token e dados do usuário

3

**Frontend → Bearer Token**

Armazena token na session do Streamlit. Inclui Authorization: Bearer {token} em todas as chamadas subsequentes

### ② Fluxo de Classificação Individual

1

**Frontend → POST /classificar**

Envia FornecedorEntrada {name, industry, environment\_score, social\_score, governance\_score}

2

**API → ServicoAvaliacao.avaliar\_um()**

Carrega modelo\_knn.joblib, modelo\_rf.joblib e config.joblib via RepositorioModeloJoblib

3

**Domínio → predicao.diagnosticar()**

Calcula pesos por setor, score ponderado, risco, impacto, quadrante. Chama KNN + RF, gera plano de ação para pilares abaixo do limiar 400

4

**API → Persistência**

Persiste FornecedorBanco (upsert por name) e AvaliacaoBanco (23 campos) no PostgreSQL via SQLAlchemy

5

**Frontend ← AvaliacaoSaida**

Exibe DiagnosticoESG: maturidade, grade, quadrante, confiança dos modelos, plano de ação

### ③ Fluxo de Treinamento Automático (Airflow)

1

**Airflow Scheduler → 02:00 diário**

Dispara dag\_treinamento\_esg. Task 1: curl GET /saude — verifica disponibilidade da API

2

**Task 2 → POST /treinar**

API invoca ServicoTreinamento.treinar(). CRISP-DM fases 2–6: KaggleHub download → preprocessamento → GridSearchCV → avaliação → salva .joblib

3

**MLflow (opcional) → Registro**

Se usar\_mlflow=True: registra runs KNN e RF com params, métricas e gráficos de análise exploratória e avaliação

4

**Task 3 → POST /dashboards/gerar**

Regenera dashboards HTML com os dados mais recentes do banco

Infraestrutura & Deploy
-----------------------

O sistema é totalmente containerizado via Docker Compose com 7 serviços. Todos compartilham a mesma instância PostgreSQL. Em produção, o PostgreSQL pode ser substituído pelo NeonDB serverless alterando apenas a variável `DATABASE_URL`.

Portas expostas

`:8501` → Streamlit (frontend) `:8000` → FastAPI (backend) `:5000` → MLflow UI `:8080` → Airflow Webserver `:5432` → PostgreSQL

Volumes persistentes

`postgres_data` → dados PostgreSQL `mlflow_artifacts` → artefatos MLflow `./artifacts` → modelos .joblib (bind mount) `./data` → datasets CSV/processados `./airflow/dags` → DAGs Airflow

Variáveis de ambiente chave

`DATABASE_URL` — PostgreSQL ou NeonDB `MLFLOW_TRACKING_URI` — http://mlflow:5000 `SEGREDO_JWT` — chave HMAC-SHA256 `ESG_NEXUS_API_URL` — usada pelo Airflow e Streamlit `MLFLOW_EXPERIMENTO` — esg-nexus-fornecedores

Scripts de inicialização

`inicializar_banco.py` — cria tabelas via SQLAlchemy `treinar_modelo.py` — executa pipeline CRISP-DM manual `iniciar_backend.py` — inicia Uvicorn dev `scripts_inicializar_banco_linux.sh` `scripts_inicializar_banco_windows.bat`

Stack Tecnológico
-----------------

⚡

FastAPI

≥ 0.110 — ASGI, Pydantic v2

🖥

Streamlit

≥ 1.36 — frontend web

🗄

PostgreSQL 16

\+ NeonDB serverless

🔗

SQLAlchemy 2.0

ORM + psycopg3

🤖

scikit-learn

≥ 1.4 — KNN + RF + GridSearchCV

🐼

pandas

≥ 2.2 — processamento de dados

📊

MLflow

≥ 2.12 — experiment tracking

⏰

Apache Airflow

2.9.3 — orchestration

💾

joblib

≥ 1.4 — persistência de modelos

🔐

JWT + bcrypt

python-jose + bcrypt

📋

structlog

≥ 24.1 — logging JSON

📦

Docker Compose

7 serviços containerizados

📈

Plotly

≥ 5.22 — gráficos interativos

🌐

KaggleHub

≥ 0.2 — download de dataset

⚙️

pydantic-settings

≥ 2.2 — configurações

🚀

Uvicorn

≥ 0.29 — ASGI server

ESG Nexus Enterprise v1.0.0-merged — Arquitetura Hexagonal + CRISP-DM Gerado em Junho 2026