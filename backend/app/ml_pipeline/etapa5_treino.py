# etapa5_treino.py
# ══════════════════════════════════════════════════════════════════
# Etapa 5 — Treino dos modelos KNN e Random Forest
# Edenred Brasil | CESAR School 2025
# ══════════════════════════════════════════════════════════════════

import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, GridSearchCV
from sklearn.metrics import classification_report, accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def etapa5_treino(X_train, X_test, y_train, y_test,
                  FEATURES, le_target) -> tuple:
    """
    Treina KNN e Random Forest com GridSearchCV (5-fold estratificado).

    KNN
    ───
    Usa StandardScaler antes do cálculo de distância euclidiana,
    para que scores (0–1000) e industry_enc (0–43) fiquem na
    mesma escala e nenhuma feature domine o cálculo de distância.
    Testa k de 3 a 21 (ímpares).

    Random Forest
    ─────────────
    Não requer normalização. Treina múltiplas árvores em subconjuntos
    aleatórios (bagging) e vota por maioria. Produz importância de
    variáveis (Gini), que orienta a priorização do plano de ação.

    Retorna:
      knn_final, rf_final,
      y_pred_knn, y_pred_rf,
      importancias, melhor_k
    """
    print("\n" + "═"*62)
    print("ETAPA 5 — TREINO: KNN E RANDOM FOREST")
    print("═"*62)

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    # ── KNN ────────────────────────────────────────────────────────
    print("\n[KNN] Grid search de k com validação cruzada 5-fold...")

    knn_pipe = Pipeline([
        ('scaler', StandardScaler()),
        ('knn',    KNeighborsClassifier(metric='euclidean'))
    ])
    param_grid_knn = {'knn__n_neighbors': list(range(3, 22, 2))}

    grid_knn = GridSearchCV(
        knn_pipe, param_grid_knn, cv=cv,
        scoring='accuracy', n_jobs=-1, verbose=0
    )
    grid_knn.fit(X_train, y_train)

    melhor_k   = grid_knn.best_params_['knn__n_neighbors']
    resultados = grid_knn.cv_results_

    print(f"\n  Resultados por k:")
    for k, mean, std in zip(
        param_grid_knn['knn__n_neighbors'],
        resultados['mean_test_score'],
        resultados['std_test_score']
    ):
        barra = "█" * int(mean * 40)
        print(f"  k={k:02d}  {mean:.2%} ± {std:.2%}  {barra}")

    print(f"\n  → Melhor k = {melhor_k}  (acurácia CV = {grid_knn.best_score_:.2%})")

    knn_final  = grid_knn.best_estimator_
    y_pred_knn = knn_final.predict(X_test)
    print(f"  Acurácia no teste: {accuracy_score(y_test, y_pred_knn):.2%}")
    print("\n  Relatório completo (teste):")
    print(classification_report(y_test, y_pred_knn,
                                 target_names=le_target.classes_))

    # ── RANDOM FOREST ──────────────────────────────────────────────
    print("\n[RANDOM FOREST] Grid search com validação cruzada 5-fold...")

    rf_pipe = Pipeline([
        ('rf', RandomForestClassifier(random_state=42, n_jobs=-1))
    ])
    param_grid_rf = {
        'rf__n_estimators':     [100, 200],
        'rf__max_depth':        [4, 6, 8, None],
        'rf__min_samples_leaf': [5, 10, 15],
    }

    grid_rf = GridSearchCV(
        rf_pipe, param_grid_rf, cv=cv,
        scoring='accuracy', n_jobs=-1, verbose=0
    )
    grid_rf.fit(X_train, y_train)

    print(f"\n  → Melhores parâmetros: {grid_rf.best_params_}")
    print(f"  → Acurácia CV:         {grid_rf.best_score_:.2%}")

    rf_final  = grid_rf.best_estimator_
    y_pred_rf = rf_final.predict(X_test)
    print(f"  Acurácia no teste: {accuracy_score(y_test, y_pred_rf):.2%}")
    print("\n  Relatório completo (teste):")
    print(classification_report(y_test, y_pred_rf,
                                 target_names=le_target.classes_))

    # Importância das variáveis (Random Forest)
    rf_estimator = rf_final.named_steps['rf']
    importancias = sorted(
        zip(FEATURES, rf_estimator.feature_importances_),
        key=lambda x: -x[1]
    )
    print("\n  Importância das variáveis (Random Forest):")
    for feat, imp in importancias:
        barra = "█" * int(imp * 50)
        print(f"    {feat:<25} {imp:.4f}  {barra}")

    return knn_final, rf_final, y_pred_knn, y_pred_rf, importancias, melhor_k


if __name__ == "__main__":
    from .etapa1_preprocessamento import etapa1_preprocessamento
    from .etapa2_metricas import etapa2_metricas
    from .etapa4_features import etapa4_preparar_features
    df, _, _     = etapa2_metricas(etapa1_preprocessamento())
    X_train, X_test, y_train, y_test, FEATURES, le_ind, le_target, df = \
        etapa4_preparar_features(df)
    etapa5_treino(X_train, X_test, y_train, y_test, FEATURES, le_target)
