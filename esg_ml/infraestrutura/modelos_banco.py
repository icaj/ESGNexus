# esg_ml/infraestrutura/modelos_banco.py
# ORM SQLAlchemy — tabelas adaptadas para DiagnosticoESG (23 campos nexus_v2)
from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from esg_ml.infraestrutura.banco_dados import Base


class UsuarioBanco(Base):
    __tablename__ = 'usuarios'
    id:          Mapped[int]      = mapped_column(Integer, primary_key=True, index=True)
    nome:        Mapped[str]      = mapped_column(String(120), nullable=False)
    email:       Mapped[str]      = mapped_column(String(180), nullable=False, unique=True, index=True)
    senha_hash:  Mapped[str]      = mapped_column(String(255), nullable=False)
    perfil:      Mapped[str]      = mapped_column(String(30),  nullable=False, default='analista_esg')
    ativo:       Mapped[bool]     = mapped_column(Boolean,     nullable=False, default=True)
    criado_em:   Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                   default=lambda: datetime.now(timezone.utc))


class FornecedorBanco(Base):
    """Fornecedor com colunas nexus_v2: name, industry, scores E/S/G."""
    __tablename__ = 'fornecedores'
    id:                Mapped[int]      = mapped_column(Integer, primary_key=True, index=True)
    name:              Mapped[str]      = mapped_column(String(220), nullable=False, index=True)
    industry:          Mapped[str]      = mapped_column(String(100), nullable=False)
    environment_score: Mapped[int]      = mapped_column(Integer, nullable=False)
    social_score:      Mapped[int]      = mapped_column(Integer, nullable=False)
    governance_score:  Mapped[int]      = mapped_column(Integer, nullable=False)
    criado_em:         Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                         default=lambda: datetime.now(timezone.utc))


class AvaliacaoBanco(Base):
    """Diagnóstico ESG completo — espelha os 23 campos de DiagnosticoESG.to_dict()."""
    __tablename__ = 'avaliacoes_esg'
    id:                    Mapped[int]      = mapped_column(Integer, primary_key=True, index=True)
    name:                  Mapped[str]      = mapped_column(String(220), nullable=False, index=True)
    industry:              Mapped[str]      = mapped_column(String(100), nullable=False)
    environment_score:     Mapped[int]      = mapped_column(Integer, nullable=False)
    social_score:          Mapped[int]      = mapped_column(Integer, nullable=False)
    governance_score:      Mapped[int]      = mapped_column(Integer, nullable=False)
    total_score:           Mapped[int]      = mapped_column(Integer, nullable=False)
    score_ponderado:       Mapped[float]    = mapped_column(Float,   nullable=False)
    grade:                 Mapped[str]      = mapped_column(String(10),  nullable=False)
    level:                 Mapped[str]      = mapped_column(String(40),  nullable=False)
    w_E:                   Mapped[float]    = mapped_column(Float, nullable=False)
    w_S:                   Mapped[float]    = mapped_column(Float, nullable=False)
    w_G:                   Mapped[float]    = mapped_column(Float, nullable=False)
    fonte_pesos:           Mapped[str]      = mapped_column(String(80),  nullable=False)
    risco:                 Mapped[float]    = mapped_column(Float, nullable=False)
    impacto:               Mapped[float]    = mapped_column(Float, nullable=False)
    quadrante:             Mapped[str]      = mapped_column(String(60),  nullable=False)
    maturidade_rf:         Mapped[str]      = mapped_column(String(20),  nullable=False)
    confianca_rf_high:     Mapped[float]    = mapped_column(Float, nullable=False)
    confianca_rf_medium:   Mapped[float]    = mapped_column(Float, nullable=False)
    maturidade_knn:        Mapped[str]      = mapped_column(String(20),  nullable=False)
    confianca_knn_high:    Mapped[float]    = mapped_column(Float, nullable=False)
    confianca_knn_medium:  Mapped[float]    = mapped_column(Float, nullable=False)
    acoes_recomendadas:    Mapped[str]      = mapped_column(Text,  nullable=False, default='')
    criado_em:             Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                             default=lambda: datetime.now(timezone.utc))


class ExperimentoMLBanco(Base):
    __tablename__ = 'experimentos_ml'
    id:             Mapped[int]      = mapped_column(Integer, primary_key=True)
    nome_execucao:  Mapped[str]      = mapped_column(String(120), nullable=False)
    knn_acuracia:   Mapped[float]    = mapped_column(Float, default=0)
    knn_f1_medium:  Mapped[float]    = mapped_column(Float, default=0)
    rf_acuracia:    Mapped[float]    = mapped_column(Float, default=0)
    rf_f1_medium:   Mapped[float]    = mapped_column(Float, default=0)
    knn_params:     Mapped[str]      = mapped_column(Text, nullable=True)
    rf_params:      Mapped[str]      = mapped_column(Text, nullable=True)
    mlflow_run_id:  Mapped[str|None] = mapped_column(String(120), nullable=True)
    criado_em:      Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                      default=lambda: datetime.now(timezone.utc))
