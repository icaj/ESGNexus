# esg_ml/interfaces/api/rotas_enterprise.py
# v3: FornecedorEntrada com 17 métricas PT → scores ESG calculados internamente.
# Saída inclui campos PT (pontuacao_esg, nivel_risco, motivos…) para o frontend.

import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from esg_ml.adaptadores.saida.repositorio_modelo_joblib import RepositorioModeloJoblib
from esg_ml.aplicacao.servico_avaliacao import ServicoAvaliacao
from esg_ml.dominio.entidades.empresa import Empresa, ScoreESG
from esg_ml.dominio.entidades.diagnostico import DiagnosticoESG
from esg_ml.infraestrutura.banco_dados import obter_sessao
from esg_ml.infraestrutura.configuracoes import Configuracoes
from esg_ml.infraestrutura.modelos_banco import (
    AvaliacaoBanco, ExperimentoMLBanco, FornecedorBanco, PlanoAcaoBanco)
from esg_ml.interfaces.api.dependencias_auth import exigir_perfil, obter_usuario_atual
from esg_ml.interfaces.api.esquemas import (
    AvaliacaoSaida,
    ClassificacaoLoteEntrada,
    FornecedorEntrada,
    FornecedorSaida,
    HistoricoFornecedorSaida,
    HistoricoItemSaida,
    PlanoAcaoSaida,
    ResultadoClassificacaoLote,
)

roteador   = APIRouter(tags=['Enterprise'])
conf       = Configuracoes()
repositorio = RepositorioModeloJoblib(conf.diretorio_artefatos)


# ── Mapeamento setor PT → industry EN (LabelEncoder Kaggle) ──────────────────

_MAPA_SETOR: dict[str, str] = {
    'tecnologia':          'Technology',
    'financeiro':          'Financial Services',
    'saude':               'Healthcare',
    'saúde':               'Healthcare',
    'energia':             'Energy',
    'industria':           'Industrials',
    'indústria':           'Industrials',
    'consumo':             'Consumer Discretionary',
    'varejo':              'Consumer Staples',
    'materiais':           'Materials',
    'servicos':            'Services',
    'serviços':            'Services',
    'logistica':           'Industrials',
    'logística':           'Industrials',
    'agronegocio':         'Consumer Staples',
    'agronegócio':         'Consumer Staples',
    'mineracao':           'Materials',
    'mineração':           'Materials',
    'telecomunicacoes':    'Communication Services',
    'telecomunicações':    'Communication Services',
    'imobiliario':         'Real Estate',
    'imobiliário':         'Real Estate',
    'utilidades':          'Utilities',
    'limpeza':             'Services',
    'alimentos':           'Consumer Staples',
    'transporte':          'Industrials',
}

_NOME_PILAR: dict[str, str] = {'E': 'Ambiental', 'S': 'Social', 'G': 'Governança'}


# ── Conversão de métricas PT → scores ESG ────────────────────────────────────

def _calcular_scores_esg(entrada: FornecedorEntrada) -> tuple[int, int, int, str]:
    """17 métricas de domínio PT → (env_score, social_score, gov_score, industry)."""

    # Ambiental (0-1000)
    e  = 250.0 if entrada.possui_politica_ambiental else 0.0
    e += min(entrada.percentual_energia_renovavel   * 2.5,  250.0)
    e += min(entrada.percentual_reciclagem_residuos * 2.0,  200.0)
    e += max(0.0, 200.0 * (1.0 - min(entrada.emissoes_carbono_ton / 5000.0, 1.0)))
    e += min(entrada.quantidade_certificacoes       * 20.0, 100.0)

    # Social (0-1000)
    s  = 250.0 if entrada.possui_programa_diversidade else 0.0
    s += max(0.0, 400.0 - entrada.incidentes_trabalhistas_12m * 40.0)
    s += max(0.0, 350.0 - entrada.noticias_negativas_12m      * 35.0)

    # Governança (0-1000)
    g  = 300.0 if entrada.possui_politica_privacidade_dados else 0.0
    g += 300.0 if entrada.possui_politica_anticorrupcao      else 0.0
    g += max(0.0, 200.0 - entrada.noticias_negativas_12m * 20.0)
    g += min(entrada.quantidade_certificacoes * 20.0, 200.0)
    if entrada.consta_lista_sancoes:
        g *= 0.1

    industry = _MAPA_SETOR.get(entrada.setor.lower().strip(), 'Services')
    return (int(min(max(e, 0.0), 1000.0)),
            int(min(max(s, 0.0), 1000.0)),
            int(min(max(g, 0.0), 1000.0)),
            industry)


