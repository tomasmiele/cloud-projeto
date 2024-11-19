# Use a imagem oficial do Python
FROM python:3.12

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de dependências e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código para o container
COPY app .

# Exponha a porta onde o FastAPI rodará
EXPOSE 8000

# Comando para iniciar a aplicação FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
