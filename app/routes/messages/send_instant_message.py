from fastapi import APIRouter, HTTPException
from app.models.InstantMessageRequest import InstantMessageRequest
from app.services.send_message_instant import send_message_instant
import logging

router = APIRouter()

# Endpoint para envio instantâneo de mensagens
@router.post("/send-message/instant", status_code=200, tags=["Messages"],
    summary="Envio de mensagem instantânea",
    description="Faz o envio de mensagem customizada no instante que faz o POST",)
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