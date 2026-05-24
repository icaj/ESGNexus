# ESG Nexus Frontend - Streamlit

Frontend analitico em Python para exibir dashboards, ranking ESG, fornecedores, certificacoes, alertas e previsoes de score por machine learning.

## Stack

- Python 3.12+
- Streamlit
- Plotly
- Pandas
- Requests

## Configuracao

```bash
cp .env.example .env
```

Ajuste a URL do backend, se necessario:

```env
API_URL=http://localhost:8080
```

## Instalar e executar

```bash
chmod +x *.sh
./instalar_e_executar_frontend.sh
```

Acesse:

```text
http://localhost:8501
```

Usuario inicial:

```text
admin@esgnexus.com
admin123
```
