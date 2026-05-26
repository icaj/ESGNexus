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


## Treinamento ML com base Kaggle

Esta versão inclui um pipeline de treinamento baseado nos scripts `app/ml_pipeline/*`.

Endpoints:

- `POST /api/ml/treinar-kaggle` — inicia o treinamento em segundo plano.
- `POST /api/ml/treinar-kaggle?force=true` — força novo treinamento.
- `GET /api/ml/treinamento-status` — consulta status, log e artefatos gerados.

Artefatos gerados:

- `modelos/modelo_knn.pkl`
- `modelos/modelo_rf.pkl`
- `modelos/config.pkl`
- `data/bronze/base_processada.csv`
- `data/bronze/pesos_por_industria.csv`
- `data/processado/analise_exploratoria.png`
- `data/processado/avaliacao_modelos.png`

Observação: o download do dataset usa KaggleHub e precisa de acesso à internet. Para datasets privados, configure suas credenciais Kaggle no ambiente.
