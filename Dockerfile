# 1. Use uma imagem Python leve
FROM python:3.11-slim

# 2. Defina diretório de trabalho
WORKDIR /app

# 3. Copie somente o requirements e instale dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copie o restante do código
COPY . .

# 5. Exponha a porta (uvicorn rodará na 80)
EXPOSE 80

# 6. Comando de inicialização
CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "80"]
