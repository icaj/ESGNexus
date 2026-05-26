# etapa2_metricas.py
# ══════════════════════════════════════════════════════════════════
# Etapa 2 — Cálculo de Maturidade, Risco e Impacto
# Edenred Brasil | CESAR School 2025
# ══════════════════════════════════════════════════════════════════

import pandas as pd

from .config import FEATURES_SCORES, TARGET, MAPA_MATURIDADE, MIN_EMPRESAS_PESO


def calcular_pesos_por_industria(df: pd.DataFrame) -> tuple:
    """
    Calcula o peso relativo de cada pilar (E, S, G) por indústria,
    usando a correlação intra-setor de cada pilar com o total_score.

    Para setores com n < MIN_EMPRESAS_PESO, usa os pesos globais
    como fallback para evitar pesos instáveis com poucas amostras.

    Retorna:
        pesos_por_ind : dict  { indústria: {w_E, w_S, w_G, n, fonte} }
        pesos_global  : dict  { coluna: peso }  (fallback geral)
    """
    # Pesos globais: correlação de cada pilar com total_score na base toda
    corr_global = (df[FEATURES_SCORES]
                   .corrwith(df['total_score'])
                   .clip(lower=0))
    soma_global  = corr_global.sum()
    pesos_global = (corr_global / soma_global).to_dict()

    pesos = {}
    for ind, grupo in df.groupby('industry'):
        n = len(grupo)
        if n >= MIN_EMPRESAS_PESO:
            corr = (grupo[FEATURES_SCORES]
                    .corrwith(grupo['total_score'])
                    .clip(lower=0))
            soma = corr.sum()
            if soma == 0:
                w     = pesos_global
                fonte = 'fallback (corr=0)'
            else:
                w     = (corr / soma).to_dict()
                fonte = f'empírico (n={n})'
        else:
            w     = pesos_global
            fonte = f'fallback (n={n}<{MIN_EMPRESAS_PESO})'

        pesos[ind] = {
            'w_E':   round(w['environment_score'], 4),
            'w_S':   round(w['social_score'],      4),
            'w_G':   round(w['governance_score'],  4),
            'n':     n,
            'fonte': fonte,
        }

    return pesos, pesos_global


def etapa2_metricas(df: pd.DataFrame) -> tuple:
    """
    Calcula score_ponderado, maturidade, risco, impacto e quadrante.

    Retorna:
        df            : DataFrame com as colunas calculadas
        pesos_por_ind : dicionário de pesos por indústria
        pesos_global  : pesos globais (fallback)
    """
    print("\n" + "═"*62)
    print("ETAPA 2 — CÁLCULO DE MATURIDADE, RISCO E IMPACTO")
    print("═"*62)

    pesos_por_ind, pesos_global = calcular_pesos_por_industria(df)

    print(f"\nPesos globais (fallback para n < {MIN_EMPRESAS_PESO}):")
    print(f"  w_E = {pesos_global['environment_score']:.4f}")
    print(f"  w_S = {pesos_global['social_score']:.4f}")
    print(f"  w_G = {pesos_global['governance_score']:.4f}")

    n_empirico = sum(1 for v in pesos_por_ind.values() if 'empírico' in v['fonte'])
    n_fallback = sum(1 for v in pesos_por_ind.values() if 'fallback'  in v['fonte'])
    print(f"\nSetores com pesos empíricos : {n_empirico}")
    print(f"Setores com fallback        : {n_fallback}")

    # Amostra de pesos mais distintos do global
    pesos_df = pd.DataFrame(pesos_por_ind).T[['w_E','w_S','w_G','n','fonte']]
    w_E_global = pesos_global['environment_score']
    pesos_df['desvio_E'] = (pesos_df['w_E'].astype(float) - w_E_global).abs()
    print("\nAmostra de pesos por setor (variação mais expressiva):")
    print(pesos_df.sort_values('desvio_E', ascending=False).head(8)[
        ['w_E','w_S','w_G','n','fonte']
    ].to_string())

    # ── Score ponderado ──────────────────────────────────────────
    def _score_ponderado(row):
        p   = pesos_por_ind.get(row['industry'], {})
        w_e = p.get('w_E', pesos_global['environment_score'])
        w_s = p.get('w_S', pesos_global['social_score'])
        w_g = p.get('w_G', pesos_global['governance_score'])
        return (w_e * row['environment_score'] +
                w_s * row['social_score']      +
                w_g * row['governance_score'])

    df['score_ponderado'] = df.apply(_score_ponderado, axis=1).round(1)

    # ── Maturidade (rótulo externo da ESG Enterprise) ────────────
    df['maturidade'] = df[TARGET].map(MAPA_MATURIDADE)

    # ── Risco: gap percentual até o máximo (1000) ────────────────
    df['risco'] = ((1000 - df['score_ponderado']) / 1000 * 100).round(1)

    # ── Impacto: percentil do score_ponderado dentro do setor ────
    df['impacto'] = (
        df.groupby('industry')['score_ponderado']
          .rank(pct=True)
          .mul(100)
          .round(1)
    )

    # ── Quadrante (Matriz de Criticidade) ────────────────────────
    def _quadrante(row):
        hi = row['impacto'] > 50
        hr = row['risco']   > 50
        if   hi and hr:      return "Alto Impacto / Alto Risco"
        elif hi and not hr:  return "Alto Impacto / Baixo Risco"
        elif not hi and hr:  return "Baixo Impacto / Alto Risco"
        else:                 return "Baixo Impacto / Baixo Risco"

    df['quadrante'] = df.apply(_quadrante, axis=1)

    # Resumo
    print("\nScore ponderado vs total_score (verificação):")
    print(df[['total_score','score_ponderado','risco','impacto']].describe().round(1))

    print("\nRisco médio por grade (usando score ponderado):")
    print(df.groupby('total_grade')['risco'].agg(['mean','min','max']).round(1))

    print("\nDistribuição por quadrante:")
    for q, n in df['quadrante'].value_counts().items():
        print(f"  {q:<38}: {n}")

    return df, pesos_por_ind, pesos_global


if __name__ == "__main__":
    from .etapa1_preprocessamento import etapa1_preprocessamento
    df = etapa1_preprocessamento()
    df, pesos_por_ind, pesos_global = etapa2_metricas(df)
    print(f"\nColunas adicionadas: score_ponderado, maturidade, risco, impacto, quadrante")
