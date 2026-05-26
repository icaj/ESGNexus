# etapa0_carga.py
# ══════════════════════════════════════════════════════════════════
# Etapa 0 — Download da base de dados do Kaggle
# Edenred Brasil | CESAR School 2025
# ══════════════════════════════════════════════════════════════════

import os
import shutil
import kagglehub

from .config import CAMINHO_DADOS


def carregar_dados_kaggle():
    """
    Baixa o dataset público de ratings ESG da ESG Enterprise via KaggleHub
    e salva em CAMINHO_DADOS (./data/raw/data.csv).

    Dataset: alistairking/public-company-esg-ratings-dataset
    """
    print("\n" + "═"*62)
    print("ETAPA 0 — DOWNLOAD DA BASE DE DADOS (KAGGLE)")
    print("═"*62)

    os.makedirs(os.path.dirname(CAMINHO_DADOS), exist_ok=True)

    print("\nBaixando dataset via KaggleHub...")
    path = kagglehub.dataset_download("alistairking/public-company-esg-ratings-dataset")

    arquivos = os.listdir(path)
    arquivo_csv = os.path.join(path, arquivos[0])
    shutil.copy(arquivo_csv, CAMINHO_DADOS)

    print(f"Arquivo salvo em: {CAMINHO_DADOS}")


if __name__ == "__main__":
    carregar_dados_kaggle()
