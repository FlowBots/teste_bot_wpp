from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field, validator
from datetime import datetime, timezone
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.triggers.date import DateTrigger
from typing import Dict
import logging
import uuid
import requests
import os
from dotenv import load_dotenv
import certifi

os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

# Carregar variáveis de ambiente
load_dotenv()

# Configurações iniciais
app = FastAPI(title="Chatbot WhatsApp Scheduler")
logging.basicConfig(level=logging.INFO)

# Banco de dados SQLite para armazenamento de agendamentos
DATABASE_URL = os.getenv("DATABASE_URL")

# Configurações da API do WhatsApp
WHATSAPP_API_URL = os.getenv("WHATSAPP_API_URL")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

# Autenticação via API Key
API_KEY = os.getenv("API_KEY")

# Token de verificação fornecido no Meta Developers
VERIFY_TOKEN = "12345"

scheduler = BackgroundScheduler(jobstores={"default": SQLAlchemyJobStore(url=DATABASE_URL)})
scheduler.start()

# Modelo de Dados para a Requisição
class ScheduleMessageRequest(BaseModel):
    recipient: str = Field(..., description="Número do destinatário no formato E.164", example="+5511999999999")
    message: str = Field(..., description="Mensagem a ser enviada")
    send_time: datetime = Field(..., description="Data e hora do envio no formato ISO 8601", example="2024-12-25T15:30:00")
    
    @validator("recipient")
    def validate_recipient(cls, value):
        if not value.startswith("+") or not value[1:].isdigit():
            raise ValueError("Número do destinatário deve estar no formato E.164 (ex: +5511999999999)")
        return value
    
    @validator("send_time")
    def validate_send_time(cls, value):
        now = datetime.now(timezone.utc)
        logging.info(f"Horário atual (UTC): {now}")
        logging.info(f"Horário fornecido (UTC): {value}")
        
        # Certifique-se de que o valor seja "offset-aware" (com fuso horário)
        if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
            value = value.replace(tzinfo=timezone.utc)
        
        if value <= now:
            raise ValueError("O horário de envio deve ser no futuro")
        return value

def authenticate(api_key: str):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

# Função Simulada de Envio de Mensagem
def send_message(job_id: str, recipient: str, message: str):
    logging.info(f"Enviando mensagem para {recipient}: {message}")

    # Aqui integraria com a API do WhatsApp
    """
    Envia uma mensagem de texto pelo WhatsApp utilizando a API oficial.

    Args:
        job_id (str): ID do trabalho agendado.
        recipient (str): Número do destinatário no formato E.164.
        message (str): Conteúdo da mensagem.
    """
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient,
        "type": "template",
        "template": {
            "name": "hello_world", "language": { "code": "en_US" }
        }
    }

    try:
        response = requests.post(WHATSAPP_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        logging.info(f"Mensagem enviada com sucesso: {response.json()}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao enviar mensagem para {recipient}: {str(e)}")
        logging.debug(f"Payload enviado: {payload}")

# Endpoint para agendamento
@app.post("/schedule-message", status_code=201)
def schedule_message(
    request: ScheduleMessageRequest, 
    #api_key: str = Depends(authenticate)
):
    try:
        schedule_id = str(uuid.uuid4())
        scheduler.add_job(
            send_message,
            trigger=DateTrigger(run_date=request.send_time),
            id=schedule_id,
            kwargs={
                "job_id": schedule_id,
                "recipient": request.recipient,
                "message": request.message,
            },
        )
        return {
            "status": "success",
            "message": "Mensagem agendada com sucesso",
            "schedule_id": schedule_id,
        }
    except Exception as e:
        logging.error(f"Erro ao agendar mensagem: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao agendar mensagem")

# Logs de sucesso e erro
@app.get("/logs", status_code=200)
def get_logs(api_key: str = Depends(authenticate)):
    return {"logs": "Aqui você pode retornar logs ou integrar com um sistema de monitoramento."}

# Rota para validar o Webhook no Meta
@app.get("/webhook")
async def validate_webhook(request: Request):
    params = request.query_params
    hub_mode = params.get("hub.mode")
    hub_verify_token = params.get("hub.verify_token")
    hub_challenge = params.get("hub.challenge")

    # Log para depuração
    logging.info(f"Recebido: hub_mode={hub_mode}, hub_verify_token={hub_verify_token}, hub_challenge={hub_challenge}")

    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return PlainTextResponse(hub_challenge)  # Retorna o desafio como texto puro
    return {"error": "Token de verificação inválido"}

# Encerramento do agendador ao finalizar o app
@app.on_event("shutdown")
def shutdown():
    scheduler.shutdown()
