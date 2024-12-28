from fastapi import FastAPI, HTTPException, Depends, Request, Query
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field, validator
from datetime import datetime, timezone
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from typing import Dict
import logging
import uuid
import requests
import os
from dotenv import load_dotenv
import certifi
import pytz

# Configurando o timezone de Brasília
BRASILIA_TZ = pytz.timezone("America/Sao_Paulo")

# Configuração de logging
LOG_FILE = "app_logs.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()  # Continua exibindo no console
    ]
)
logging.info("Servidor iniciado e logging configurado.")

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
APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")

# Token de verificação fornecido no Meta Developers
VERIFY_TOKEN = "12345"

scheduler = BackgroundScheduler(jobstores={"default": SQLAlchemyJobStore(url=DATABASE_URL)})
scheduler.start()

# Função para atualizar o token de acesso
def update_access_token():
    global ACCESS_TOKEN
    logging.info("Iniciando renovação do token de acesso.")
    try:
        url = "https://graph.facebook.com/v14.0/oauth/access_token"
        params = {
            "grant_type": "fb_exchange_token",
            "client_id": APP_ID,
            "client_secret": APP_SECRET,
            "fb_exchange_token": ACCESS_TOKEN,
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        ACCESS_TOKEN = data.get("access_token")
        logging.info("Token de acesso atualizado com sucesso.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao renovar o token de acesso: {str(e)}")

def get_expiration_time():
    url = "https://graph.facebook.com/v14.0/oauth/access_token"
    params = {
        "grant_type": "fb_exchange_token",
        "client_id": APP_ID,
        "client_secret": APP_SECRET,
        "fb_exchange_token": ACCESS_TOKEN,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("expires_in")

# Agendar renovação do token de acesso
scheduler.add_job(
    update_access_token,
    trigger=IntervalTrigger(hours=1),  # Ajuste conforme a validade do token
    id="update_access_token_job",
    replace_existing=True
)

# Modelo de Dados para a Requisição
class ScheduleMessageRequest(BaseModel):
    recipient: str = Field(..., description="Número do destinatário no formato E.164", example="+5555997013555")
    message: str = Field(..., description="Mensagem a ser enviada")
    send_time: datetime = Field(..., description="Data e hora do envio no formato ISO 8601", example="2024-12-27T15:30:00")
    
    @validator("recipient")
    def validate_recipient(cls, value):
        logging.info(f"Validando destinatário: {value}")
        if not value.startswith("+") or not value[1:].isdigit():
            logging.error("Número de destinatário inválido.")
            raise ValueError("Número do destinatário deve estar no formato E.164 (ex: +5511999999999)")
        return value
    
    @validator("send_time")
    def validate_send_time(cls, value):
        # Obter o horário atual no fuso horário de Brasília
        now_brasilia = datetime.now(BRASILIA_TZ)
        logging.info(f"Horário atual (Brasília): {now_brasilia}")

        # Certificar que o horário fornecido é "offset-aware" (com fuso horário)
        if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
            value = BRASILIA_TZ.localize(value)

        logging.info(f"Horário fornecido 'offset-aware': {value}")

        # Comparar o horário ajustado com o horário atual de Brasília
        if value <= now_brasilia:
            logging.error("O horário de envio está no passado.")
            raise ValueError("O horário de envio deve ser no futuro")
        
        return value  # Retorna o horário original
    
# Modelo de Dados para a Requisição de Mensagem Instantânea
class InstantMessageRequest(BaseModel):
    recipient: str = Field(..., description="Número do destinatário no formato E.164", example="+5555997013555")
    message: str = Field(..., description="Mensagem a ser enviada")

    @validator("recipient")
    def validate_recipient(cls, value):
        logging.info(f"Validando destinatário: {value}")
        if not value.startswith("+") or not value[1:].isdigit():
            logging.error("Número de destinatário inválido.")
            raise ValueError("Número do destinatário deve estar no formato E.164 (ex: +5511999999999)")
        return value

# Função Simulada de Envio de Mensagem Agendada
def send_message(job_id: str, recipient: str, message: str):
    logging.info(f"Iniciando envio de mensagem - Job ID: {job_id}, Destinatário: {recipient}: {message}")

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
        logging.info(f"Mensagem enviada com sucesso para {recipient}. Resposta: {response.json()}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao enviar mensagem para {recipient}: {str(e)}")
        logging.debug(f"Payload enviado: {payload}")
        raise HTTPException(status_code=500, detail="Erro ao enviar a mensagem")
    

# Função Simulada de Envio de Mensagem
def send_message_instant(recipient: str, message: str):
    logging.info(f"Iniciando envio de mensagem para o destinatário: {recipient}: {message}")

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
        logging.info(f"Mensagem enviada com sucesso para {recipient}. Resposta: {response.json()}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao enviar mensagem para {recipient}: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao enviar a mensagem")

# Endpoint para verificação do token atual
@app.get("/current-token")
def get_current_token():
    return {"access_token": ACCESS_TOKEN}

# Endpoint para pegar tempo de expiração do token
@app.get("/expiration-time")
def expiration_time():
    expiration_time = get_expiration_time()
    return {"expiration_time": expiration_time}

# Endpoint para renovar o token de acesso
@app.get("/update-token")
def update_token():
    global ACCESS_TOKEN
    update_access_token()    
    return {"access_token": ACCESS_TOKEN}

# Endpoint para envio instantâneo de mensagens
@app.post("/send-message", status_code=200)
def send_instant_message(request: InstantMessageRequest):
    try:
        response = send_message_instant(request.recipient, request.message)
        logging.info(f"Mensagem enviada com sucesso para {request.recipient}. Resposta: {request.message}")
        return {"status": "success", "response": response}
    except Exception as e:
        logging.error(f"Erro ao enviar mensagem instantânea: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao enviar mensagem instantânea")

# Endpoint para agendamento
@app.post("/schedule-message", status_code=201)
def schedule_message(
    request: ScheduleMessageRequest, 
    #api_key: str = Depends(authenticate)
):
    try:
        schedule_id = str(uuid.uuid4())
        logging.info(f"Agendando mensagem - ID: {schedule_id}, Destinatário: {request.recipient}, Horário: {request.send_time}")
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
        logging.info(f"Mensagem agendada com sucesso - ID: {schedule_id} HORÁRIO: {request.send_time}")
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
def get_logs(
    level: str = Query("INFO", description="Nível do log (INFO, ERROR, DEBUG, etc.)"),
    keyword: str = Query(None, description="Palavra-chave para filtrar os logs (opcional)"),
    lines: int = Query(50, description="Número de linhas de log para retornar")
):
    """
    Retorna os logs armazenados no arquivo com filtros opcionais.
    """
    logging.info(f"Logs acessados - Nível: {level}, Palavra-chave: {keyword}, Linhas: {lines}")
    try:
        with open(LOG_FILE, "r") as log_file:
            logs = log_file.readlines()

        # Filtro por nível de log
        filtered_logs = [log for log in logs if f"- {level.upper()} -" in log]

        # Filtro por palavra-chave, se especificado
        if keyword:
            filtered_logs = [log for log in filtered_logs if keyword in log]

        # Retorna apenas as últimas `lines` linhas
        return {"logs": filtered_logs[-lines:]}
    except Exception as e:
        logging.error(f"Erro ao acessar os logs: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao acessar os logs")

# Rota para validar o Webhook no Meta
@app.get("/webhook")
async def validate_webhook(request: Request):
    params = request.query_params
    logging.info(f"Webhook recebido - Parâmetros: {params}")

    hub_mode = params.get("hub.mode")
    hub_verify_token = params.get("hub.verify_token")
    hub_challenge = params.get("hub.challenge")

    # Log para depuração
    logging.info(f"Recebido: hub_mode={hub_mode}, hub_verify_token={hub_verify_token}, hub_challenge={hub_challenge}")

    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        logging.info("Webhook validado com sucesso.")
        return PlainTextResponse(hub_challenge)  # Retorna o desafio como texto puro
    else:
        logging.warning("Falha ao validar o webhook. Token de verificação inválido.")
        return {"error": "Token de verificação inválido"}

# Encerramento do agendador ao finalizar o app
@app.on_event("shutdown")
def shutdown():
    logging.info("Aplicação finalizando. Scheduler será desligado.")
    scheduler.shutdown()
