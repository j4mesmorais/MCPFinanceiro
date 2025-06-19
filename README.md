# MCPFinanceiro
Servidor de MCP de administração de lançamentos financeiros contabeis

## Banco de Dados
O arquivo `database.py` usa SQLAlchemy para gerenciar as conexões. Por padrao o
projeto cria um banco SQLite local (`mcp.db`). Para utilizar PostgreSQL ou outro
banco defina a variavel de ambiente `DB_URL` com a string de conexao, por
exemplo:

```bash
export DB_URL=postgresql://usuario:senha@localhost:5432/minha_base
```

### Migracoes com Alembic
Para criar e atualizar estruturas de banco utilize o [Alembic](https://alembic.sqlalchemy.org/):

```bash
pip install sqlalchemy alembic
alembic init alembic
# configure o arquivo alembic.ini e gere as revisoes
alembic revision --autogenerate -m "mensagem"
alembic upgrade head
```


## Testes
Para executar a suíte de testes utilize o [pytest](https://pytest.org/):

```bash
pytest
```
