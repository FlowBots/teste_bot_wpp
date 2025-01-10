from fastapi import APIRouter, HTTPException
from app.models.InstantMessageRequest import InstantMessageRequest
import requests
import logging
from pydantic import BaseModel
from app.models.SendStarterAgentTemplate import TemplateRequest  # Template da mensagem
from app.config import ACCESS_TOKEN, WHATSAPP_API_URL

router = APIRouter()


@router.post("/send-starter-agent")
def send_starter_agent_template(request: TemplateRequest):
    """
    Endpoint para enviar o template `starter_agent` sem variáveis.
    """
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": request.recipient,
        "type": "template",
        "template": {
            "name": "starter_agent",  # Nome do template
            "language": {"code": "pt_BR"},  # Idioma configurado no template
        },
    }
    # TODO Arurmar esse payload
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
