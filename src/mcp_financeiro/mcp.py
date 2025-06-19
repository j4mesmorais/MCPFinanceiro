import json
from typing import Callable, Dict, Any, List

from fastapi import APIRouter, Request
from starlette.responses import StreamingResponse

from database import get_session
from services.people import (
    create_person,
    get_person,
    list_people,
    update_person,
    delete_person,
)

router = APIRouter()

# Mapping of JSON-RPC method names to service functions and metadata
TOOLS: Dict[str, Dict[str, Any]] = {
    "create_person": {
        "func": create_person,
        "params": ["name", "email"],
        "description": "Create a new Person record",
    },
    "get_person": {
        "func": get_person,
        "params": ["person_id"],
        "description": "Retrieve a Person by ID",
    },
    "list_people": {
        "func": list_people,
        "params": [],
        "description": "List all Person records",
    },
    "update_person": {
        "func": update_person,
        "params": ["person_id", "name", "email"],
        "description": "Update fields of a Person",
    },
    "delete_person": {
        "func": delete_person,
        "params": ["person_id"],
        "description": "Delete a Person by ID",
    },
}


@router.get("/mcp/tools")
def describe_tools() -> List[Dict[str, Any]]:
    """Return metadata about available JSON-RPC tools."""
    return [
        {
            "name": name,
            "params": meta["params"],
            "description": meta["description"],
        }
        for name, meta in TOOLS.items()
    ]


@router.post("/mcp")
async def handle_rpc(request: Request) -> StreamingResponse:
    """Handle a JSON-RPC request and return the response via SSE."""
    payload = await request.json()
    method = payload.get("method")
    params = payload.get("params", {}) or {}
    rpc_id = payload.get("id")

    if method not in TOOLS:
        response = {
            "jsonrpc": "2.0",
            "id": rpc_id,
            "error": {"code": -32601, "message": "Method not found"},
        }
    else:
        # Acquire a DB session using the existing dependency
        db_gen = get_session()
        db = next(db_gen)
        try:
            result = TOOLS[method]["func"](db, **params)
            # SQLAlchemy models are not JSON serializable by default
            if hasattr(result, "__dict__"):
                result = result.__dict__
            elif isinstance(result, list):
                result = [r.__dict__ if hasattr(r, "__dict__") else r for r in result]

            response = {"jsonrpc": "2.0", "id": rpc_id, "result": result}
        finally:
            db_gen.close()

    async def event_generator():
        yield f"data: {json.dumps(response)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


__all__ = ["router"]
