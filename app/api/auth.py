from fastapi import APIRouter, HTTPException, status
from datetime import datetime, timedelta
import jwt
from app.config import settings
from pydantic import BaseModel

router = APIRouter(tags=["auth"])

class TokenRequest(BaseModel):
    username: str
    password: str

@router.post("/token")
def login(data: TokenRequest):
    # TODO: validar credenciais reais
    if data.username != "admin" or data.password != "senha":
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    exp = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = jwt.encode({"sub": data.username, "exp": exp}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}
