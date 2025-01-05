from fastapi import APIRouter, HTTPException
from app.models.InstantMessageRequest import InstantMessageRequest
from app.services.send_message_instant import send_message_instant

# importando a função send_message_template para erro de janela de 24h
from .send_message_template import send_message_template

import logging

router = APIRouter()


# Endpoint para envio instantâneo de mensagens
@router.post("/send-message", status_code=200)
def send_instant_message(request: InstantMessageRequest):
    try:
        response = send_message_instant(request.recipient, request.message)
        logging.info(
            f"Mensagem enviada com sucesso para {request.recipient}. Resposta: {request.message}"
        )
        return {"status": "success", "response": response}
    except Exception as e:
        logging.error(f"Erro ao enviar mensagem instantânea: {str(e)}")
        # raise HTTPException(
        #     status_code=500, detail="Erro ao enviar mensagem instantânea"
        # )

        #! Detecta erro de janela de 24 horas e tenta envia um template
        if "24 hours have passed" in str(e):
            logging.warning(
                f"Mensagem fora da janela de 24 horas para {request.recipient}. Tentando enviar template."
            )
            try:
                # Envia um template de mensagem
                template_response = send_message_template(
                    recipient=request.recipient,
                    template_name="starter_agent",  # Nome do template aprovado
                    variables=["nath"],  # Variáveis para o template
                )
                logging.info(
                    f"Template enviado com sucesso para {request.recipient}. Resposta: {template_response}"
                )
                return {"status": "success", "response": template_response}
            except Exception as template_error:
                logging.error(
                    f"Erro ao enviar template para {request.recipient}: {str(template_error)}"
                )
                raise HTTPException(
                    status_code=500, detail="Erro ao enviar template de mensagem"
                )
        else:
            # Caso seja outro erro, levanta a exceção genérica
            raise HTTPException(
                status_code=500, detail="Erro ao enviar mensagem instantânea"
            )
