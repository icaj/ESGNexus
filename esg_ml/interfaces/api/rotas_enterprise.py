# esg_ml/interfaces/api/rotas_enterprise.py
# Rotas Enterprise com núcleo nexus_v2: inputs E/S/G, DiagnosticoESG completo
# v2: histórico de avaliações por fornecedor + plano de ação estruturado em banco

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
from esg_ml.infraestrutura.modelos_banco import AvaliacaoBanco, FornecedorBanco, PlanoAcaoBanco
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

roteador = APIRouter(tags=['Enterprise'])
conf = Configuracoes()
repositorio = RepositorioModeloJoblib(conf.diretorio_artefatos)


# ── Helpers de conversão ──────────────────────────────────────────────────────

def _dominio(entrada: FornecedorEntrada) -> Empresa:
    """FornecedorEntrada (API) → Empresa (domínio), incluindo campos opcionais."""
    return Empresa(
        name=entrada.name,
        industry=entrada.industry,
        scores=ScoreESG(
            environment_score=entrada.environment_score,
            social_score=entrada.social_score,
            governance_score=entrada.governance_score,
        ),
        cnpj=entrada.cnpj,
        email=entrada.email,
        telefone=entrada.telefone,
        contato=entrada.contato,
        quantidade_funcionarios=entrada.quantidade_funcionarios,
        endereco=entrada.endereco,
        website=entrada.website,
        descricao=entrada.descricao,
    )


def _saida(d: DiagnosticoESG) -> AvaliacaoSaida:
    """DiagnosticoESG → AvaliacaoSaida com plano de ação estruturado."""
    dados = d.to_dict()
    dados['plano_acao'] = [
        PlanoAcaoSaida(
            pilar=item.pilar,
            score=item.score,
            importancia=round(item.importancia, 4),
            acao=item.acao,
        )
        for item in d.plano_acao
    ]
    return AvaliacaoSaida(**dados)


# ── Helpers de persistência ───────────────────────────────────────────────────

def _persistir_fornecedor(sessao: Session, entrada: FornecedorEntrada) -> FornecedorBanco:
    """Upsert de FornecedorBanco por name. Retorna o objeto (novo ou existente).

    Campos opcionais só são sobrescritos se o novo valor for não-None,
    preservando dados já cadastrados caso o upload não os inclua.
    """
    existente = sessao.query(FornecedorBanco).filter(FornecedorBanco.name == entrada.name).first()

    if existente is None:
        forn = FornecedorBanco(
            name=entrada.name,
            industry=entrada.industry,
            environment_score=entrada.environment_score,
            social_score=entrada.social_score,
            governance_score=entrada.governance_score,
            cnpj=entrada.cnpj,
            email=entrada.email,
            telefone=entrada.telefone,
            contato=entrada.contato,
            quantidade_funcionarios=entrada.quantidade_funcionarios,
            endereco=entrada.endereco,
            website=entrada.website,
            descricao=entrada.descricao,
        )
        sessao.add(forn)
        return forn

    # Atualizar campos obrigatórios
    existente.industry          = entrada.industry
    existente.environment_score = entrada.environment_score
    existente.social_score      = entrada.social_score
    existente.governance_score  = entrada.governance_score

    # Atualizar campos opcionais apenas se fornecidos (não sobrescreve com None)
    if entrada.cnpj                    is not None: existente.cnpj                    = entrada.cnpj
    if entrada.email                   is not None: existente.email                   = entrada.email
    if entrada.telefone                is not None: existente.telefone                = entrada.telefone
    if entrada.contato                 is not None: existente.contato                 = entrada.contato
    if entrada.quantidade_funcionarios is not None: existente.quantidade_funcionarios = entrada.quantidade_funcionarios
    if entrada.endereco                is not None: existente.endereco                = entrada.endereco
    if entrada.website                 is not None: existente.website                 = entrada.website
    if entrada.descricao               is not None: existente.descricao               = entrada.descricao

    return existente


def _persistir_avaliacao(sessao: Session, d: DiagnosticoESG,
                          fornecedor_id: int | None = None) -> AvaliacaoBanco:
    """Cria um novo registro de avaliação ESG (histórico — nunca sobrescreve)."""
    dados = d.to_dict()
    dados['fornecedor_id'] = fornecedor_id
    av = AvaliacaoBanco(**dados)
    sessao.add(av)
    return av


