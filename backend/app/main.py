from contextlib import asynccontextmanager
from datetime import date
from pathlib import Path

import pandas as pd
from fastapi import Depends, FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from .database import db_cursor, init_db
from .schemas import (
    LoginRequest,
    FornecedorCreate,
    FornecedorUpdate,
    AvaliacaoCreate,
    CertificacaoCreate,
    MlPrevisaoRequest,
)
from .security import verificar_senha, gerar_token, obter_usuario_logado, obter_usuarios_logados
from .ml_service import prever_score, treinar_modelo_demo

BASE_DIR = Path(__file__).resolve().parent


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    treinar_modelo_demo()
    yield


app = FastAPI(
    title="ESG Nexus API - FastAPI + ML",
    version="3.0.0",
    description="Backend para cadastro, ranking e analise ESG de fornecedores com suporte a machine learning.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    arquivo = BASE_DIR / "favicon.ico"
    if arquivo.exists():
        return FileResponse(arquivo)
    raise HTTPException(status_code=404, detail="favicon nao encontrado")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/auth/login")
@app.post("/auth/login", include_in_schema=False)
def login(dados: LoginRequest):
    with db_cursor() as cur:
        cur.execute("SELECT * FROM usuarios WHERE email = %s AND ativo = TRUE", (dados.email,))
        usuario = cur.fetchone()
    if not usuario or not verificar_senha(dados.senha, usuario["senha_hash"]):
        raise HTTPException(status_code=401, detail="Usuario ou senha invalidos")
    return {"access_token": gerar_token(usuario), "token_type": "bearer", "usuario": {"nome": usuario["nome"], "email": usuario["email"], "perfil": usuario["perfil"]}}


@app.get("/api/auth/me")
def me(usuario=Depends(obter_usuario_logado)):
    return usuario


@app.get("/api/fornecedores")
def listar_fornecedores(usuario=Depends(obter_usuario_logado)):
    with db_cursor() as cur:
        cur.execute("""
            SELECT f.*,
                   COALESCE(a.nota_final, 0) AS nota_final,
                   COALESCE(a.nota_ambiental, 0) AS nota_ambiental,
                   COALESCE(a.nota_social, 0) AS nota_social,
                   COALESCE(a.nota_governanca, 0) AS nota_governanca
              FROM fornecedores f
         LEFT JOIN LATERAL (
                   SELECT * FROM avaliacoes_fornecedor af
                    WHERE af.fornecedor_id = f.id
                    ORDER BY af.data_avaliacao DESC, af.id DESC
                    LIMIT 1
              ) a ON TRUE
          ORDER BY f.razao_social
        """)
        return cur.fetchall()


@app.post("/api/fornecedores")
def criar_fornecedor(dados: FornecedorCreate, usuario=Depends(obter_usuario_logado)):
    with db_cursor(commit=True) as cur:
        cur.execute("""
            INSERT INTO fornecedores
            (razao_social, nome_fantasia, cnpj, email, telefone, nome_contato, segmento, categoria, estado, cidade, nivel_risco, status)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            RETURNING id
        """, tuple(dados.model_dump().values()))
        novo = cur.fetchone()
    return {"id": novo["id"], "mensagem": "Fornecedor cadastrado com sucesso"}


@app.get("/api/fornecedores/{fornecedor_id}")
def obter_fornecedor(fornecedor_id: int, usuario=Depends(obter_usuario_logado)):
    with db_cursor() as cur:
        cur.execute("SELECT * FROM fornecedores WHERE id = %s", (fornecedor_id,))
        fornecedor = cur.fetchone()
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor nao encontrado")
    return fornecedor


@app.put("/api/fornecedores/{fornecedor_id}")
def atualizar_fornecedor(fornecedor_id: int, dados: FornecedorUpdate, usuario=Depends(obter_usuario_logado)):
    valores = dados.model_dump()
    with db_cursor(commit=True) as cur:
        cur.execute("""
            UPDATE fornecedores SET
                razao_social=%s, nome_fantasia=%s, cnpj=%s, email=%s, telefone=%s,
                nome_contato=%s, segmento=%s, categoria=%s, estado=%s, cidade=%s,
                nivel_risco=%s, status=%s, data_atualizacao=NOW()
            WHERE id=%s
        """, (*valores.values(), fornecedor_id))
    return {"mensagem": "Fornecedor atualizado"}


@app.delete("/api/fornecedores/{fornecedor_id}")
def excluir_fornecedor(fornecedor_id: int, usuario=Depends(obter_usuario_logado)):
    with db_cursor(commit=True) as cur:
        cur.execute("DELETE FROM fornecedores WHERE id=%s", (fornecedor_id,))
    return {"mensagem": "Fornecedor excluido"}


def calcular_classificacao(score: float) -> str:
    if score >= 90:
        return "A"
    if score >= 75:
        return "B"
    if score >= 60:
        return "C"
    return "D"


@app.post("/api/avaliacoes")
def criar_avaliacao(dados: AvaliacaoCreate, usuario=Depends(obter_usuario_logado)):
    pesos = obter_pesos()
    nota_final = (
        dados.nota_ambiental * pesos["peso_ambiental"] +
        dados.nota_social * pesos["peso_social"] +
        dados.nota_governanca * pesos["peso_governanca"]
    )
    classificacao = calcular_classificacao(nota_final)
    data_avaliacao = dados.data_avaliacao or date.today()
    with db_cursor(commit=True) as cur:
        cur.execute("""
            INSERT INTO avaliacoes_fornecedor
            (fornecedor_id, data_avaliacao, nota_ambiental, nota_social, nota_governanca, nota_final, classificacao, observacoes)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            RETURNING id
        """, (dados.fornecedor_id, data_avaliacao, dados.nota_ambiental, dados.nota_social, dados.nota_governanca, nota_final, classificacao, dados.observacoes))
        novo = cur.fetchone()
    return {"id": novo["id"], "nota_final": round(nota_final, 2), "classificacao": classificacao}


@app.get("/api/ranking")
def ranking(usuario=Depends(obter_usuario_logado)):
    with db_cursor() as cur:
        cur.execute("""
            SELECT f.id, f.razao_social, f.cnpj, f.segmento, f.categoria, f.nivel_risco,
                   a.nota_ambiental, a.nota_social, a.nota_governanca, a.nota_final, a.classificacao,
                   RANK() OVER (ORDER BY a.nota_final DESC NULLS LAST) AS posicao
              FROM fornecedores f
         LEFT JOIN LATERAL (
                   SELECT * FROM avaliacoes_fornecedor af
                    WHERE af.fornecedor_id = f.id
                    ORDER BY af.data_avaliacao DESC, af.id DESC
                    LIMIT 1
              ) a ON TRUE
          ORDER BY a.nota_final DESC NULLS LAST, f.razao_social
        """)
        return cur.fetchall()


@app.post("/api/certificacoes")
def criar_certificacao(dados: CertificacaoCreate, usuario=Depends(obter_usuario_logado)):
    with db_cursor(commit=True) as cur:
        cur.execute("""
            INSERT INTO certificacoes_fornecedor
            (fornecedor_id, nome, orgao_emissor, data_emissao, data_validade, status, url_arquivo)
            VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING id
        """, (dados.fornecedor_id, dados.nome, dados.orgao_emissor, dados.data_emissao, dados.data_validade, dados.status, dados.url_arquivo))
        novo = cur.fetchone()
    return {"id": novo["id"], "mensagem": "Certificacao cadastrada"}


@app.get("/api/certificacoes")
def listar_certificacoes(usuario=Depends(obter_usuario_logado)):
    with db_cursor() as cur:
        cur.execute("""
            SELECT c.*, f.razao_social
              FROM certificacoes_fornecedor c
              JOIN fornecedores f ON f.id = c.fornecedor_id
             ORDER BY c.data_validade NULLS LAST
        """)
        return cur.fetchall()


@app.get("/api/alertas")
def listar_alertas(usuario=Depends(obter_usuario_logado)):
    gerar_alertas_automaticos()
    with db_cursor() as cur:
        cur.execute("""
            SELECT a.*, f.razao_social
              FROM alertas a
         LEFT JOIN fornecedores f ON f.id = a.fornecedor_id
             ORDER BY a.data_criacao DESC
        """)
        return cur.fetchall()


@app.get("/api/configuracoes")
def listar_configuracoes(usuario=Depends(obter_usuario_logado)):
    with db_cursor() as cur:
        cur.execute("SELECT chave, valor FROM configuracoes ORDER BY chave")
        return cur.fetchall()


def obter_pesos():
    with db_cursor() as cur:
        cur.execute("SELECT chave, valor FROM configuracoes WHERE chave IN ('peso_ambiental','peso_social','peso_governanca')")
        rows = cur.fetchall()
    valores = {r["chave"]: float(r["valor"]) for r in rows}
    return {"peso_ambiental": valores.get("peso_ambiental", 0.35), "peso_social": valores.get("peso_social", 0.30), "peso_governanca": valores.get("peso_governanca", 0.35)}


def gerar_alertas_automaticos():
    with db_cursor(commit=True) as cur:
        cur.execute("""
            INSERT INTO alertas (fornecedor_id, tipo_alerta, severidade, titulo, descricao)
            SELECT f.id, 'SCORE_BAIXO', 'ALTA', 'Fornecedor com score ESG abaixo do minimo',
                   'O fornecedor possui nota final inferior ao limite minimo configurado.'
              FROM fornecedores f
              JOIN LATERAL (
                   SELECT * FROM avaliacoes_fornecedor af WHERE af.fornecedor_id=f.id ORDER BY af.data_avaliacao DESC, af.id DESC LIMIT 1
              ) a ON TRUE
             WHERE a.nota_final < 60
               AND NOT EXISTS (
                   SELECT 1 FROM alertas x WHERE x.fornecedor_id=f.id AND x.tipo_alerta='SCORE_BAIXO' AND x.status='ABERTO'
               )
        """)


@app.get("/api/dashboard")
def dashboard(usuario=Depends(obter_usuario_logado)):
    with db_cursor() as cur:
        cur.execute("SELECT COUNT(*) AS total FROM fornecedores")
        total = cur.fetchone()["total"]
        cur.execute("SELECT COUNT(*) AS total FROM avaliacoes_fornecedor")
        total_avaliacoes = cur.fetchone()["total"]
        cur.execute("SELECT COALESCE(AVG(nota_final),0) AS media FROM avaliacoes_fornecedor")
        media = float(cur.fetchone()["media"])
        cur.execute("SELECT COALESCE(COUNT(*),0) AS total FROM alertas WHERE status='ABERTO'")
        alertas_abertos = cur.fetchone()["total"]
        cur.execute("""
            SELECT classificacao, COUNT(*) AS total
              FROM (
                SELECT DISTINCT ON (fornecedor_id) fornecedor_id, classificacao
                  FROM avaliacoes_fornecedor
                 ORDER BY fornecedor_id, data_avaliacao DESC, id DESC
              ) ult
             GROUP BY classificacao
             ORDER BY classificacao
        """)
        distribuicao = cur.fetchall()
        cur.execute("""
            SELECT f.razao_social, a.nota_final
              FROM fornecedores f
              JOIN LATERAL (
                   SELECT * FROM avaliacoes_fornecedor af WHERE af.fornecedor_id=f.id ORDER BY af.data_avaliacao DESC, af.id DESC LIMIT 1
              ) a ON TRUE
             ORDER BY a.nota_final DESC
             LIMIT 10
        """)
        top10 = cur.fetchall()
        cur.execute("""
            SELECT COALESCE(f.segmento, 'Nao informado') AS segmento, COUNT(*) AS total, COALESCE(AVG(a.nota_final),0) AS media_score
              FROM fornecedores f
         LEFT JOIN LATERAL (
                   SELECT * FROM avaliacoes_fornecedor af WHERE af.fornecedor_id=f.id ORDER BY af.data_avaliacao DESC, af.id DESC LIMIT 1
              ) a ON TRUE
             GROUP BY COALESCE(f.segmento, 'Nao informado')
             ORDER BY total DESC
        """)
        por_segmento = cur.fetchall()
    return {"kpis": {"total_fornecedores": total, "total_avaliacoes": total_avaliacoes, "media_score": round(media, 2), "alertas_abertos": alertas_abertos}, "distribuicao_classificacao": distribuicao, "top10": top10, "por_segmento": por_segmento}


@app.post("/api/ml/prever-score")
def ml_prever_score(dados: MlPrevisaoRequest, usuario=Depends(obter_usuario_logado)):
    return prever_score(dados)


@app.post("/api/ml/importar-fornecedores-csv")
async def importar_csv(arquivo: UploadFile = File(...), usuario=Depends(obter_usuario_logado)):
    df = pd.read_csv(arquivo.file)
    obrigatorias = {"razao_social"}
    if not obrigatorias.issubset(df.columns):
        raise HTTPException(status_code=400, detail="CSV deve conter ao menos a coluna razao_social")
    total = 0
    with db_cursor(commit=True) as cur:
        for _, row in df.fillna("").iterrows():
            cur.execute("""
                INSERT INTO fornecedores (razao_social, nome_fantasia, cnpj, email, segmento, categoria, estado, cidade, nivel_risco, status)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (cnpj) DO NOTHING
            """, (
                row.get("razao_social"), row.get("nome_fantasia"), row.get("cnpj") or None,
                row.get("email"), row.get("segmento"), row.get("categoria"), row.get("estado"), row.get("cidade"),
                row.get("nivel_risco") or "MEDIO", row.get("status") or "ATIVO"
            ))
            total += 1
    return {"mensagem": "Importacao processada", "linhas_lidas": total}


@app.get("/api/usuarios-logados")
def usuarios_logados(usuarios=Depends(obter_usuarios_logados)):
    usuarios = obter_usuarios_logados()
    return {"usuarios_logados": list(usuarios.values())}
