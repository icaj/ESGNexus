# esg_ml/interfaces/api/rotas_enterprise.py
# Rotas Enterprise com núcleo nexus_v2: inputs E/S/G, DiagnosticoESG completo

import json
import pandas as pd
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from esg_ml.adaptadores.entrada.leitor_fornecedores_pandas import LeitorFornecedoresPandas
from esg_ml.adaptadores.saida.repositorio_modelo_joblib import RepositorioModeloJoblib
from esg_ml.aplicacao.servico_avaliacao import ServicoAvaliacao
from esg_ml.dominio.entidades.empresa import Empresa, ScoreESG
from esg_ml.dominio.entidades.diagnostico import DiagnosticoESG
from esg_ml.infraestrutura.banco_dados import obter_sessao
from esg_ml.infraestrutura.configuracoes import Configuracoes
from esg_ml.infraestrutura.modelos_banco import AvaliacaoBanco, FornecedorBanco
from esg_ml.interfaces.api.dependencias_auth import exigir_perfil, obter_usuario_atual
from esg_ml.interfaces.api.esquemas import (
    AvaliacaoSaida, ClassificacaoLoteEntrada,
    FornecedorEntrada, ResultadoClassificacaoLote)

roteador = APIRouter(tags=['Enterprise'])
conf = Configuracoes()
repositorio = RepositorioModeloJoblib(conf.diretorio_artefatos)


def _dominio(entrada: FornecedorEntrada) -> Empresa:
    return Empresa(
        name=entrada.name,
        industry=entrada.industry,
        scores=ScoreESG(
            environment_score=entrada.environment_score,
            social_score=entrada.social_score,
            governance_score=entrada.governance_score,
        )
    )


def _saida(d: DiagnosticoESG) -> AvaliacaoSaida:
    return AvaliacaoSaida(**d.to_dict())


def _persistir_fornecedor(sessao: Session, entrada: FornecedorEntrada) -> None:
    existente = sessao.query(FornecedorBanco).filter(FornecedorBanco.name == entrada.name).first()
    if existente is None:
        sessao.add(FornecedorBanco(
            name=entrada.name, industry=entrada.industry,
            environment_score=entrada.environment_score,
            social_score=entrada.social_score,
            governance_score=entrada.governance_score))
    else:
        existente.industry          = entrada.industry
        existente.environment_score = entrada.environment_score
        existente.social_score      = entrada.social_score
        existente.governance_score  = entrada.governance_score


def _persistir_avaliacao(sessao: Session, d: DiagnosticoESG) -> None:
    dados = d.to_dict()
    sessao.add(AvaliacaoBanco(**dados))


# ── Treino ────────────────────────────────────────────────────────
@roteador.post('/treinar', dependencies=[Depends(exigir_perfil('administrador','cientista_dados'))])
def treinar() -> dict:
    """CRISP-DM Fases 2–6: baixa dados do Kaggle, GridSearchCV, critério Fase 5."""
    from esg_ml.aplicacao.servico_treinamento import ServicoTreinamento
    return ServicoTreinamento(repositorio).treinar()


# ── Classificação individual ──────────────────────────────────────
@roteador.post('/classificar', response_model=AvaliacaoSaida,
               dependencies=[Depends(obter_usuario_atual)])
def classificar(entrada: FornecedorEntrada,
                sessao: Session = Depends(obter_sessao)) -> AvaliacaoSaida:
    avaliacao = ServicoAvaliacao(repositorio).avaliar_um(_dominio(entrada))
    _persistir_fornecedor(sessao, entrada)
    _persistir_avaliacao(sessao, avaliacao)
    sessao.commit()
    return _saida(avaliacao)


# ── Classificação em lote ─────────────────────────────────────────
@roteador.post('/classificar/lote', response_model=ResultadoClassificacaoLote,
               dependencies=[Depends(obter_usuario_atual)])
def classificar_lote(entrada: ClassificacaoLoteEntrada,
                     sessao: Session = Depends(obter_sessao)) -> ResultadoClassificacaoLote:
    resultados, erros = [], []
    servico = ServicoAvaliacao(repositorio)
    for idx, forn in enumerate(entrada.fornecedores, 1):
        try:
            d = servico.avaliar_um(_dominio(forn))
            _persistir_fornecedor(sessao, forn)
            _persistir_avaliacao(sessao, d)
            resultados.append(_saida(d))
        except Exception as exc:
            erros.append({'linha': str(idx), 'name': forn.name, 'erro': str(exc)})
    sessao.commit()
    return ResultadoClassificacaoLote(
        total_processados=len(resultados), total_erros=len(erros),
        resultados=resultados, erros=erros)


# ── Upload de arquivo ─────────────────────────────────────────────
@roteador.post('/avaliar/upload', response_model=list[AvaliacaoSaida],
               dependencies=[Depends(obter_usuario_atual)])
