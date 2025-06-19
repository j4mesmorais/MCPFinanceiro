from datetime import datetime, date
from sqlalchemy import Column, Integer, String, DateTime, Date

from database import Base


class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=True, unique=True)
    celular = Column(String(20), nullable=True)
    endereco = Column(String(200), nullable=True)
    tipo = Column(String(1), nullable=True)
    status = Column(String(10), nullable=True)
    cpf_cnpj = Column(String(20), nullable=True)
    dt_nascimento = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


__all__ = ["Person"]
