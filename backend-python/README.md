# ESG Nexus Backend - Python FastAPI + NeonDB PostgreSQL

Backend do ESG Nexus usando **FastAPI** e **PostgreSQL no NeonDB**.

## Tecnologias

- Python 3
- FastAPI
- Uvicorn
- PostgreSQL / NeonDB
- psycopg2
- Pandas / Scikit-learn para evolução futura de ML

## Configuração do NeonDB

1. Crie um projeto no NeonDB.
2. Copie a string de conexão PostgreSQL.
3. Crie o arquivo `.env`:

```bash
cp .env.example .env
```

4. Edite a variável `DATABASE_URL`:

```env
DATABASE_URL=postgresql://usuario:senha@ep-sua-instancia.us-east-2.aws.neon.tech/esg_nexus?sslmode=require
```

> Importante: mantenha `sslmode=require`, pois o NeonDB usa conexão SSL.

## Executar localmente

```bash
chmod +x *.sh
./instalar_e_executar.sh
```

Ou manualmente:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

## Documentação da API

```text
http://localhost:8080/docs
```

## Credenciais iniciais

- e-mail: `admin@esgnexus.com`
- senha: `admin123`

## Endpoints principais

- `POST /api/auth/login`
- `GET /api/auth/me`
- `GET /api/fornecedores`
- `POST /api/fornecedores`
- `GET /api/fornecedores/{id}`
- `PUT /api/fornecedores/{id}`
- `DELETE /api/fornecedores/{id}`
- `POST /api/avaliacoes`
- `GET /api/ranking`
- `GET /api/dashboard`
- `GET /api/certificacoes`
- `GET /api/alertas`
- `GET /api/configuracoes`
- `POST /api/ml/prever-score`

## Observações

- O schema é criado automaticamente na inicialização da API.
- O usuário administrador inicial também é criado automaticamente.
- Esta versão não sobe banco local via Docker Compose, pois usa NeonDB como banco externo.
