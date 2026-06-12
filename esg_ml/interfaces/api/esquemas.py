# esg_ml/interfaces/api/esquemas.py — Pydantic schemas nexus_v2
from pydantic import BaseModel, Field

class FornecedorEntrada(BaseModel):
    """Entrada: scores ESG 0–1000 por pilar (padrão nexus_v2)."""
    name:              str
    industry:          str = 'Unknown'
    environment_score: int = Field(ge=0, le=1000)
    social_score:      int = Field(ge=0, le=1000)
    governance_score:  int = Field(ge=0, le=1000)

class AvaliacaoSaida(BaseModel):
    """Saída: DiagnosticoESG completo (23 campos)."""
    name:                  str
    industry:              str
    environment_score:     int
    social_score:          int
    governance_score:      int
    total_score:           int
    score_ponderado:       float
    grade:                 str
    level:                 str
    w_E:                   float
    w_S:                   float
    w_G:                   float
    fonte_pesos:           str
    risco:                 float
    impacto:               float
    quadrante:             str
    maturidade_rf:         str
    confianca_rf_high:     float
    confianca_rf_medium:   float
    maturidade_knn:        str
    confianca_knn_high:    float
    confianca_knn_medium:  float
    acoes_recomendadas:    str

class ClassificacaoLoteEntrada(BaseModel):
    fornecedores: list[FornecedorEntrada]

class ResultadoClassificacaoLote(BaseModel):
    total_processados: int
    total_erros:       int
    resultados:        list[AvaliacaoSaida]
    erros:             list[dict[str, str]]
