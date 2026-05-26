# config.py
# ══════════════════════════════════════════════════════════════════
# Configurações e constantes compartilhadas por todos os módulos
# Edenred Brasil | CESAR School 2025
# ══════════════════════════════════════════════════════════════════

import os
import warnings
import numpy as np

warnings.filterwarnings("ignore")
np.random.seed(42)

# ── Caminhos ──────────────────────────────────────────────────────
CAMINHO_DADOS = "./data/raw/data.csv"
PASTA_BRONZE  = "./data/bronze"
PASTA_SAIDA   = "./data/processado"
PASTA_MODELOS = "./modelos"

os.makedirs(PASTA_BRONZE,  exist_ok=True)
os.makedirs(PASTA_SAIDA,   exist_ok=True)
os.makedirs(PASTA_MODELOS, exist_ok=True)

# ── Colunas ───────────────────────────────────────────────────────
COLUNAS_REMOVER = [
    'ticker', 'logo', 'weburl', 'last_processing_date',
    'cik', 'currency', 'exchange'
]

FEATURES_SCORES  = ['environment_score', 'social_score', 'governance_score']
FEATURE_INDUSTRY = 'industry'
TARGET           = 'total_level'   # 'High' ou 'Medium'

# ── Maturidade ────────────────────────────────────────────────────
MAPA_MATURIDADE = {'High': 'Avançado', 'Medium': 'Iniciante'}

# ── Pesos por indústria ───────────────────────────────────────────
# Setores com menos empresas que esse limiar recebem pesos globais
MIN_EMPRESAS_PESO = 5

# ── Normalização de nomes de indústria ────────────────────────────
# Mesmo setor com variações textuais → nome canônico único
NOMES_CANONICOS = {
    'Aerospace & Defense':           'Aerospace and Defense',
    'Hotels, Restaurants & Leisure': 'Hotels Restaurants and Leisure',
    'Metals & Mining':               'Metals and Mining',
}
