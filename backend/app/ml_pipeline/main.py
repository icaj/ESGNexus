# main.py
# ══════════════════════════════════════════════════════════════════
# Orquestrador do Pipeline ESG
# Edenred Brasil | CESAR School 2025
#
# Executa todas as etapas em sequência.
# Cada etapa pode ser executada e testada de forma independente
# chamando diretamente seu próprio arquivo (ex: python etapa2_metricas.py).
#
# Uso:
#   python main.py
# ══════════════════════════════════════════════════════════════════

from .etapa0_carga          import carregar_dados_kaggle
from .etapa1_preprocessamento import etapa1_preprocessamento
from .etapa2_metricas       import etapa2_metricas
from .etapa3_exploracao     import etapa3_exploracao
from .etapa4_features       import etapa4_preparar_features
from .etapa5_treino         import etapa5_treino
from .etapa6_avaliacao      import etapa6_avaliacao
from .etapa7_salvar         import etapa7_salvar
from .config                import CAMINHO_DADOS


def start():
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  PIPELINE ESG — BASE ESG ENTERPRISE                      ║")
    print("║  Edenred Brasil | CESAR School 2025                      ║")
    print("╚══════════════════════════════════════════════════════════╝")

    carregar_dados_kaggle()

    df = etapa1_preprocessamento(CAMINHO_DADOS)

    df, pesos_por_ind, pesos_global = etapa2_metricas(df)

    etapa3_exploracao(df)

    X_train, X_test, y_train, y_test, FEATURES, le_ind, le_target, df = \
        etapa4_preparar_features(df)

    knn_final, rf_final, y_pred_knn, y_pred_rf, importancias, melhor_k = \
        etapa5_treino(X_train, X_test, y_train, y_test, FEATURES, le_target)

    etapa6_avaliacao(knn_final, rf_final, X_test, y_test,
                     y_pred_knn, y_pred_rf, importancias, le_target, FEATURES)

    etapa7_salvar(df, knn_final, rf_final, le_ind, le_target,
                  importancias, FEATURES, pesos_por_ind, pesos_global)

    print("\n╔══════════════════════════════════════════════════════════╗")
    print("║  PIPELINE CONCLUÍDO                                      ║")
    print("╚══════════════════════════════════════════════════════════╝")


if __name__ == "__main__":
    start()
