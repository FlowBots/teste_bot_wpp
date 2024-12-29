from fastapi import APIRouter, HTTPException
from app.models import InstantMessageRequest, ScheduleMessageRequest
from app.services import send_message_instant
import logging

router = APIRouter()

@router.post("/send-message")
def send_instant_message(request: InstantMessageRequest):
    try:
        response = send_message_instant(request.recipient, request.message)
        logging.info(
            f"Mensagem enviada com sucesso para {request.recipient}. Resposta: {request.message}"
        )
        return {"status": "success", "response": response}
    except Exception as e:
        logging.error(f"Erro ao enviar mensagem instantânea: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Erro ao enviar mensagem instantânea"
        )