def _persistir_plano_acao(sessao: Session, d: DiagnosticoESG,
                           avaliacao_id: int,
                           fornecedor_id: int | None = None) -> None:
    """Persiste os itens do plano de ação da avaliação na tabela planos_acao."""
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
    """Fluxo completo: avaliar → persistir fornecedor → histórico → plano de ação."""
    d = servico.avaliar_um(_dominio(entrada))

    forn = _persistir_fornecedor(sessao, entrada)
    sessao.flush()                                   # obtém forn.id antes do commit

    av_banco = _persistir_avaliacao(sessao, d, forn.id)
    sessao.flush()                                   # obtém av_banco.id

    _persistir_plano_acao(sessao, d, av_banco.id, forn.id)

    return _saida(d)


# ── Treino ────────────────────────────────────────────────────────────────────

@roteador.post('/treinar', dependencies=[Depends(exigir_perfil('administrador', 'cientista_dados'))])
def treinar() -> dict:
    """CRISP-DM Fases 2–6: baixa dados do Kaggle, GridSearchCV, critério Fase 5."""
    from esg_ml.aplicacao.servico_treinamento import ServicoTreinamento
    return ServicoTreinamento(repositorio).treinar()


# ── Classificação individual ──────────────────────────────────────────────────

@roteador.post('/classificar', response_model=AvaliacaoSaida,
               dependencies=[Depends(obter_usuario_atual)])
def classificar(entrada: FornecedorEntrada,
                sessao: Session = Depends(obter_sessao)) -> AvaliacaoSaida:
    """Classifica um fornecedor e persiste resultado + plano de ação no banco."""
    servico = ServicoAvaliacao(repositorio)
    resultado = _classificar_e_persistir(sessao, entrada, servico)
    sessao.commit()
    return resultado


# ── Classificação em lote ─────────────────────────────────────────────────────

@roteador.post('/classificar/lote', response_model=ResultadoClassificacaoLote,
               dependencies=[Depends(obter_usuario_atual)])
