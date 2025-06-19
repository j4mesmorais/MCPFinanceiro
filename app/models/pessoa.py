from sqlalchemy import Column, Integer, String, Enum
from enum import Enum as PyEnum
from app.database import Base

class Tipo(PyEnum):
    C = "C"   # Cliente
    F = "F"   # Fornecedor

class Status(PyEnum):
    Ativo = "Ativo"
    Cancelado = "Cancelado"

class Pessoa(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, index=True) 
    celular = Column(String, nullable=True, unique=True)
    endereco = Column(String, nullable=True)
    tipo = Column(Enum(Tipo), nullable=False)
    status = Column(Enum(Status), nullable=False, default=Status.Ativo)
    cpf_cnpj = Column(String, nullable=True, unique=True)