def _nivel_risco(risco: float) -> str:
    if risco > 60:
        return 'alto'
    if risco > 30:
        return 'medio'
    return 'baixo'


# ── Helpers de conversão ──────────────────────────────────────────────────────

def _dominio(entrada: FornecedorEntrada) -> Empresa:
    """FornecedorEntrada (17 métricas PT) → Empresa (domínio ML)."""
    env, soc, gov, industry = _calcular_scores_esg(entrada)
    return Empresa(
        name=entrada.razao_social,
        industry=industry,
        scores=ScoreESG(environment_score=env, social_score=soc, governance_score=gov),
        cnpj=entrada.cnpj or None,
    )


def _saida(d: DiagnosticoESG, entrada: FornecedorEntrada | None = None) -> AvaliacaoSaida:
    """DiagnosticoESG → AvaliacaoSaida com campos PT para o frontend."""
    dados = d.to_dict()

    # Identificação PT
    if entrada is not None:
        dados['codigo_fornecedor'] = entrada.codigo_fornecedor
        dados['razao_social']      = entrada.razao_social
        dados['setor']             = entrada.setor

    # Pontuação 0-100
    dados['pontuacao_ambiental']  = d.environment_score // 10
    dados['pontuacao_social']     = d.social_score      // 10
    dados['pontuacao_governanca'] = d.governance_score  // 10
    dados['pontuacao_esg']        = round(d.score_ponderado / 10.0, 1)

    # Nível de risco e recomendação
    nr = _nivel_risco(d.risco)
    dados['nivel_risco']  = nr
    dados['recomendacao'] = {
        'alto':  'Requer plano de ação ESG imediato',
        'medio': 'Aprovar com plano de melhoria ESG',
        'baixo': 'Aprovar',
    }[nr]

    dados['probabilidade_ml_alto_risco'] = round(d.confianca_rf_high / 100.0, 3)

    # Motivos derivados do plano de ação
    motivos = [
        f"Pilar {_NOME_PILAR.get(item.pilar, item.pilar)} requer atenção (score {item.score}/1000)"
        for item in d.plano_acao[:3]
    ]
    dados['motivos'] = motivos or [
        f"Desempenho ESG {nr} — pontuação {dados['pontuacao_esg']}/100"
    ]

    dados['plano_acao'] = [
        PlanoAcaoSaida(pilar=item.pilar, score=item.score,
                       importancia=round(item.importancia, 4), acao=item.acao)
        for item in d.plano_acao
    ]
    return AvaliacaoSaida(**dados)


# ── Helpers de persistência ───────────────────────────────────────────────────

def _persistir_fornecedor(sessao: Session, entrada: FornecedorEntrada) -> FornecedorBanco:
    """Upsert de FornecedorBanco por CNPJ (fallback: razao_social)."""
    env, soc, gov, industry = _calcular_scores_esg(entrada)

    if entrada.cnpj:
        existente = sessao.query(FornecedorBanco).filter(
            FornecedorBanco.cnpj == entrada.cnpj).first()
    else:
        existente = sessao.query(FornecedorBanco).filter(
            FornecedorBanco.name == entrada.razao_social).first()

    if existente is None:
        forn = FornecedorBanco(
            name=entrada.razao_social,
            industry=industry,
            environment_score=env,
            social_score=soc,
            governance_score=gov,
            cnpj=entrada.cnpj or None,
        )
        sessao.add(forn)
        return forn

    existente.name              = entrada.razao_social
    existente.industry          = industry
    existente.environment_score = env
    existente.social_score      = soc
    existente.governance_score  = gov
    return existente


def _persistir_avaliacao(sessao: Session, d: DiagnosticoESG,
                          fornecedor_id: int | None = None) -> AvaliacaoBanco:
    dados = d.to_dict()
    dados['fornecedor_id'] = fornecedor_id
    av = AvaliacaoBanco(**dados)
    sessao.add(av)
    return av


