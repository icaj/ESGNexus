# etapa1_preprocessamento.py
# ══════════════════════════════════════════════════════════════════
# Etapa 1 — Pré-processamento da base de dados
# Edenred Brasil | CESAR School 2025
# ══════════════════════════════════════════════════════════════════

import pandas as pd

from .config import (
    CAMINHO_DADOS, COLUNAS_REMOVER, FEATURES_SCORES,
    TARGET, NOMES_CANONICOS
)


def etapa1_preprocessamento(caminho: str = CAMINHO_DADOS) -> pd.DataFrame:
    """
    Carrega e limpa a base de dados bruta.

    Operações realizadas:
      1. Leitura do CSV
      2. Remoção de colunas de metadados não analíticos
      3. Preenchimento de nulos em 'industry' com 'Unknown'
      4. Normalização de nomes de indústria (str.strip + mapa canônico)
      5. Verificação de integridade: total_score == E + S + G
    """
    print("\n" + "═"*62)
    print("ETAPA 1 — PRÉ-PROCESSAMENTO")
    print("═"*62)

    df = pd.read_csv(caminho)
    print(f"\nBase carregada: {df.shape[0]} empresas × {df.shape[1]} colunas")

    # Remover colunas não analíticas
    df = df.drop(columns=[c for c in COLUNAS_REMOVER if c in df.columns])
    print(f"Colunas após remoção de metadados: {df.shape[1]}")

    # Tratar nulos de industry
    n_nulos = df['industry'].isna().sum()
    df['industry'] = df['industry'].fillna('Unknown')
    print(f"Nulos em 'industry': {n_nulos} → preenchidos com 'Unknown'")

    # Normalizar nomes de indústria
    df['industry'] = df['industry'].str.strip()
    antes  = df['industry'].value_counts().to_dict()
    df['industry'] = df['industry'].replace(NOMES_CANONICOS)
    depois = df['industry'].value_counts().to_dict()

    print(f"\nNormalização de nomes de indústria:")
    for original, canonico in NOMES_CANONICOS.items():
        n_antes  = antes.get(original, 0)
        n_depois = depois.get(canonico, 0)
        print(f"  '{original}'")
        print(f"    → '{canonico}'  ({n_antes} registros fundidos, total no grupo: {n_depois})")
    print(f"\n  Setores únicos antes : {len(antes)}")
    print(f"  Setores únicos depois: {df['industry'].nunique()}")

    # Verificar integridade: total_score == soma dos pilares
    soma = df[FEATURES_SCORES].sum(axis=1)
    assert (soma == df['total_score']).all(), "ERRO: total_score != soma dos pilares"
    print("\nVerificação: total_score = soma(E+S+G) ✓")

    # Distribuição do alvo
    print(f"\nDistribuição do alvo ({TARGET}):")
    for nivel, n in df[TARGET].value_counts().items():
        print(f"  {nivel:<10}: {n:3d}  ({n/len(df)*100:.1f}%)")

    print(f"\nGrades totais disponíveis na base:")
    grade_info = df.groupby('total_grade')['total_score'].agg(['min','max','count'])
    print(grade_info.sort_values('min').to_string())

    return df


if __name__ == "__main__":
    df = etapa1_preprocessamento()
    print(f"\nDataFrame retornado: {df.shape}")
