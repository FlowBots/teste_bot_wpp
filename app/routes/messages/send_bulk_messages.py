from fastapi import APIRouter, HTTPException
import requests
from app.config import WHATSAPP_API_URL, ACCESS_TOKEN
from app.models.BulkMessageRequest import BulkMessageRequest
import logging

from app.services.send_message_template import send_message_template

router = APIRouter()

@router.post("/messages/bulk", status_code=200, tags=["Messages"],
    summary="Envio de mensagem em massa",
    description="Envia mensagens em massa para múltiplos destinatários.")
def send_bulk_messages(request: BulkMessageRequest):
    """
    Envia mensagens em massa para múltiplos destinatários.
    """
    logging.info(f"Iniciando envio de mensagens em massa para {len(request.recipients)} destinatários.")
    
    
    failed_recipients = []
    successful_recipients = []

    for recipient in request.recipients:
        try:
            response = send_message_template(recipient, request.message)
            logging.info(f"Mensagem enviada com sucesso para {recipient}")
            successful_recipients.append(recipient)
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao enviar mensagem para {recipient}: {str(e)}")
            failed_recipients.append({"recipient": recipient, "error": str(e)})

    return {
        "status": "completed",
        "total_recipients": len(request.recipients),
        "successful_recipients": successful_recipients,
        "failed_recipients": failed_recipients,
    }
