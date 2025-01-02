import requests
import logging
from app.config import WHATSAPP_API_URL, ACCESS_TOKEN

# Função Simulada de Envio de Mensagem Agendada
def send_message_scheduled(job_id: str, recipient: str, message: str):
    logging.info(
        f"Iniciando envio de mensagem - Job ID: {job_id}, Destinatário: {recipient}: {message}"
    )

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
        "text": {"body": message},
    }

    try:
        response = requests.post(WHATSAPP_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        logging.info(
            f"Mensagem enviada com sucesso para {recipient}. Resposta: {response.json()}"
        )
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao enviar mensagem para {recipient}: {str(e)}")
        logging.debug(f"Payload enviado: {payload}")
        raise HTTPException(status_code=500, detail="Erro ao enviar a mensagem")