def _persistir_plano_acao(sessao: Session, d: DiagnosticoESG,
                           avaliacao_id: int,
                           fornecedor_id: int | None = None) -> None:
    for item in d.plano_acao:
        sessao.add(PlanoAcaoBanco(
            avaliacao_id=avaliacao_id,
            fornecedor_id=fornecedor_id,
            pilar=item.pilar,
            score=item.score,
            importancia=item.importancia,
            acao=item.acao,
        ))


def _classificar_e_persistir(
    sessao: Session,
    entrada: FornecedorEntrada,
    servico: ServicoAvaliacao,
) -> AvaliacaoSaida:
    d        = servico.avaliar_um(_dominio(entrada))
    forn     = _persistir_fornecedor(sessao, entrada)
    sessao.flush()
    av_banco = _persistir_avaliacao(sessao, d, forn.id)
    sessao.flush()
    _persistir_plano_acao(sessao, d, av_banco.id, forn.id)
    return _saida(d, entrada)


# ── Treino ────────────────────────────────────────────────────────────────────

@roteador.post('/treinar',
               dependencies=[Depends(exigir_perfil('administrador', 'cientista_dados'))])
def treinar() -> dict:
    """CRISP-DM Fases 2–6: baixa dados do Kaggle, GridSearchCV, critério Fase 5."""
    from esg_ml.aplicacao.servico_treinamento import ServicoTreinamento
    return ServicoTreinamento(repositorio).treinar()


# ── Cadastro de fornecedor (sem classificação) ────────────────────────────────

@roteador.post('/fornecedores', response_model=FornecedorSaida,
               dependencies=[Depends(obter_usuario_atual)])
def cadastrar_fornecedor(entrada: FornecedorEntrada,
                         sessao: Session = Depends(obter_sessao)) -> FornecedorSaida:
    """Cadastra ou atualiza fornecedor sem executar classificação ML."""
    forn = _persistir_fornecedor(sessao, entrada)
    sessao.flush()
    sessao.commit()
    total = sessao.query(AvaliacaoBanco).filter(
        AvaliacaoBanco.fornecedor_id == forn.id).count()
    return FornecedorSaida(
        id=forn.id,
        codigo_fornecedor=entrada.codigo_fornecedor,
        razao_social=entrada.razao_social,
        name=forn.name,
        industry=forn.industry,
        environment_score=forn.environment_score,
        social_score=forn.social_score,
        governance_score=forn.governance_score,
        cnpj=forn.cnpj,
        criado_em=forn.criado_em,
        atualizado_em=forn.atualizado_em,
        total_avaliacoes=total,
    )


# ── Classificação individual ──────────────────────────────────────────────────

@roteador.post('/classificar', response_model=AvaliacaoSaida,
               dependencies=[Depends(obter_usuario_atual)])
def classificar(entrada: FornecedorEntrada,
                sessao: Session = Depends(obter_sessao)) -> AvaliacaoSaida:
    """Classifica um fornecedor e persiste resultado + plano de ação no banco."""
    servico = ServicoAvaliacao(repositorio)
    try:
        resultado = _classificar_e_persistir(sessao, entrada, servico)
        sessao.commit()
        return resultado
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


# ── Classificação em lote ─────────────────────────────────────────────────────

@roteador.post('/classificar/lote', response_model=ResultadoClassificacaoLote,
               dependencies=[Depends(obter_usuario_atual)])
def classificar_lote(entrada: ClassificacaoLoteEntrada,
                     sessao: Session = Depends(obter_sessao)) -> ResultadoClassificacaoLote:
    """Classifica lista de fornecedores com rastreamento de erros por linha."""
    servico        = ServicoAvaliacao(repositorio)
    resultados, erros = [], []

    ausentes = [n for n in ('modelo_knn', 'modelo_rf', 'config') if not repositorio.existe(n)]
    if ausentes:
        raise HTTPException(
            status_code=503,
            detail=f"Modelos ausentes: {ausentes}. Execute: POST /treinar",
        )

    for idx, forn in enumerate(entrada.fornecedores, 1):
        try:
            # SAVEPOINT por linha: falha de uma linha não quebra a sessão das demais
            with sessao.begin_nested():
                resultado = _classificar_e_persistir(sessao, forn, servico)
            resultados.append(resultado)
        except Exception as exc:
            erros.append({
                'linha':             str(idx),
                'codigo_fornecedor': forn.codigo_fornecedor,
                'razao_social':      forn.razao_social,
                'erro':              str(exc),
            })

    sessao.commit()
    return ResultadoClassificacaoLote(
        total_processados=len(resultados),
        total_erros=len(erros),
        resultados=resultados,
        erros=erros,
    )


