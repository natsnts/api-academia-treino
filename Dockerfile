# Usa a imagem oficial do Python
FROM python:3.12-slim

# Evita geração de arquivos .pyc e garante logs em tempo real no container
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia e instala as dependências primeiro (aproveita cache de camadas do Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY app.py .

# Expõe a porta configurada no Flask (app.py)
EXPOSE 8080

# Define o comando para rodar a aplicação
CMD ["python", "app.py"]
