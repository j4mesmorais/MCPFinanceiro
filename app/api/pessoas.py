from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.pessoa import PessoaCreate, PessoaOut, PessoaUpdate
from app.crud.pessoa import create_pessoa, get_pessoa, list_pessoas, update_pessoa
from app.crud.pessoa import delete_pessoa
#from app.api.deps import get_db, get_current_user

from fastapi import Security
from app.api.deps import get_db, get_current_user

#router = APIRouter(prefix="/pessoas", tags=["pessoas"], dependencies=[Depends(get_current_user)])

router = APIRouter(
     prefix="/pessoas",
     tags=["pessoas"],
    dependencies=[Security(get_current_user)] 
 )


@router.post("/", response_model=PessoaOut, 
    status_code=status.HTTP_201_CREATED,
    operation_id="createPessoa"
)
def criar(p: PessoaCreate, db: Session = Depends(get_db)):
    return create_pessoa(db, p)

@router.get("/", response_model=list[PessoaOut],
    operation_id="listPessoas"
)

def listar(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return list_pessoas(db, skip, limit)

@router.get("/{id}", response_model=PessoaOut,
    operation_id="getPessoaById"
)

def buscar(id: int, db: Session = Depends(get_db)):
    obj = get_pessoa(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")
    return obj

@router.patch("/{id}", response_model=PessoaOut,
    operation_id="updatePessoa"
)

def alterar(id: int, p: PessoaUpdate, db: Session = Depends(get_db)):
    obj = update_pessoa(db, id, p)
    if not obj:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")
    return obj

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT,
    operation_id="deletePessoa"
)
def remover(id: int, db: Session = Depends(get_db)):
    ok = delete_pessoa(db, id)
    if not ok:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")
    return  # 204 No Content