# ── Upload de arquivo ─────────────────────────────────────────────────────────

@roteador.post('/avaliar/upload', response_model=list[AvaliacaoSaida],
               dependencies=[Depends(obter_usuario_atual)])
async def avaliar_upload(
    arquivo: UploadFile = File(...),
    sessao: Session = Depends(obter_sessao),
) -> list[AvaliacaoSaida]:
    """Upload CSV/XLSX com 17 colunas PT — classifica todos os fornecedores do arquivo.

    Colunas obrigatórias: codigo_fornecedor, razao_social, cnpj, setor, pais,
        possui_politica_ambiental, emissoes_carbono_ton, percentual_energia_renovavel,
        percentual_reciclagem_residuos, incidentes_trabalhistas_12m,
        possui_programa_diversidade, possui_politica_privacidade_dados,
        possui_politica_anticorrupcao, consta_lista_sancoes, noticias_negativas_12m,
        quantidade_certificacoes, receita_anual
    """
    from pathlib import Path
    from tempfile import NamedTemporaryFile

    sufixo = Path(arquivo.filename or 'arquivo.csv').suffix or '.csv'
    with NamedTemporaryFile(delete=False, suffix=sufixo) as tmp:
        tmp.write(await arquivo.read())
        tmp_path = Path(tmp.name)

    def _safe_float(v: object, default: float = 0.0) -> float:
        try:
            r = float(v)  # type: ignore[arg-type]
            return default if pd.isna(r) else r
        except (TypeError, ValueError):
            return default

    def _safe_int(v: object, default: int = 0) -> int:
        try:
            r = float(v)  # type: ignore[arg-type]
            return default if pd.isna(r) else int(r)
        except (TypeError, ValueError):
            return default

    ausentes = [n for n in ('modelo_knn', 'modelo_rf', 'config') if not repositorio.existe(n)]
    if ausentes:
        tmp_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=503,
            detail=f"Modelos ausentes: {ausentes}. Execute: POST /treinar",
        )

    try:
        df = (pd.read_csv(tmp_path)
              if sufixo.lower() == '.csv'
              else pd.read_excel(tmp_path))
        df.columns = [str(c).strip().lower().replace(' ', '_').replace('-', '_')
                      for c in df.columns]

        def _conv_bool(v: object) -> bool:
            if isinstance(v, bool):
                return v
            if pd.isna(v):
                return False
            return str(v).strip().lower() in {'1', 'true', 'sim', 's', 'yes', 'y'}

        for col in ['possui_politica_ambiental', 'possui_programa_diversidade',
                    'possui_politica_privacidade_dados', 'possui_politica_anticorrupcao',
                    'consta_lista_sancoes']:
            if col in df.columns:
                df[col] = df[col].map(_conv_bool)

        servico    = ServicoAvaliacao(repositorio)
        resultados: list[AvaliacaoSaida] = []

        for _, row in df.iterrows():
            forn = FornecedorEntrada(
                codigo_fornecedor              = str(row.get('codigo_fornecedor', '') or ''),
                razao_social                   = str(row.get('razao_social', '') or ''),
                cnpj                           = str(row.get('cnpj', '') or ''),
                setor                          = str(row.get('setor', '') or ''),
                pais                           = str(row.get('pais', 'BR') or 'BR'),
                possui_politica_ambiental      = bool(row.get('possui_politica_ambiental', False)),
                emissoes_carbono_ton           = _safe_float(row.get('emissoes_carbono_ton', 0)),
                percentual_energia_renovavel   = _safe_float(row.get('percentual_energia_renovavel', 0)),
                percentual_reciclagem_residuos = _safe_float(row.get('percentual_reciclagem_residuos', 0)),
                incidentes_trabalhistas_12m    = _safe_int(row.get('incidentes_trabalhistas_12m', 0)),
                possui_programa_diversidade    = bool(row.get('possui_programa_diversidade', False)),
                possui_politica_privacidade_dados = bool(row.get('possui_politica_privacidade_dados', False)),
                possui_politica_anticorrupcao  = bool(row.get('possui_politica_anticorrupcao', False)),
                consta_lista_sancoes           = bool(row.get('consta_lista_sancoes', False)),
                noticias_negativas_12m         = _safe_int(row.get('noticias_negativas_12m', 0)),
                quantidade_certificacoes       = _safe_int(row.get('quantidade_certificacoes', 0)),
                receita_anual                  = _safe_float(row.get('receita_anual', 0)),
            )
            # SAVEPOINT por linha: erro de DB não contamina a sessão das linhas seguintes
            with sessao.begin_nested():
                resultados.append(_classificar_e_persistir(sessao, forn, servico))

        sessao.commit()
        return resultados

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    finally:
        tmp_path.unlink(missing_ok=True)


