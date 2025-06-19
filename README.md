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
   deseje utilizar migrações de banco, inclua também o pacote
   **sqlalchemy-migrate**:

```bash
pip install sqlalchemy python-dotenv sqlalchemy-migrate
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

### Migrações com ``migrate``

Para manter o esquema de banco sincronizado sem utilizar o Alembic, foi adicionado
um pequeno script ``migrate_db.py``. Ele apenas cria todas as tabelas definidas
nos modelos se ainda não existirem. Para executá‑lo:

```bash
python migrate_db.py
```

Esse comando garante que o banco de dados possua as tabelas necessárias.

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


