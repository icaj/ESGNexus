from pathlib import Path
import joblib
import numpy as np
from sklearn.ensemble import RandomForestRegressor

MODEL_PATH = Path(__file__).resolve().parent / "modelo_score_esg.joblib"

RISCO_MAP = {"BAIXO": 0, "MEDIO": 1, "ALTO": 2, "CRITICO": 3}


def _features(nota_ambiental, nota_social, nota_governanca, quantidade_certificacoes, nivel_risco):
    risco = RISCO_MAP.get(str(nivel_risco).upper(), 1)
    return np.array([[nota_ambiental, nota_social, nota_governanca, quantidade_certificacoes, risco]], dtype=float)


def treinar_modelo_demo():
    X = np.array([
        [90, 85, 88, 5, 0], [80, 77, 82, 3, 1], [65, 70, 68, 2, 1],
        [55, 58, 60, 1, 2], [40, 45, 50, 0, 3], [95, 92, 90, 6, 0],
        [72, 66, 70, 2, 1], [30, 35, 40, 0, 3], [88, 80, 84, 4, 0]
    ], dtype=float)
    y = np.array([88, 80, 68, 57, 43, 92, 70, 34, 84], dtype=float)
    model = RandomForestRegressor(n_estimators=80, random_state=42)
    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)
    return model


def carregar_modelo():
    if MODEL_PATH.exists():
        return joblib.load(MODEL_PATH)
    return treinar_modelo_demo()


def prever_score(dados):
    model = carregar_modelo()
    X = _features(
        dados.nota_ambiental,
        dados.nota_social,
        dados.nota_governanca,
        dados.quantidade_certificacoes,
        dados.nivel_risco,
    )
    score = float(model.predict(X)[0])
    score = max(0, min(100, score))
    if score >= 90:
        faixa = "A"
    elif score >= 75:
        faixa = "B"
    elif score >= 60:
        faixa = "C"
    else:
        faixa = "D"
    return {"score_previsto": round(score, 2), "faixa_prevista": faixa}
