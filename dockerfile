FROM python

WORKDIR /app

# Copia o código para o diretório do container
COPY . .

# Define argumentos para variáveis de ambiente (usados no build)
ARG TOKEN_META
ARG PHONE_NUMBER_ID
ARG VERIFY_TOKEN

# Configura variáveis de ambiente no container
ENV TOKEN_META=${TOKEN_META}
ENV PHONE_NUMBER_ID=${PHONE_NUMBER_ID}
ENV VERIFY_TOKEN=${VERIFY_TOKEN}

# Instala as dependências com pip
RUN pip install -r requirements.txt

# Comando para rodar o servidor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