# ── Consulta de fornecedores ──────────────────────────────────────────────────

@roteador.get('/fornecedores', response_model=list[FornecedorSaida],
              dependencies=[Depends(obter_usuario_atual)])
def listar_fornecedores(sessao: Session = Depends(obter_sessao)) -> list[FornecedorSaida]:
    """Lista todos os fornecedores com dados cadastrais e total de avaliações."""
    registros = sessao.query(FornecedorBanco).order_by(FornecedorBanco.name).all()
    result = []
    for r in registros:
        total = sessao.query(AvaliacaoBanco).filter(
            AvaliacaoBanco.fornecedor_id == r.id).count()
        result.append(FornecedorSaida(
            id=r.id,
            name=r.name,
            industry=r.industry,
            environment_score=r.environment_score,
            social_score=r.social_score,
            governance_score=r.governance_score,
            cnpj=r.cnpj,
            email=r.email,
            telefone=r.telefone,
            contato=r.contato,
            quantidade_funcionarios=r.quantidade_funcionarios,
            endereco=r.endereco,
            website=r.website,
            descricao=r.descricao,
            criado_em=r.criado_em,
            atualizado_em=r.atualizado_em,
            total_avaliacoes=total,
        ))
    return result


# ── Histórico de avaliações por fornecedor ────────────────────────────────────

@roteador.get('/fornecedores/{fornecedor_id}/historico',
              response_model=HistoricoFornecedorSaida,
              dependencies=[Depends(obter_usuario_atual)])
def historico_fornecedor(fornecedor_id: int,
                         sessao: Session = Depends(obter_sessao)) -> HistoricoFornecedorSaida:
    """Histórico completo de avaliações ESG de um fornecedor (ordem cronológica)."""
    forn = sessao.query(FornecedorBanco).filter(FornecedorBanco.id == fornecedor_id).first()
    if not forn:
        raise HTTPException(status_code=404, detail='Fornecedor não encontrado')

    avaliacoes = (sessao.query(AvaliacaoBanco)
                  .filter(AvaliacaoBanco.fornecedor_id == fornecedor_id)
                  .order_by(AvaliacaoBanco.criado_em.desc())
                  .all())

    itens = []
    for av in avaliacoes:
        planos = (sessao.query(PlanoAcaoBanco)
                  .filter(PlanoAcaoBanco.avaliacao_id == av.id)
                  .order_by(PlanoAcaoBanco.importancia.desc())
                  .all())
        itens.append(HistoricoItemSaida(
            avaliacao_id=av.id,
            criado_em=av.criado_em,
            environment_score=av.environment_score,
            social_score=av.social_score,
            governance_score=av.governance_score,
            total_score=av.total_score,
            score_ponderado=av.score_ponderado,
            grade=av.grade,
            maturidade_rf=av.maturidade_rf,
            maturidade_knn=av.maturidade_knn,
            confianca_rf_high=av.confianca_rf_high,
            risco=av.risco,
            impacto=av.impacto,
            quadrante=av.quadrante,
            plano_acao=[
                PlanoAcaoSaida(pilar=p.pilar, score=p.score,
                               importancia=p.importancia, acao=p.acao)
                for p in planos
            ],
        ))

    return HistoricoFornecedorSaida(
        fornecedor_id=forn.id,
        name=forn.name,
        industry=forn.industry,
        total_avaliacoes=len(itens),
        avaliacoes=itens,
    )


# ── Plano de ação atual do fornecedor ─────────────────────────────────────────

