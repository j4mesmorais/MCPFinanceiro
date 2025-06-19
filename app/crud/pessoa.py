from sqlalchemy.orm import Session
from app.models.pessoa import Pessoa
from app.schemas.pessoa import PessoaCreate, PessoaUpdate

def create_pessoa(db: Session, obj: PessoaCreate):
    p = Pessoa(**obj.dict())
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

def get_pessoa(db: Session, pessoa_id: int):
    return db.query(Pessoa).filter(Pessoa.id == pessoa_id).first()

def list_pessoas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Pessoa).offset(skip).limit(limit).all()

def update_pessoa(db: Session, pessoa_id: int, obj: PessoaUpdate):
    p = get_pessoa(db, pessoa_id)
    if not p:
        return None
    for field, value in obj.dict(exclude_unset=True).items():
        setattr(p, field, value)
    db.commit()
    db.refresh(p)
    return p

def delete_pessoa(db: Session, pessoa_id: int) -> bool:
    p = db.query(Pessoa).filter(Pessoa.id == pessoa_id).first()
    if not p:
        return False
    db.delete(p)
    db.commit()
    return True