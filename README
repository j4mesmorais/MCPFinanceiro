# MCP API

API de CRUD de Pessoas protegida por JWT, construída com FastAPI, SQLAlchemy e Alembic.

## 🚀 Visão Geral

* **Linguagem**: Python 3.11
* **Framework**: FastAPI
* **Banco de Dados**: SQLite (`mcp.db`)
* **ORM**: SQLAlchemy + Alembic
* **Documentação**: Swagger UI (OpenAPI)
* **Autenticação**: JWT (Bearer)
* **Servidor MCP**: compatível com o MCP Client Tool do n8n, permitindo que fluxos de IA registrem clientes automaticamente no banco de dados via n8n

## 📂 Estrutura do Projeto

```
meu_projeto/
├── .env                      # Variáveis de ambiente
├── requirements.txt          # Dependências Python
├── Dockerfile                # Imagem Docker
├── docker-compose.yml        # Orquestração com Traefik
├── run.py                    # Entry-point do FastAPI
└── app/
    ├── config.py            # Pydantic Settings
    ├── database.py          # Engine, Session e Base
    ├── models/              # Modelos SQLAlchemy
    ├── schemas/             # Schemas Pydantic
    ├── crud/                # Funções de acesso ao BD
    └── api/                 # Rotas e dependências de segurança
```

## ⚙️ Pré-requisitos

* Python 3.11+
* pip
* Docker & Docker Compose (opcional para container)

## 🔧 Instalação Local

1. Clone o repositório:

   ```bash
   git clone <SEU_REPO_URL>
   cd meu_projeto
   ```
2. Crie e ative um virtualenv:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate.bat # Windows
   ```
3. Instale dependências:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
4. Configure seu `.env` (exemplo em `.env.example`):

   ```dotenv
   SECRET_KEY=uma_senha_supersecreta
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   DATABASE_URL=sqlite:///./mcp.db
   ```
5. Gere o banco e suba o servidor:

   ```bash
   uvicorn run:app --reload
   ```

## 🌐 Uso com Docker Compose

1. Build e up:

   ```bash
   docker-compose build
   docker-compose up -d
   ```
2. Acesse em `https://mcpfinanceiro.adjunto.com.br` ou `http://localhost:8000`.

## 📑 Documentação & Swagger UI

* **OpenAPI JSON**: `/openapi.json`
* **Swagger UI**: `/docs`

  * Clique em **Authorize**, cole apenas o JWT.
  * Depois faça chamadas às rotas de `/pessoas`.

## 🔐 Autenticação JWT

* **Esquema**: Bearer JWT
* **Components/securitySchemes**: `bearerAuth`
* As operações usam `Security(get_current_user)` e `global security` no OpenAPI.

### Geração de Token (externa)

Exemplo de geração manual:

```bash
python3 - << 'PYCODE'
import jwt, datetime
SECRET_KEY = "uma_senha_supersecreta"
ALGORITHM = "HS256"
payload = {"sub":"usuario", "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)}
print(jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM))
PYCODE
```

## 📝 Endpoints Principais

| Método | Rota            | Operation ID    | Descrição                 |
| ------ | --------------- | --------------- | ------------------------- |
| POST   | `/pessoas/`     | `createPessoa`  | Cria nova pessoa          |
| GET    | `/pessoas/`     | `listPessoas`   | Lista pessoas             |
| GET    | `/pessoas/{id}` | `getPessoaById` | Busca pessoa por ID       |
| PATCH  | `/pessoas/{id}` | `updatePessoa`  | Atualiza campos da pessoa |
| DELETE | `/pessoas/{id}` | `deletePessoa`  | Remove pessoa             |

## 📂 Migrações com Alembic

1. Inicializar repo:

   ```bash
   alembic init migrations
   ```
2. Criar migration:

   ```bash
   alembic revision --autogenerate -m "Descrição"
   ```
3. Aplicar:

   ```bash
   alembic upgrade head
   ```

## ⚖️ Licença

MIT License © **Adjunto Sistemas**
