from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    senha: str

class TokenResponse(BaseModel):
    token: str
    tipo: str = 'Bearer'
    usuario: dict

class FornecedorBase(BaseModel):
    razao_social: str
    nome_fantasia: Optional[str] = None
    cnpj: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    nome_contato: Optional[str] = None
    segmento: Optional[str] = None
    categoria: Optional[str] = None
    pais: Optional[str] = 'Brasil'
    estado: Optional[str] = None
    cidade: Optional[str] = None
    nivel_risco: Optional[str] = 'MEDIO'
    status: Optional[str] = 'ATIVO'

class FornecedorCreate(FornecedorBase):
    pass

class FornecedorUpdate(FornecedorBase):
    razao_social: Optional[str] = None

class AvaliacaoCreate(BaseModel):
    fornecedor_id: int
    data_avaliacao: date
    nota_ambiental: float = 0
    nota_social: float = 0
    nota_governanca: float = 0
    observacoes: Optional[str] = None

class PrevisaoScoreRequest(BaseModel):
    nota_ambiental: float
    nota_social: float
    nota_governanca: float
    quantidade_certificacoes: int = 0
    nivel_risco: str = 'MEDIO'
