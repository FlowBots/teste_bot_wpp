### Instalar as bibliotecas

pip install fastapi uvicorn apscheduler sqlalchemy pydantic python-dotenv requests


### Executar serviço
python -m venv venv

source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

uvicorn main:app --reload


### Ajustar ENV

WHATSAPP_API_URL=
ACCESS_TOKEN=
DATABASE_URL=
API_KEY=

### Rotas implementaadas

- POST /schedule-message

- GET /logs