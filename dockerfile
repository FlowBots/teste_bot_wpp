FROM python

WORKDIR /app

# Copia o código para o diretório do container
COPY . .

# Instala as dependências com pip
RUN pip install -r requirements.txt

# Comando para rodar o servidor
CMD ["uvicorn", "__main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
