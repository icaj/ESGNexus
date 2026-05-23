from datetime import datetime, timedelta
from uuid import uuid4
from fastapi import Header, HTTPException
from passlib.hash import bcrypt
from app.config import settings
from app.db.connection import get_connection

_tokens: dict[str, dict] = {}

def autenticar(email: str, senha: str) -> dict:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute('''
            SELECT u.id, u.nome, u.email, u.senha_hash, u.ativo, p.nome AS perfil
            FROM usuarios u
            JOIN perfis p ON p.id = u.perfil_id
            WHERE u.email = %s
        ''', (email,))
        usuario = cur.fetchone()
        cur.close()
    if not usuario or not usuario['ativo'] or not bcrypt.verify(senha, usuario['senha_hash']):
        raise HTTPException(status_code=401, detail='Credenciais invalidas')
    token = str(uuid4())
    usuario_publico = {k: usuario[k] for k in ('id', 'nome', 'email', 'perfil')}
    _tokens[token] = {
        'usuario': usuario_publico,
        'expira_em': datetime.utcnow() + timedelta(minutes=settings.token_expiration_minutes)
    }
    return {'token': token, 'usuario': usuario_publico}

def usuario_atual(authorization: str | None = Header(default=None)) -> dict:
    if not authorization or not authorization.lower().startswith('bearer '):
        raise HTTPException(status_code=401, detail='Token nao informado')
    token = authorization.split(' ', 1)[1]
    sessao = _tokens.get(token)
    if not sessao or sessao['expira_em'] < datetime.utcnow():
        _tokens.pop(token, None)
        raise HTTPException(status_code=401, detail='Token invalido ou expirado')
    return sessao['usuario']
