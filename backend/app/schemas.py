from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    senha: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class FornecedorBase(BaseModel):
    razao_social: str
    nome_fantasia: Optional[str] = None
    cnpj: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    nome_contato: Optional[str] = None
    segmento: Optional[str] = None
    categoria: Optional[str] = None
    estado: Optional[str] = None
    cidade: Optional[str] = None
    nivel_risco: Optional[str] = "MEDIO"
    status: Optional[str] = "ATIVO"


class FornecedorCreate(FornecedorBase):
    pass


class FornecedorUpdate(FornecedorBase):
    pass


class AvaliacaoCreate(BaseModel):
    fornecedor_id: int
    data_avaliacao: Optional[date] = None
    nota_ambiental: float
    nota_social: float
    nota_governanca: float
    observacoes: Optional[str] = None


class CertificacaoCreate(BaseModel):
    fornecedor_id: int
    nome: str
    orgao_emissor: Optional[str] = None
    data_emissao: Optional[date] = None
    data_validade: Optional[date] = None
    status: Optional[str] = "VALIDA"
    url_arquivo: Optional[str] = None


class MlPrevisaoRequest(BaseModel):
    nota_ambiental: float
    nota_social: float
    nota_governanca: float
    quantidade_certificacoes: int = 0
    nivel_risco: str = "MEDIO"
