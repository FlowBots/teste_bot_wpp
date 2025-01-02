import requests
import logging
from app.config import WHATSAPP_API_URL, ACCESS_TOKEN

# Função Simulada de Envio de Mensagem
def send_message_template(recipient: str, message: str):
    logging.info(
        f"Iniciando envio de mensagem para o destinatário: {recipient}: {message}"
    )

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
        logging.info(
            f"Mensagem enviada com sucesso para {recipient}. Resposta: {response.json()}"
        )
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao enviar mensagem para {recipient}: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao enviar a mensagem")