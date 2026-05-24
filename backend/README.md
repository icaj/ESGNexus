# ESG Nexus Backend - FastAPI + ML + NeonDB

Backend Python para cadastro de fornecedores ESG, ranking, dashboards e previsao de score usando machine learning.

## Stack

- Python 3.12+
- FastAPI
- PostgreSQL / NeonDB
- Pandas
- Scikit-learn
- Uvicorn

## Configuracao

```bash
cp .env.example .env
```

Edite `DATABASE_URL` com sua string do NeonDB:

```env
DATABASE_URL=postgresql://usuario:senha@ep-instancia.neon.tech/esg_nexus?sslmode=require
```

## Instalar e executar

```bash
chmod +x *.sh
./instalar_e_executar.sh
```

API:

```text
http://localhost:8080/docs
```

Usuario inicial:

```text
admin@esgnexus.com
admin123
```
