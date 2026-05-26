# etapa7_salvar.py
# ══════════════════════════════════════════════════════════════════
# Etapa 7 — Salvar modelos e metadados
# Edenred Brasil | CESAR School 2025
# ══════════════════════════════════════════════════════════════════

import pandas as pd
import joblib

from .config import PASTA_MODELOS, PASTA_BRONZE, MAPA_MATURIDADE, MIN_EMPRESAS_PESO


def etapa7_salvar(df, knn_final, rf_final, le_ind, le_target,
                  importancias, FEATURES, pesos_por_ind, pesos_global):
    """
    Salva todos os artefatos necessários para o script esg_predicao.py.

    Arquivos gerados em PASTA_MODELOS:
      modelo_knn.pkl  — modelo KNN + encoders + base de referência
      modelo_rf.pkl   — modelo RF  + encoders + importâncias
      config.pkl      — configurações, benchmark e pesos por indústria

    Arquivos gerados em PASTA_BRONZE:
      pesos_por_industria.csv — tabela de pesos para documentação
      base_processada.csv     — base completa com métricas calculadas
    """
    print("\n" + "═"*62)
    print("ETAPA 7 — SALVANDO MODELOS")
    print("═"*62)

    # Base de referência para benchmarking por vizinhança (KNN)
    base_ref = df[[
        'name', 'industry', 'environment_score', 'social_score',
        'governance_score', 'total_score', 'score_ponderado',
        'total_grade', 'total_level', 'maturidade',
        'risco', 'impacto', 'quadrante'
    ]].copy()

    # Benchmark médio por indústria (para cálculo de impacto na predição)
    benchmark = df.groupby('industry')[[
        'environment_score', 'social_score', 'governance_score',
        'total_score', 'score_ponderado'
    ]].mean().round(1).to_dict()

    # modelo_knn.pkl
    joblib.dump({
        'modelo':      knn_final,
        'le_target':   le_target,
        'le_industry': le_ind,
        'features':    FEATURES,
        'base_ref':    base_ref.to_dict('records'),
    }, f'{PASTA_MODELOS}/modelo_knn.pkl')
    print(f"  ✓ {PASTA_MODELOS}/modelo_knn.pkl")

    # modelo_rf.pkl
    joblib.dump({
        'modelo':       rf_final,
        'le_target':    le_target,
        'le_industry':  le_ind,
        'features':     FEATURES,
        'importancias': importancias,
        'base_ref':     base_ref.to_dict('records'),
    }, f'{PASTA_MODELOS}/modelo_rf.pkl')
    print(f"  ✓ {PASTA_MODELOS}/modelo_rf.pkl")

    # config.pkl
    joblib.dump({
        'le_industry':       le_ind,
        'le_target':         le_target,
        'features':          FEATURES,
        'benchmark':         benchmark,
        'mapa_maturidade':   MAPA_MATURIDADE,
        'pesos_por_ind':     pesos_por_ind,
        'pesos_global':      pesos_global,
        'min_empresas_peso': MIN_EMPRESAS_PESO,
    }, f'{PASTA_MODELOS}/config.pkl')
    print(f"  ✓ {PASTA_MODELOS}/config.pkl")

    # pesos_por_industria.csv
    pd.DataFrame(pesos_por_ind).T[['w_E', 'w_S', 'w_G', 'n', 'fonte']].to_csv(
        f'{PASTA_BRONZE}/pesos_por_industria.csv'
    )
    print(f"  ✓ {PASTA_BRONZE}/pesos_por_industria.csv")

    # base_processada.csv
    base_ref.to_csv(f'{PASTA_BRONZE}/base_processada.csv', index=False)
    print(f"  ✓ {PASTA_BRONZE}/base_processada.csv")

    print(f"\nPróximo passo: execute esg_predicao.py para classificar novos fornecedores.")


if __name__ == "__main__":
    from .etapa1_preprocessamento import etapa1_preprocessamento
    from .etapa2_metricas import etapa2_metricas
    from .etapa4_features import etapa4_preparar_features
    from .etapa5_treino import etapa5_treino

    df, pesos_por_ind, pesos_global = etapa2_metricas(etapa1_preprocessamento())
    X_train, X_test, y_train, y_test, FEATURES, le_ind, le_target, df = \
        etapa4_preparar_features(df)
    knn_final, rf_final, y_pred_knn, y_pred_rf, importancias, melhor_k = \
        etapa5_treino(X_train, X_test, y_train, y_test, FEATURES, le_target)
    etapa7_salvar(df, knn_final, rf_final, le_ind, le_target,
                  importancias, FEATURES, pesos_por_ind, pesos_global)
