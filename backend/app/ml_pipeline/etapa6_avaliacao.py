# etapa6_avaliacao.py
# ══════════════════════════════════════════════════════════════════
# Etapa 6 — Avaliação dos modelos e visualizações
# Edenred Brasil | CESAR School 2025
# ══════════════════════════════════════════════════════════════════

import matplotlib.pyplot as plt
from sklearn.metrics import (
    confusion_matrix, ConfusionMatrixDisplay, accuracy_score
)

from .config import PASTA_SAIDA


def etapa6_avaliacao(knn_final, rf_final, X_test, y_test,
                     y_pred_knn, y_pred_rf, importancias,
                     le_target, FEATURES):
    """
    Avalia os dois modelos no conjunto de teste e gera visualizações.

    Painéis gerados:
      1. Matriz de confusão do KNN
      2. Matriz de confusão do Random Forest
      3. Importância das variáveis (Random Forest, Gini)

    Salva em: PASTA_SAIDA/avaliacao_modelos.png
    """
    print("\n" + "═"*62)
    print("ETAPA 6 — AVALIAÇÃO E VISUALIZAÇÕES")
    print("═"*62)

    fig, axes = plt.subplots(1, 3, figsize=(16, 5), facecolor='#F7F8FA')
    fig.suptitle('Avaliação dos Modelos ML — ESG',
                 fontsize=14, fontweight='bold', color='#1A1A2E')

    # Matriz de confusão KNN
    cm_knn = confusion_matrix(y_test, y_pred_knn)
    disp   = ConfusionMatrixDisplay(cm_knn, display_labels=le_target.classes_)
    disp.plot(ax=axes[0], colorbar=False, cmap='Blues')
    axes[0].set_title(
        f'KNN — Matriz de Confusão\nAcurácia: {accuracy_score(y_test, y_pred_knn):.2%}',
        fontweight='bold'
    )

    # Matriz de confusão Random Forest
    cm_rf  = confusion_matrix(y_test, y_pred_rf)
    disp2  = ConfusionMatrixDisplay(cm_rf, display_labels=le_target.classes_)
    disp2.plot(ax=axes[1], colorbar=False, cmap='Greens')
    axes[1].set_title(
        f'Random Forest — Matriz de Confusão\nAcurácia: {accuracy_score(y_test, y_pred_rf):.2%}',
        fontweight='bold'
    )

    # Importância das variáveis (Random Forest)
    feats   = [f[0] for f in importancias]
    valores = [f[1] for f in importancias]
    colors_imp = [
        '#3498DB' if v < 0.3 else ('#E67E22' if v < 0.6 else '#E74C3C')
        for v in valores
    ]
    axes[2].barh(range(len(feats)), valores, color=colors_imp,
                 edgecolor='white', height=0.6)
    axes[2].set_yticks(range(len(feats)))
    axes[2].set_yticklabels(feats, fontsize=9)
    axes[2].set_title('Importância das Variáveis\n(Random Forest)',
                      fontweight='bold')
    axes[2].set_xlabel('Importância (Gini)')
    axes[2].set_facecolor('#FAFAFA')
    axes[2].spines[['top', 'right']].set_visible(False)
    for i, val in enumerate(valores):
        axes[2].text(val + 0.002, i, f'{val:.3f}', va='center', fontsize=8)

    plt.tight_layout()
    plt.savefig(f'{PASTA_SAIDA}/avaliacao_modelos.png',
                dpi=140, bbox_inches='tight', facecolor='#F7F8FA')
    plt.close()
    print(f"Gráfico salvo: {PASTA_SAIDA}/avaliacao_modelos.png")

    # Comparativo final
    print(f"\n{'─'*40}")
    print(f"  COMPARATIVO FINAL")
    print(f"{'─'*40}")
    print(f"  Modelo         Acurácia (teste)")
    print(f"  KNN            {accuracy_score(y_test, y_pred_knn):.2%}")
    print(f"  Random Forest  {accuracy_score(y_test, y_pred_rf):.2%}")


if __name__ == "__main__":
    from .etapa1_preprocessamento import etapa1_preprocessamento
    from .etapa2_metricas import etapa2_metricas
    from .etapa4_features import etapa4_preparar_features
    from .etapa5_treino import etapa5_treino

    df, _, _     = etapa2_metricas(etapa1_preprocessamento())
    X_train, X_test, y_train, y_test, FEATURES, le_ind, le_target, df = \
        etapa4_preparar_features(df)
    knn_final, rf_final, y_pred_knn, y_pred_rf, importancias, melhor_k = \
        etapa5_treino(X_train, X_test, y_train, y_test, FEATURES, le_target)
    etapa6_avaliacao(knn_final, rf_final, X_test, y_test,
                     y_pred_knn, y_pred_rf, importancias, le_target, FEATURES)
