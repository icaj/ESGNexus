# etapa4_features.py
# ══════════════════════════════════════════════════════════════════
# Etapa 4 — Preparação das features para Machine Learning
# Edenred Brasil | CESAR School 2025
# ══════════════════════════════════════════════════════════════════

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

from .config import FEATURES_SCORES, TARGET


def etapa4_preparar_features(df: pd.DataFrame) -> tuple:
    """
    Prepara X, y e os encoders para treino dos modelos.

    Features de entrada (X):
      - environment_score  (numérica, 0–1000)
      - social_score       (numérica, 0–1000)
      - governance_score   (numérica, 0–1000)
      - industry_enc       (encoding ordinal da indústria)

    Nota: total_score NÃO é incluído — seria multicolinearidade
    perfeita, pois total_score = E + S + G.

    Variável-alvo (y):
      - total_level: 'High' → 1, 'Medium' → 0

    Split:
      - 80% treino / 20% teste, estratificado por classe.

    Retorna:
      X_train, X_test, y_train, y_test,
      FEATURES, le_ind, le_target, df
    """
    print("\n" + "═"*62)
    print("ETAPA 4 — PREPARAÇÃO DAS FEATURES")
    print("═"*62)

    # Encoding da indústria
    le_ind = LabelEncoder()
    df['industry_enc'] = le_ind.fit_transform(df['industry'])

    FEATURES = FEATURES_SCORES + ['industry_enc']

    X = df[FEATURES].values
    y = df[TARGET].values

    le_target = LabelEncoder()
    y_enc     = le_target.fit_transform(y)  # Medium=0, High=1

    print(f"\nFeatures: {FEATURES}")
    print(f"Shape X : {X.shape}")
    print(f"Classes : {le_target.classes_}  "
          f"(encodadas como {list(range(len(le_target.classes_)))})")

    print(f"\nDistribuição y:")
    for cls, enc in zip(le_target.classes_, range(len(le_target.classes_))):
        n = (y_enc == enc).sum()
        print(f"  {cls} ({enc}): {n} ({n/len(y_enc)*100:.1f}%)")

    # Split estratificado 80/20
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_enc, test_size=0.2, stratify=y_enc, random_state=42
    )
    print(f"\nSplit: {len(X_train)} treino / {len(X_test)} teste (80/20, estratificado)")

    return X_train, X_test, y_train, y_test, FEATURES, le_ind, le_target, df


if __name__ == "__main__":
    from .etapa1_preprocessamento import etapa1_preprocessamento
    from .etapa2_metricas import etapa2_metricas
    df, _, _ = etapa2_metricas(etapa1_preprocessamento())
    X_train, X_test, y_train, y_test, FEATURES, le_ind, le_target, df = \
        etapa4_preparar_features(df)
    print(f"\nX_train shape: {X_train.shape}")
