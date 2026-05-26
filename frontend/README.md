# ESG Nexus Frontend Streamlit - Visual Avancado

Esta versao preserva as rotas e funcionalidades do `app.py` original, mas adiciona:

- identidade visual profissional com CSS customizado
- tela de login mais elaborada
- cards executivos
- dashboard com gauge, histograma, boxplot, pizza, heatmap, correlacao, dispersao, funil e ranking
- pagina de ranking com estatisticas descritivas
- graficos adicionais para certificacoes, alertas e machine learning
- filtros por segmento, classificacao e risco

## Executar

```bash
pip install streamlit pandas plotly requests python-dotenv
streamlit run app.py
```

Configure a API no arquivo `.env`:

```env
API_URL=http://localhost:8080
```

## Treinamento do modelo ESG

Esta versão adiciona o menu **Treinamento do Modelo**.

O botão dispara no backend FastAPI o endpoint:

- `POST /api/ml/treinar-kaggle`
- `POST /api/ml/treinar-kaggle?force=true`
- `GET /api/ml/treinamento-status`

O pipeline baixa a base pública do Kaggle via KaggleHub, processa os dados, treina KNN e Random Forest e salva os artefatos em `modelos/` e `data/` no backend.
