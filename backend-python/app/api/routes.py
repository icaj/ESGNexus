from fastapi import APIRouter, Depends, HTTPException
from app.db.connection import get_connection
from app.models.schemas import LoginRequest, FornecedorCreate, FornecedorUpdate, AvaliacaoCreate, PrevisaoScoreRequest
from app.services.auth_service import autenticar, usuario_atual
from app.ml.score_model import prever_score_esg

router = APIRouter(prefix='/api')

@router.post('/auth/login')
def login(payload: LoginRequest):
    return autenticar(payload.email, payload.senha)

@router.get('/auth/me')
def me(usuario=Depends(usuario_atual)):
    return usuario

@router.get('/fornecedores')
def listar_fornecedores(usuario=Depends(usuario_atual)):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM fornecedores ORDER BY razao_social')
        rows = cur.fetchall()
        cur.close()
        return rows

@router.post('/fornecedores', status_code=201)
def criar_fornecedor(payload: FornecedorCreate, usuario=Depends(usuario_atual)):
    sql = '''INSERT INTO fornecedores
        (razao_social, nome_fantasia, cnpj, email, telefone, nome_contato, segmento, categoria, pais, estado, cidade, nivel_risco, status)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id'''
    valores = tuple(payload.model_dump().values())
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(sql, valores)
        row = cur.fetchone()
        novo_id = row['id']
        cur.close()
        return {'id': novo_id, **payload.model_dump()}

@router.get('/fornecedores/{fornecedor_id}')
def obter_fornecedor(fornecedor_id: int, usuario=Depends(usuario_atual)):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM fornecedores WHERE id = %s', (fornecedor_id,))
        row = cur.fetchone()
        cur.close()
        if not row:
            raise HTTPException(status_code=404, detail='Fornecedor nao encontrado')
        return row

@router.put('/fornecedores/{fornecedor_id}')
def atualizar_fornecedor(fornecedor_id: int, payload: FornecedorUpdate, usuario=Depends(usuario_atual)):
    dados = payload.model_dump(exclude_unset=True)
    if not dados:
        return obter_fornecedor(fornecedor_id, usuario)
    campos = ', '.join([f'{campo} = %s' for campo in dados.keys()])
    valores = list(dados.values()) + [fornecedor_id]
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(f'UPDATE fornecedores SET {campos} WHERE id = %s', valores)
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail='Fornecedor nao encontrado')
        cur.close()
    return obter_fornecedor(fornecedor_id, usuario)

@router.delete('/fornecedores/{fornecedor_id}')
def excluir_fornecedor(fornecedor_id: int, usuario=Depends(usuario_atual)):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute('DELETE FROM fornecedores WHERE id = %s', (fornecedor_id,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail='Fornecedor nao encontrado')
        cur.close()
        return {'mensagem': 'Fornecedor excluido com sucesso'}

@router.post('/avaliacoes', status_code=201)
def criar_avaliacao(payload: AvaliacaoCreate, usuario=Depends(usuario_atual)):
    nota_final = round(payload.nota_ambiental * 0.35 + payload.nota_social * 0.30 + payload.nota_governanca * 0.35, 2)
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute('''INSERT INTO avaliacoes_fornecedor
            (fornecedor_id, data_avaliacao, nota_ambiental, nota_social, nota_governanca, nota_final, observacoes, criado_por)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id''',
            (payload.fornecedor_id, payload.data_avaliacao, payload.nota_ambiental, payload.nota_social,
             payload.nota_governanca, nota_final, payload.observacoes, usuario['id']))
        row = cur.fetchone()
        novo_id = row['id']
        cur.close()
        return {'id': novo_id, **payload.model_dump(), 'nota_final': nota_final}

@router.get('/ranking')
def ranking(usuario=Depends(usuario_atual)):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute('''
            SELECT f.id, f.razao_social, f.cnpj, f.segmento, f.nivel_risco,
                   a.nota_ambiental, a.nota_social, a.nota_governanca, a.nota_final, a.data_avaliacao
            FROM fornecedores f
            LEFT JOIN avaliacoes_fornecedor a ON a.id = (
                SELECT af.id FROM avaliacoes_fornecedor af
                WHERE af.fornecedor_id = f.id
                ORDER BY af.data_avaliacao DESC, af.id DESC
                LIMIT 1
            )
            ORDER BY a.nota_final DESC, f.razao_social ASC
        ''')
        rows = cur.fetchall()
        cur.close()
        for idx, row in enumerate(rows, start=1):
            row['posicao_ranking'] = idx
        return rows

@router.get('/dashboard')
def dashboard(usuario=Depends(usuario_atual)):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) AS total_fornecedores FROM fornecedores')
        total_fornecedores = cur.fetchone()['total_fornecedores']
        cur.execute('SELECT COUNT(DISTINCT fornecedor_id) AS total_avaliados FROM avaliacoes_fornecedor')
        total_avaliados = cur.fetchone()['total_avaliados']
        cur.execute('SELECT AVG(nota_final) AS media_score FROM avaliacoes_fornecedor')
        media = cur.fetchone()['media_score'] or 0
        cur.execute("SELECT COUNT(*) AS alertas_abertos FROM alertas WHERE status = 'ABERTO'")
        alertas_abertos = cur.fetchone()['alertas_abertos']
        cur.close()
        return {
            'total_fornecedores': total_fornecedores,
            'total_avaliados': total_avaliados,
            'media_score': round(float(media), 2),
            'alertas_abertos': alertas_abertos,
        }

@router.get('/certificacoes')
def certificacoes(usuario=Depends(usuario_atual)):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM certificacoes ORDER BY nome')
        rows = cur.fetchall()
        cur.close()
        return rows

@router.get('/alertas')
def alertas(usuario=Depends(usuario_atual)):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute('''SELECT a.*, f.razao_social FROM alertas a
                       LEFT JOIN fornecedores f ON f.id = a.fornecedor_id
                       ORDER BY a.data_criacao DESC''')
        rows = cur.fetchall()
        cur.close()
        return rows

@router.get('/configuracoes')
def configuracoes(usuario=Depends(usuario_atual)):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute('SELECT chave, valor FROM configuracoes ORDER BY chave')
        rows = cur.fetchall()
        cur.close()
        return rows

@router.post('/ml/prever-score')
def prever_score(payload: PrevisaoScoreRequest, usuario=Depends(usuario_atual)):
    return prever_score_esg(payload)
