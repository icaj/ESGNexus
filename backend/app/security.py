import secrets
from typing import Dict
from fastapi import Header, HTTPException
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
TOKENS: Dict[str, dict] = {}


def verificar_senha(senha: str, senha_hash: str) -> bool:
    return pwd_context.verify(senha, senha_hash)


def gerar_token(usuario: dict) -> str:
    token = secrets.token_urlsafe(32)
    TOKENS[token] = {"id": usuario["id"], "email": usuario["email"], "nome": usuario["nome"], "perfil": usuario["perfil"]}
    return token


def obter_usuario_logado(authorization: str | None = Header(default=None)):
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Token nao informado")
    token = authorization.split(" ", 1)[1]
    usuario = TOKENS.get(token)
    if not usuario:
        raise HTTPException(status_code=401, detail="Token invalido ou expirado")
    return usuario