def classificar_lote(entrada: ClassificacaoLoteEntrada,
                     sessao: Session = Depends(obter_sessao)) -> ResultadoClassificacaoLote:
    """Classifica lista de fornecedores com rastreamento de erros por linha."""
    servico = ServicoAvaliacao(repositorio)
    resultados, erros = [], []

    for idx, forn in enumerate(entrada.fornecedores, 1):
        try:
            resultado = _classificar_e_persistir(sessao, forn, servico)
            resultados.append(resultado)
        except Exception as exc:
            erros.append({'linha': str(idx), 'name': forn.name, 'erro': str(exc)})

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
async def avaliar_upload(arquivo, sessao: Session = Depends(obter_sessao)):
    """Upload CSV/XLSX — classifica todas as empresas do arquivo.

    Colunas obrigatórias: name, industry, environment_score, social_score, governance_score
    Colunas opcionais:    cnpj, email, telefone, contato, quantidade_funcionarios,
                          endereco, website, descricao
    """
    from fastapi import File, UploadFile
    from pathlib import Path
    from tempfile import NamedTemporaryFile

    sufixo = Path(arquivo.filename or 'f.csv').suffix or '.csv'
    with NamedTemporaryFile(delete=False, suffix=sufixo) as tmp:
        tmp.write(await arquivo.read())
        tmp_path = Path(tmp.name)

    try:
        empresas = LeitorFornecedoresPandas(tmp_path).listar_empresas()
        servico = ServicoAvaliacao(repositorio)
        resultados = []

        for empresa in empresas:
            # Reconstruir FornecedorEntrada a partir da Empresa (inclui campos opcionais)
            forn_entrada = FornecedorEntrada(
                name=empresa.name,
                industry=empresa.industry,
                environment_score=empresa.scores.environment_score,
                social_score=empresa.scores.social_score,
                governance_score=empresa.scores.governance_score,
                cnpj=empresa.cnpj,
                email=empresa.email,
                telefone=empresa.telefone,
                contato=empresa.contato,
                quantidade_funcionarios=empresa.quantidade_funcionarios,
                endereco=empresa.endereco,
                website=empresa.website,
                descricao=empresa.descricao,
            )
            resultado = _classificar_e_persistir(sessao, forn_entrada, servico)
            resultados.append(resultado)

        sessao.commit()
        return resultados

    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
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
    """Retorna o histórico completo de avaliações ESG de um fornecedor (ordem cronológica).

    Permite acompanhar a evolução temporal da maturidade ESG do fornecedor.
    """
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
    """Retorna o plano de ação da avaliação mais recente do fornecedor.

    O plano é gerado pela engine ML (Random Forest) e contém ações prioritizadas
    por importância de feature para os pilares E, S e G abaixo do limiar de conformidade.
    """
    ultima_av = (sessao.query(AvaliacaoBanco)
                 .filter(AvaliacaoBanco.fornecedor_id == fornecedor_id)
                 .order_by(AvaliacaoBanco.criado_em.desc())
                 .first())

    if not ultima_av:
        raise HTTPException(
            status_code=404,
            detail='Fornecedor não encontrado ou ainda não possui avaliações')

    planos = (sessao.query(PlanoAcaoBanco)
              .filter(PlanoAcaoBanco.avaliacao_id == ultima_av.id)
              .order_by(PlanoAcaoBanco.importancia.desc())
              .all())

    if not planos:
        return []  # todos os pilares estão acima do limiar de conformidade

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
    """Retorna o plano de ação de uma avaliação específica (por ID).

    Útil para consultar planos históricos de avaliações anteriores.
    """
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
    """KPIs executivos usando a avaliação mais recente por fornecedor."""
    # Subquery: ID da última avaliação por fornecedor_id
    from sqlalchemy import func

    # Última avaliação por fornecedor (para fornecedores vinculados)
    subq = (sessao.query(
                func.max(AvaliacaoBanco.id).label('max_id')
            )
            .filter(AvaliacaoBanco.fornecedor_id.isnot(None))
            .group_by(AvaliacaoBanco.fornecedor_id)
            .subquery())

    # Avaliações legadas (sem fornecedor_id) + última por fornecedor
    registros_vinculados = (sessao.query(AvaliacaoBanco)
                            .join(subq, AvaliacaoBanco.id == subq.c.max_id)
                            .all())
    registros_legados    = (sessao.query(AvaliacaoBanco)
                            .filter(AvaliacaoBanco.fornecedor_id.is_(None))
                            .all())
    registros = registros_vinculados + registros_legados

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
              .rename(columns={'size': 'quantidade'}).to_dict('records')),
        'distribuicao_quadrante': (
            df.groupby('quadrante', as_index=False).size()
              .rename(columns={'size': 'quantidade'}).to_dict('records')),
        'medias_pilares': [
            {'pilar': 'Ambiental',  'valor': round(float(df['environment_score'].mean()), 1)},
            {'pilar': 'Social',     'valor': round(float(df['social_score'].mean()), 1)},
            {'pilar': 'Governança', 'valor': round(float(df['governance_score'].mean()), 1)},
        ],
        'top_risco': (df.sort_values('risco', ascending=False)
                        .head(10)[['name', 'industry', 'risco', 'impacto',
                                   'quadrante', 'maturidade_rf']].to_dict('records')),
        'melhores': (df.sort_values('score_ponderado', ascending=False)
                       .head(10)[['name', 'industry', 'score_ponderado',
                                  'grade', 'maturidade_rf']].to_dict('records')),
    }


@roteador.get('/dashboard/ml',
              dependencies=[Depends(exigir_perfil('administrador', 'cientista_dados'))])
def dashboard_ml(sessao: Session = Depends(obter_sessao)) -> dict:
    """Métricas de ML: dispersão, confiança dos modelos, concordância KNN vs RF."""
    registros = sessao.query(AvaliacaoBanco).all()
    if not registros:
        return {'dispersao': [], 'distribuicao_confianca': []}

    df = pd.DataFrame([{c.name: getattr(r, c.name)
                         for c in r.__table__.columns} for r in registros])
    return {
        'dispersao': df[['name', 'industry', 'environment_score', 'social_score',
                          'governance_score', 'score_ponderado', 'risco', 'impacto',
                          'maturidade_rf', 'confianca_rf_high']].to_dict('records'),
        'distribuicao_confianca': df[['confianca_rf_high', 'confianca_rf_medium',
                                       'confianca_knn_high', 'confianca_knn_medium',
                                       'maturidade_rf']].to_dict('records'),
        'concordancia_modelos': {
            'total':    len(df),
            'concordam': int(df['maturidade_rf'].eq(df['maturidade_knn']).sum()),
            'divergem':  int((~df['maturidade_rf'].eq(df['maturidade_knn'])).sum()),
        },
    }