async def avaliar_upload(arquivo, sessao: Session = Depends(obter_sessao)):
    from fastapi import File, UploadFile
    from pathlib import Path
    from tempfile import NamedTemporaryFile
    sufixo = Path(arquivo.filename or 'f.csv').suffix or '.csv'
    with NamedTemporaryFile(delete=False, suffix=sufixo) as tmp:
        tmp.write(await arquivo.read())
        tmp_path = Path(tmp.name)
    try:
        empresas = LeitorFornecedoresPandas(tmp_path).listar_empresas()
        servico  = ServicoAvaliacao(repositorio)
        resultados = []
        for empresa in empresas:
            forn_entrada = FornecedorEntrada(
                name=empresa.name, industry=empresa.industry,
                environment_score=empresa.scores.environment_score,
                social_score=empresa.scores.social_score,
                governance_score=empresa.scores.governance_score)
            d = servico.avaliar_um(empresa)
            _persistir_fornecedor(sessao, forn_entrada)
            _persistir_avaliacao(sessao, d)
            resultados.append(_saida(d))
        sessao.commit()
        return resultados
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    finally:
        tmp_path.unlink(missing_ok=True)


# ── Consultas ─────────────────────────────────────────────────────
@roteador.get('/fornecedores', dependencies=[Depends(obter_usuario_atual)])
def listar_fornecedores(sessao: Session = Depends(obter_sessao)) -> list[dict]:
    registros = sessao.query(FornecedorBanco).order_by(FornecedorBanco.name).all()
    return [{c.name: getattr(r, c.name)
             for c in r.__table__.columns if c.name != 'id'}
            for r in registros]


# ── Dashboards ────────────────────────────────────────────────────
@roteador.get('/dashboard/executivo', dependencies=[Depends(obter_usuario_atual)])
def dashboard_executivo(sessao: Session = Depends(obter_sessao)) -> dict:
    registros = sessao.query(AvaliacaoBanco).all()
    if not registros:
        return {'kpis': {}, 'distribuicao_maturidade': [], 'top_risco': [], 'melhores': []}
    df = pd.DataFrame([{c.name: getattr(r, c.name)
                         for c in r.__table__.columns} for r in registros])
    total = len(df)
    return {
        'kpis': {
            'total_fornecedores': total,
            'score_ponderado_medio': round(float(df['score_ponderado'].mean()), 2),
            'avancados': int((df['maturidade_rf'] == 'Avançado').sum()),
            'iniciantes': int((df['maturidade_rf'] == 'Iniciante').sum()),
            'modelos_concordam': int(df['maturidade_rf'].eq(df['maturidade_knn']).sum()),
        },
        'distribuicao_maturidade': (
            df.groupby('maturidade_rf', as_index=False).size()
              .rename(columns={'size':'quantidade'}).to_dict('records')),
        'distribuicao_quadrante': (
            df.groupby('quadrante', as_index=False).size()
              .rename(columns={'size':'quantidade'}).to_dict('records')),
        'medias_pilares': [
            {'pilar':'Ambiental','valor':round(float(df['environment_score'].mean()),1)},
            {'pilar':'Social',   'valor':round(float(df['social_score'].mean()),1)},
            {'pilar':'Governança','valor':round(float(df['governance_score'].mean()),1)},
        ],
        'top_risco': (df.sort_values('risco', ascending=False)
                        .head(10)[['name','industry','risco','impacto',
                                   'quadrante','maturidade_rf']].to_dict('records')),
        'melhores': (df.sort_values('score_ponderado', ascending=False)
                       .head(10)[['name','industry','score_ponderado',
                                  'grade','maturidade_rf']].to_dict('records')),
    }


@roteador.get('/dashboard/ml',
              dependencies=[Depends(exigir_perfil('administrador','cientista_dados'))])
def dashboard_ml(sessao: Session = Depends(obter_sessao)) -> dict:
    registros = sessao.query(AvaliacaoBanco).all()
    if not registros:
        return {'dispersao': [], 'distribuicao_confianca': []}
    df = pd.DataFrame([{c.name: getattr(r, c.name)
                         for c in r.__table__.columns} for r in registros])
    return {
        'dispersao': df[['name','industry','environment_score','social_score',
                          'governance_score','score_ponderado','risco','impacto',
                          'maturidade_rf','confianca_rf_high']].to_dict('records'),
        'distribuicao_confianca': df[['confianca_rf_high','confianca_rf_medium',
                                       'confianca_knn_high','confianca_knn_medium',
                                       'maturidade_rf']].to_dict('records'),
        'concordancia_modelos': {
            'total': len(df),
            'concordam': int(df['maturidade_rf'].eq(df['maturidade_knn']).sum()),
            'divergem':  int((~df['maturidade_rf'].eq(df['maturidade_knn'])).sum()),
        }
    }
