from app.models.schemas import PrevisaoScoreRequest

PESOS = {
    'ambiental': 0.35,
    'social': 0.30,
    'governanca': 0.35,
}

RISCO_PENALIDADE = {
    'BAIXO': 0,
    'MEDIO': 3,
    'ALTO': 8,
    'CRITICO': 15,
}

def prever_score_esg(dados: PrevisaoScoreRequest) -> dict:
    """
    Modelo inicial simples e explicavel.
    Pode ser substituido depois por um modelo scikit-learn carregado com joblib.
    """
    score_base = (
        dados.nota_ambiental * PESOS['ambiental'] +
        dados.nota_social * PESOS['social'] +
        dados.nota_governanca * PESOS['governanca']
    )
    bonus_certificacoes = min(dados.quantidade_certificacoes * 1.5, 6)
    penalidade_risco = RISCO_PENALIDADE.get(dados.nivel_risco.upper(), 3)
    score_final = max(0, min(100, score_base + bonus_certificacoes - penalidade_risco))
    if score_final >= 90:
        faixa = 'A'
    elif score_final >= 75:
        faixa = 'B'
    elif score_final >= 60:
        faixa = 'C'
    else:
        faixa = 'D'
    return {
        'score_previsto': round(score_final, 2),
        'faixa': faixa,
        'modelo': 'heuristico_inicial',
        'observacao': 'Este endpoint esta preparado para evoluir para scikit-learn/joblib.'
    }
