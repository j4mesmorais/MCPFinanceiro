# app/api/mcp.py
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sse_starlette.sse import EventSourceResponse
import json

router = APIRouter()
auth = HTTPBearer()

@router.get("/stream")
async def stream(creds: HTTPAuthorizationCredentials = Depends(auth)):
    async def event_generator():
        yield json.dumps({"event": "ready", "message": "MCP Server pronto"})
        # aqui você poderia expandir para processar mensagens via SSE…
    return EventSourceResponse(event_generator())
