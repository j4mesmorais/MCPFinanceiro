import os
import json
from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse

router = APIRouter()
auth = HTTPBearer()

@router.get("/stream")
async def stream(request: Request):
    async def event_generator():
        yield json.dumps({"event": "ready", "message": "MCP Server pronto"})

    if os.getenv("DISABLE_AUTH", "false").lower() == "true":
        # 🔓 Sem autenticação
        return EventSourceResponse(event_generator())

    # 🔐 Com autenticação via header Authorization
    creds: HTTPAuthorizationCredentials = await auth(request)
    if not creds or not creds.credentials:
        return JSONResponse(status_code=403, content={"detail": "Not authenticated"})

    # Aqui você pode validar o token se quiser, ex: decode_jwt(creds.credentials)
    return EventSourceResponse(event_generator())
