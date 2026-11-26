# Usa a imagem oficial do Python
FROM python:3.12-slim

# Evita geração de arquivos .pyc e garante logs em tempo real no container
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Cria um usuário de sistema comum chamado "appuser" (Resolve a vulnerabilidade)
RUN useradd -m appuser

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia e instala as dependências como root (para uso global no container)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação e passa a posse para o appuser
COPY --chown=appuser:appuser app.py .

# Expõe a porta configurada no Flask (app.py)
EXPOSE 8080

# Muda do usuário root para o usuário comum antes de rodar a API
USER appuser

# Define o comando para rodar a aplicação
CMD ["python", "app.py"]