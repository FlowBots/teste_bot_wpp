FROM python

WORKDIR /app

COPY . .

# Instala as dependências com pip
RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]