from pydantic import BaseModel,Field
from typing import Optional
from app.models.pessoa import Tipo, Status

class PessoaBase(BaseModel):
    nome: Optional[str]
    celular: Optional[str]
    endereco: Optional[str]
    tipo: Optional[Tipo]
    status: Optional[Status]
    cpf_cnpj: Optional[str]

class PessoaCreate(PessoaBase):
    nome: str = Field(..., title="Nome Completo")
    tipo: Tipo = Field(..., title="Tipo (C ou F)")
    celular: Optional[str] = Field(None, title="Celular")
    endereco: Optional[str] = Field(None, title="Endereço")
    status: Status = Field(Status.Ativo, title="Status")
    cpf_cnpj: Optional[str] = Field(None, title="CPF ou CNPJ")
    class Config:
        title = "PessoaCreate"

class PessoaUpdate(PessoaBase):
    nome: Optional[str] = Field(None, title="Nome Completo")
    tipo: Optional[Tipo] = Field(None, title="Tipo (C ou F)")
    celular: Optional[str] = Field(None, title="Celular")
    endereco: Optional[str] = Field(None, title="Endereço")
    status: Optional[Status] = Field(None, title="Status")
    cpf_cnpj: Optional[str] = Field(None, title="CPF ou CNPJ")

    class Config:
        title = "PessoaUpdate"

class PessoaOut(PessoaBase):
    id: int = Field(..., title="ID")
    nome: str = Field(..., title="Nome Completo")
    tipo: Tipo = Field(..., title="Tipo (C ou F)")
    celular: Optional[str] = Field(None, title="Celular")
    endereco: Optional[str] = Field(None, title="Endereço")
    status: Status = Field(..., title="Status")
    cpf_cnpj: Optional[str] = Field(None, title="CPF ou CNPJ")

    class Config:
        orm_mode = True
        title = "PessoaOut"
