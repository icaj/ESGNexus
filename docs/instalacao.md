# Guia de Instalação — ESG Nexus Enterprise

Este guia cobre a instalação de todos os módulos da aplicação: **Backend (FastAPI)**, **Frontend (Streamlit)**, **PostgreSQL**, **MLflow** e **Apache Airflow**.

---

## Pré-requisitos

| Ferramenta | Versão mínima | Verificar |
|---|---|---|
| Python | 3.11 | `python --version` |
| Docker | 24+ | `docker --version` |
| Docker Compose | 2.x | `docker compose version` |
| Git | qualquer | `git --version` |

---

## Opção 1 — Docker Compose (recomendado)

Sobe todos os serviços de uma vez: PostgreSQL, API, Streamlit, MLflow, Airflow.

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/ESGNexus.git
cd ESGNexus

# Suba todos os serviços
docker compose up --build -d

# Acompanhe os logs
docker compose logs -f
```

### Serviços e portas

| Serviço | URL | Credenciais padrão |
|---|---|---|
| API (FastAPI) | http://localhost:8000 | — |
| Docs interativos | http://localhost:8000/docs | — |
| Frontend (Streamlit) | http://localhost:8501 | — |
| MLflow UI | http://localhost:5000 | — |
| Airflow UI | http://localhost:8080 | admin / admin |
| PostgreSQL | localhost:5432 | esg / esg |

### Parar os serviços

```bash
docker compose down          # para e remove os containers
docker compose down -v       # também remove os volumes (dados)
```

---

## Opção 2 — Instalação local (desenvolvimento)

### 1. Backend (FastAPI)

```bash
# Crie e ative o ambiente virtual
python -m venv .venv

# Linux/macOS
source .venv/bin/activate
# Windows
.venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt
# ou via pyproject.toml
pip install -e .

# Configure as variáveis de ambiente
cp .env.example .env   # edite conforme necessário
```

Variáveis obrigatórias no `.env`:

```env
DATABASE_URL=postgresql+psycopg://esg:esg@localhost:5432/esg_nexus
MLFLOW_TRACKING_URI=http://localhost:5000
SEGREDO_JWT=altere-este-segredo-em-producao
```

Inicie o servidor:

```bash
uvicorn esg_ml.interfaces.api.principal:app --reload --host 0.0.0.0 --port 8000
```

---

### 2. Frontend (Streamlit)

O frontend usa o mesmo ambiente virtual do backend.

```bash
# Com o .venv ativado
streamlit run frontend_streamlit/app.py --server.port 8501
```

Ou, se estiver usando a pasta `frontend/frontend`:

```bash
streamlit run frontend/frontend/app.py --server.port 8501
```

Variável de ambiente necessária:

```env
ESG_NEXUS_API_URL=http://localhost:8000
```

---

### 3. PostgreSQL

**Via Docker (mais simples):**

```bash
docker run -d \
  --name esg-postgres \
  -e POSTGRES_DB=esg_nexus \
  -e POSTGRES_USER=esg \
  -e POSTGRES_PASSWORD=esg \
  -p 5432:5432 \
  postgres:16-alpine
```

**Instalação nativa:** siga o guia oficial em https://www.postgresql.org/download/ e crie o banco manualmente:

```sql
CREATE DATABASE esg_nexus;
CREATE USER esg WITH PASSWORD 'esg';
GRANT ALL PRIVILEGES ON DATABASE esg_nexus TO esg;
```

---

### 4. MLflow

```bash
# Com o .venv ativado (mlflow já está em requirements.txt)
mlflow ui \
  --host 0.0.0.0 \
  --port 5000 \
  --backend-store-uri postgresql+psycopg://esg:esg@localhost:5432/esg_nexus \
  --default-artifact-root ./artifacts
```

Acesse a UI em http://localhost:5000.

---

### 5. Apache Airflow

O Airflow **não está incluído** em `requirements.txt` por ser pesado e ter dependências próprias. Instale-o em um ambiente separado.

```bash
# Crie um ambiente virtual exclusivo para o Airflow
python -m venv .venv-airflow
source .venv-airflow/bin/activate   # Linux/macOS
# .venv-airflow\Scripts\activate    # Windows

# Defina a versão e instale
AIRFLOW_VERSION=2.9.3
PYTHON_VERSION=3.11
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

# Configure o banco de dados
export AIRFLOW__CORE__EXECUTOR=LocalExecutor
export AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://esg:esg@localhost:5432/esg_nexus
export AIRFLOW__CORE__LOAD_EXAMPLES=False

# Inicialize o banco e crie o usuário admin
airflow db migrate
airflow users create \
  --username admin \
  --password admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com

# Aponte para a pasta de DAGs do projeto
export AIRFLOW__CORE__DAGS_FOLDER=$(pwd)/airflow/airflow/dags
```

Inicie o webserver e o scheduler (em terminais separados):

```bash
airflow webserver --port 8080
airflow scheduler
```

Acesse a UI em http://localhost:8080 (admin / admin).

---

## Ordem de inicialização recomendada (local)

```
1. PostgreSQL    → banco de dados disponível antes dos demais
2. MLflow        → registra experimentos usados pela API
3. Backend (API) → expõe endpoints consumidos pelo frontend e pelo Airflow
4. Frontend      → interface do usuário
5. Airflow       → orquestração de pipelines (opcional para desenvolvimento)
```

---

## Verificação rápida

```bash
# API health check
curl http://localhost:8000/health

# Docs interativos
open http://localhost:8000/docs        # macOS
start http://localhost:8000/docs       # Windows
```

---

## Solução de problemas comuns

| Problema | Causa provável | Solução |
|---|---|---|
| `connection refused` na porta 5432 | PostgreSQL não iniciou | Verifique `docker compose ps` ou `pg_isready` |
| `ModuleNotFoundError` | Dependências não instaladas | Rode `pip install -r requirements.txt` com o venv ativo |
| Airflow `DAG import error` | Módulos do projeto não no `PYTHONPATH` | Exporte `PYTHONPATH=$(pwd)` antes de iniciar o scheduler |
| MLflow `artifact location` vazio | Pasta `./artifacts` não existe | `mkdir artifacts` na raiz do projeto |
| Streamlit não conecta na API | `ESG_NEXUS_API_URL` errada | Confira a variável de ambiente apontando para `localhost:8000` |
