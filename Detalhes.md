### Criar ambiente
python -m venv venv

source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows


### Instalar as bibliotecas

pip install pytz fastapi uvicorn apscheduler sqlalchemy pydantic python-dotenv requests

### Executar serviço

uvicorn main:app --reload

- Na hospedagem:

uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --reload

### Ajustar ENV

WHATSAPP_API_URL=
ACCESS_TOKEN=
DATABASE_URL=
APP_ID=
APP_SECRET=

### Rotas implementaadas

Endpoint João para envio de mensagem para usar de base correção

- POST /send-message-v-joao

Endpoint para verificação do token atual

- GET /current-token

Endpoint para pegar tempo de expiração do token

- GET /expiration-time

Endpoint para renovar o token de acesso

- GET /update-token

Endpoint para envio instantâneo de mensagens

- POST /send-message

Endpoint para agendamento

- POST /schedule-message

Endpoint para logs de sucesso e erro

- GET /logs

Endpoint para validar o Webhook no Meta

- GET /webhook