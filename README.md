# MCPFinanceiro

Servidor de MCP de administração de lançamentos financeiros contábeis. O projeto
é composto por um pequeno pacote Python que inicializa a configuração da
aplicação via variáveis de ambiente e disponibiliza utilidades de acesso a
um banco de dados usando SQLAlchemy.

## Ambiente de desenvolvimento

1. Garanta que possui **Python 3.8** ou superior instalado.
2. Crie e ative um ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Instale as dependências do projeto (SQLAlchemy e python-dotenv).  Caso
   deseje utilizar migrações de banco, inclua também o Alembic:

```bash
pip install sqlalchemy python-dotenv alembic
```

4. Copie o arquivo `.env.example` para `.env` e ajuste os valores de `JWT_SECRET`
   e `DB_URL` conforme sua necessidade. A chave `JWT_SECRET` é utilizada para
   assinar tokens JWT no algoritmo **HS256**.

## Banco de dados

O arquivo `database.py` define a conexão utilizando SQLAlchemy. Por padrão é
criado um banco **SQLite** local (`mcp.db`). Para utilizar PostgreSQL ou outro
banco de dados, defina a variável de ambiente `DB_URL` com a string de conexão.

```bash
export DB_URL=postgresql://usuario:senha@localhost:5432/minha_base
```

### Migrações com Alembic

Caso deseje versionar e aplicar mudanças de esquema no banco, utilize o
[Alembic](https://alembic.sqlalchemy.org/):

```bash
pip install sqlalchemy alembic
alembic init alembic
# edite o arquivo `alembic/env.py` para importar a `Base` do projeto e definir
# `target_metadata`. Isso é necessário para que o comando `--autogenerate`
# consiga detectar as alterações nos modelos.
#
# ```python
# from pathlib import Path
# import sys
# sys.path.append(str(Path(__file__).resolve().parents[1]))
# from database import Base
# target_metadata = Base.metadata
# ```
#
# Com o `env.py` configurado, ajuste o `alembic.ini` e gere as revisões
alembic revision --autogenerate -m "mensagem"
alembic upgrade head
```
Esses comandos geram arquivos de revisão na pasta `alembic` e aplicam o
upgrade para a versão mais recente do schema.

### Atualizando o banco de dados

Quando novas colunas ou tabelas são adicionadas aos modelos, é necessário gerar
uma revisão e aplicá-la para manter o banco sincronizado:

```bash
alembic revision --autogenerate -m "minhas alterações"
alembic upgrade head
```

Se a aplicação reportar `sqlalchemy.exc.OperationalError` informando que uma
coluna não existe (por exemplo `no such column: people.celular`), o banco de
dados provavelmente está desatualizado e precisa das migrações acima.

## Autenticação JWT

A aplicação protege as rotas REST utilizando tokens JWT. Obtenha um token em
`/token` e use o botão **Authorize** do Swagger UI informando o valor no formato
`Bearer <token>`. A chave utilizada para assinar os tokens é configurada através
da variável `JWT_SECRET` presente no `.env`.

## MCP e n8n

Além das rotas REST tradicionais, a aplicação expõe a rota `/mcp` que segue o
**Model Context Protocol** utilizando JSON-RPC 2.0 sobre **Server-Sent Events**.
O endpoint `/mcp/tools` retorna a lista de operações disponíveis como "tools",
permitindo que o nó **MCP Client Tool** do n8n descubra cada operação CRUD.
Para invocar uma operação envie uma requisição JSON-RPC para `/mcp` e aguarde o
resultado ser emitido via SSE.


