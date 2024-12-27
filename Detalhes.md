### Criar ambiente
python -m venv venv

source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows


### Instalar as bibliotecas

pip install fastapi uvicorn apscheduler sqlalchemy pydantic python-dotenv requests

### Executar serviço

uvicorn main:app --reload


### Ajustar ENV

WHATSAPP_API_URL=
ACCESS_TOKEN=
DATABASE_URL=
APP_ID=
APP_SECRET=

### Rotas implementaadas

- POST /schedule-message

- GET /logs