@roteador.get('/fornecedores/{fornecedor_id}/plano-acao',
              response_model=list[PlanoAcaoSaida],
              dependencies=[Depends(obter_usuario_atual)])
def plano_acao_fornecedor(fornecedor_id: int,
                           sessao: Session = Depends(obter_sessao)) -> list[PlanoAcaoSaida]:
    """Plano de ação da avaliação mais recente do fornecedor."""
    ultima_av = (sessao.query(AvaliacaoBanco)
                 .filter(AvaliacaoBanco.fornecedor_id == fornecedor_id)
                 .order_by(AvaliacaoBanco.criado_em.desc())
                 .first())
    if not ultima_av:
        raise HTTPException(status_code=404,
                            detail='Fornecedor não encontrado ou sem avaliações')

    planos = (sessao.query(PlanoAcaoBanco)
              .filter(PlanoAcaoBanco.avaliacao_id == ultima_av.id)
              .order_by(PlanoAcaoBanco.importancia.desc())
              .all())
    return [
        PlanoAcaoSaida(pilar=p.pilar, score=p.score,
                       importancia=p.importancia, acao=p.acao)
        for p in planos
    ]


# ── Plano de ação de uma avaliação específica ─────────────────────────────────

@roteador.get('/avaliacoes/{avaliacao_id}/plano-acao',
              response_model=list[PlanoAcaoSaida],
              dependencies=[Depends(obter_usuario_atual)])
def plano_acao_avaliacao(avaliacao_id: int,
                          sessao: Session = Depends(obter_sessao)) -> list[PlanoAcaoSaida]:
    """Plano de ação de uma avaliação específica (por ID)."""
    av = sessao.query(AvaliacaoBanco).filter(AvaliacaoBanco.id == avaliacao_id).first()
    if not av:
        raise HTTPException(status_code=404, detail='Avaliação não encontrada')

    planos = (sessao.query(PlanoAcaoBanco)
              .filter(PlanoAcaoBanco.avaliacao_id == avaliacao_id)
              .order_by(PlanoAcaoBanco.importancia.desc())
              .all())
    return [
        PlanoAcaoSaida(pilar=p.pilar, score=p.score,
                       importancia=p.importancia, acao=p.acao)
        for p in planos
    ]


# ── Dashboards ────────────────────────────────────────────────────────────────

@roteador.get('/dashboard/executivo', dependencies=[Depends(obter_usuario_atual)])
def dashboard_executivo(sessao: Session = Depends(obter_sessao)) -> dict:
    """KPIs executivos — usa a avaliação mais recente por fornecedor."""
    from sqlalchemy import func

    subq = (sessao.query(func.max(AvaliacaoBanco.id).label('max_id'))
            .filter(AvaliacaoBanco.fornecedor_id.isnot(None))
            .group_by(AvaliacaoBanco.fornecedor_id)
            .subquery())

    registros = (
        sessao.query(AvaliacaoBanco).join(subq, AvaliacaoBanco.id == subq.c.max_id).all()
        + sessao.query(AvaliacaoBanco).filter(AvaliacaoBanco.fornecedor_id.is_(None)).all()
    )

    if not registros:
        return {'kpis': {}, 'distribuicao_risco': [], 'medias_pilares': [],
                'top_risco': [], 'melhores': []}

    df = pd.DataFrame([{c.name: getattr(r, c.name)
                         for c in r.__table__.columns} for r in registros])

    df['nivel_risco'] = df['risco'].apply(_nivel_risco)

    top_df = df.sort_values('risco', ascending=False).head(10).copy()
    top_df['razao_social']               = top_df['name']
    top_df['probabilidade_ml_alto_risco'] = (top_df['confianca_rf_high'] / 100.0).round(3)

    mel_df = df.sort_values('score_ponderado', ascending=False).head(10).copy()
    mel_df['razao_social'] = mel_df['name']
    mel_df['pontuacao_esg'] = (mel_df['score_ponderado'] / 10.0).round(1)

    return {
        'kpis': {
            'total_fornecedores':     len(df),
            'score_medio':            round(float(df['score_ponderado'].mean()) / 10.0, 2),
            'alto_risco':             int((df['nivel_risco'] == 'alto').sum()),
            'probabilidade_ml_media': round(float(df['confianca_rf_high'].mean()), 1),
        },
        'distribuicao_risco': (
            df.groupby('nivel_risco', as_index=False)
              .size().rename(columns={'size': 'quantidade'}).to_dict('records')
        ),
        'medias_pilares': [
            {'pilar': 'Ambiental',  'valor': round(float(df['environment_score'].mean()) / 10.0, 1)},
            {'pilar': 'Social',     'valor': round(float(df['social_score'].mean())       / 10.0, 1)},
            {'pilar': 'Governança', 'valor': round(float(df['governance_score'].mean())   / 10.0, 1)},
        ],
        'top_risco': (
            top_df[['razao_social', 'industry', 'risco',
                    'probabilidade_ml_alto_risco', 'quadrante', 'maturidade_rf']]
            .to_dict('records')
        ),
        'melhores': (
            mel_df[['razao_social', 'industry', 'pontuacao_esg', 'grade', 'maturidade_rf']]
            .to_dict('records')
        ),
    }


