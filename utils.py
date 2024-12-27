import logging
import requests
import os

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
WHATSAPP_API_URL = os.getenv("WHATSAPP_API_URL")

def send_message(job_id: str, recipient: str, message: str):
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
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao enviar mensagem para {recipient}: {str(e)}")
