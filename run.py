from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.api.pessoas import router as pessoas_router
from app.database import Base, engine
from app.api.mcp import router as mcp_router
# Cria as tabelas no startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MCP API",
    version="1.0.0",
    description="CRUD de Pessoas — autenticado por JWT",
    swagger_ui_parameters={"persistAuthorization": True},  # persiste o token
)

# 1) Inclui todas as rotas de pessoas
app.include_router(pessoas_router)
app.include_router(mcp_router)
# 2) Gera o OpenAPI customizado, adicionando securitySchemes e security global
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    openapi_schema["security"] = [{"bearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# 3) Sobrescreve o método que o FastAPI usa para gerar o docs
app.openapi = custom_openapi
