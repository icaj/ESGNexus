# esg_ml/interfaces/api/esquemas.py — Pydantic schemas nexus_v2
from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


# ── Entrada ───────────────────────────────────────────────────────────────────

class FornecedorEntrada(BaseModel):
    """Entrada da API para classificação de fornecedor.

    Campos obrigatórios (engine ML):
        name, industry, environment_score, social_score, governance_score

    Campos opcionais (cadastro/identificação):
        cnpj, email, telefone, contato, quantidade_funcionarios, endereco, website, descricao
    """
    # ── Obrigatórios ──────────────────────────────────────────────────────
    name:              str
    industry:          str = 'Unknown'
    environment_score: int = Field(ge=0, le=1000)
    social_score:      int = Field(ge=0, le=1000)
    governance_score:  int = Field(ge=0, le=1000)

    # ── Opcionais ─────────────────────────────────────────────────────────
    cnpj:                    Optional[str] = None
    email:                   Optional[str] = None
    telefone:                Optional[str] = None
    contato:                 Optional[str] = None   # nome do responsável
    quantidade_funcionarios: Optional[int] = Field(default=None, ge=0)
    endereco:                Optional[str] = None
    website:                 Optional[str] = None
    descricao:               Optional[str] = None


class ClassificacaoLoteEntrada(BaseModel):
    fornecedores: list[FornecedorEntrada]


# ── Saída: Plano de Ação ──────────────────────────────────────────────────────

class PlanoAcaoSaida(BaseModel):
    """Item individual do plano de ação recomendado pela engine ML."""
    pilar:       str    # 'E', 'S' ou 'G'
    score:       int    # score atual do pilar (0–1000)
    importancia: float  # feature importance RF
    acao:        str    # descrição da ação recomendada


# ── Saída: Avaliação completa ─────────────────────────────────────────────────

class AvaliacaoSaida(BaseModel):
    """Resultado completo do diagnóstico ESG (23 campos + plano de ação estruturado)."""
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
    acoes_recomendadas:    str   # resumo textual (retrocompatibilidade)
    plano_acao:            list[PlanoAcaoSaida] = []  # itens estruturados


class ResultadoClassificacaoLote(BaseModel):
    total_processados: int
    total_erros:       int
    resultados:        list[AvaliacaoSaida]
    erros:             list[dict[str, str]]


# ── Saída: Histórico ──────────────────────────────────────────────────────────

class HistoricoItemSaida(BaseModel):
    """Resumo de uma avaliação no histórico temporal do fornecedor."""
    avaliacao_id:      int
    criado_em:         datetime
    environment_score: int
    social_score:      int
    governance_score:  int
    total_score:       int
    score_ponderado:   float
    grade:             str
    maturidade_rf:     str
    maturidade_knn:    str
    confianca_rf_high: float
    risco:             float
    impacto:           float
    quadrante:         str
    plano_acao:        list[PlanoAcaoSaida] = []


class HistoricoFornecedorSaida(BaseModel):
    """Histórico completo de um fornecedor com todas as suas avaliações."""
    fornecedor_id:  int
    name:           str
    industry:       str
    total_avaliacoes: int
    avaliacoes:     list[HistoricoItemSaida]


# ── Saída: Fornecedor com dados cadastrais ────────────────────────────────────

class FornecedorSaida(BaseModel):
    """Dados completos do fornecedor cadastrado."""
    id:                      int
    name:                    str
    industry:                str
    environment_score:       int
    social_score:            int
    governance_score:        int
    cnpj:                    Optional[str] = None
    email:                   Optional[str] = None
    telefone:                Optional[str] = None
    contato:                 Optional[str] = None
    quantidade_funcionarios: Optional[int] = None
    endereco:                Optional[str] = None
    website:                 Optional[str] = None
    descricao:               Optional[str] = None
    criado_em:               Optional[datetime] = None
    atualizado_em:           Optional[datetime] = None
    total_avaliacoes:        int = 0
