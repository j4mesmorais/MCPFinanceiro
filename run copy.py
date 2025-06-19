from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
#from fastapi.openapi.docs import get_swagger_ui_html
#from app.api.auth import router as auth_router
from app.api.pessoas import router as pessoas_router
from app.database import Base, engine

# cria tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MCP API",
    version="1.0.0",
    description="CRUD de Pessoas — autenticado por JWT"
)

# Swagger só aparece após fornecer token
#app.add_api_route(
#    "/docs",
#    lambda: get_swagger_ui_html(
#        openapi_url=app.openapi_url,
#        title="MCP API – Swagger",
#        oauth2_redirect_url=None
#    ),
#    include_in_schema=False
#)

#app.include_router(auth_router)
app.include_router(pessoas_router)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    # Gera o schema base
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    # Define o security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    # Aplica o security globalmente a todas as operações
    openapi_schema["security"] = [{"bearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Sobrescreve o método init do OpenAPI
app.openapi = custom_openapi