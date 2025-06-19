from pydantic import BaseModel
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
    nome: str 
    tipo: Tipo    
    status: Status = Status.Ativo    
    celular: Optional[str] = None
    endereco: Optional[str] = None
    cpf_cnpj: Optional[str] = None

class PessoaUpdate(PessoaBase):
    pass  # todos campos opcionais para partial update

class PessoaOut(PessoaBase):
    id: int
    nome: str 
    tipo: Tipo
    status: Status    
    class Config:
        orm_mode = True