@roteador.get('/dashboard/ml',
              dependencies=[Depends(exigir_perfil('administrador', 'cientista_dados'))])
def dashboard_ml(sessao: Session = Depends(obter_sessao)) -> dict:
    """Dashboard de ML: métricas do modelo, dispersão e importância de features."""
    # Métricas do modelo (DB → artefato → zeros)
    metricas: dict = {'accuracy': 0.0, 'precision': 0.0, 'recall': 0.0, 'f1': 0.0}
    ultimo_exp = (sessao.query(ExperimentoMLBanco)
                  .order_by(ExperimentoMLBanco.criado_em.desc()).first())
    if ultimo_exp:
        metricas = {
            'accuracy':  round(float(ultimo_exp.rf_acuracia),  3),
            'precision': round(float(ultimo_exp.rf_acuracia),  3),
            'recall':    round(float(ultimo_exp.rf_acuracia),  3),
            'f1':        round(float(ultimo_exp.rf_f1_medium), 3),
        }
    else:
        try:
            _, rf_meta = repositorio.carregar('modelo_rf')
            m = rf_meta.get('metricas', {})
            metricas = {k: round(float(v), 3)
                        for k, v in m.items()
                        if k in ('accuracy', 'precision', 'recall', 'f1')} or metricas
        except Exception:
            pass

    # Feature importance
    feature_importance: list = []
    try:
        _, rf_meta = repositorio.carregar('modelo_rf')
        importancias = dict(rf_meta.get('importancias', []))
        _LABELS_FI = {
            'environment_score': 'Ambiental',
            'social_score':      'Social',
            'governance_score':  'Governança',
            'industry_enc':      'Setor',
        }
        feature_importance = sorted(
            [{'variavel': _LABELS_FI.get(k, k), 'importancia': round(float(v) * 100, 1)}
             for k, v in importancias.items()],
            key=lambda x: -x['importancia'],
        )
    except Exception:
        pass

    registros = sessao.query(AvaliacaoBanco).all()
    if not registros:
        return {'metricas': metricas, 'distribuicao_scores': [],
                'dispersao': [], 'feature_importance': feature_importance}

    df = pd.DataFrame([{c.name: getattr(r, c.name)
                         for c in r.__table__.columns} for r in registros])

    df['nivel_risco']               = df['risco'].apply(_nivel_risco)
    df['pontuacao_esg']             = (df['score_ponderado'] / 10.0).round(1)
    df['probabilidade_ml_alto_risco'] = (df['confianca_rf_high'] / 100.0).round(3)
    df['pontuacao_ambiental']       = (df['environment_score'] / 10).astype(int)
    df['pontuacao_social']          = (df['social_score']      / 10).astype(int)
    df['pontuacao_governanca']      = (df['governance_score']  / 10).astype(int)
    df['razao_social']              = df['name']

    return {
        'metricas': metricas,
        'distribuicao_scores': (
            df[['razao_social', 'pontuacao_esg', 'nivel_risco']].to_dict('records')
        ),
        'dispersao': (
            df[['razao_social', 'pontuacao_esg', 'probabilidade_ml_alto_risco',
                'nivel_risco', 'pontuacao_ambiental', 'pontuacao_social', 'pontuacao_governanca']]
            .to_dict('records')
        ),
        'feature_importance': feature_importance,
    }
