#!/bin/bash

# Criar ambiente virtual
python3 -m venv venv

# Ativar o ambiente virtual
source venv/bin/activate

# Instalar as bibliotecas
pip install fastapi uvicorn apscheduler sqlalchemy pydantic python-dotenv requests

# Executar o serviço
#uvicorn main:app --reload

uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --reload

