from fastapi import APIRouter, HTTPException
from app.models.TemplateMessageRequest import TemplateMessageRequest
from app.services.send_message_hello_word import send_message_hello_word
import logging

router = APIRouter()

@router.post("/send-hello-world", tags=["Messages"],
    summary="Envia Template Hello World",
    description="Faz envio ao destinatário de uma mensagem template padrão Heloo World",)
def send_hello_word(request: TemplateMessageRequest):
    """
    Endpoint para enviar o template Hello World sem variáveis.
    """
    try:
        response = send_message_hello_word(request.recipient)
        logging.info(
            f"Mensagem Hello World enviada com sucesso para {request.recipient}."
        )
        return {"status": "success", "response": response}
    except Exception as e:
        logging.error(f"Erro ao enviar mensagem Hello World: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Erro ao enviar mensagem Hello World"
        )