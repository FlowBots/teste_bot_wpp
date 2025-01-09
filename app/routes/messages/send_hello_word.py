from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
import logging

# Configurações
from app.config import ACCESS_TOKEN, WHATSAPP_API_URL

router = APIRouter()


# Modelo de requisição # MANDAR PARA A PASTA MODELS!!!!
class TemplateMessageRequest(BaseModel):
    recipient: str  # Número do destinatário no formato E.164


@router.post("/send-hello-world", tags=["Messages"],
    summary="Envia Template Hello World",
    description="Faz envio ao destinatário de uma mensagem template padrão Heloo World",)
def send_hello_word(request: TemplateMessageRequest):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": request.recipient,
        "type": "template",
        "template": {
            "name": "hello_world",  # Nome do template padrão do WhatsApp
            "language": {"code": "en_US"},  # Idioma configurado para o hello_world
        },
    }

    # Log do payload para depuração
    logging.info(f"Payload enviado para o WhatsApp: {payload}")

    try:
        response = requests.post(WHATSAPP_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        logging.info(
            f"Template enviado com sucesso para {request.recipient}. Resposta: {response.json()}"
        )
        return {"status": "success", "response": response.json()}
    except requests.exceptions.RequestException as e:
        if e.response is not None:
            logging.error(f"Erro ao enviar template: {e.response.text}")
        raise HTTPException(
            status_code=500, detail=f"Erro ao enviar template: {e.response.text}"
        )