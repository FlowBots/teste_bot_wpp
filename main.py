from fastapi import FastAPI, Request
import requests
from fastapi.responses import (
    PlainTextResponse,
)  # Certifique-se de adicionar esta importação
from dotenv import load_dotenv
import os

# Carrega as variáveis do arquivo .env
load_dotenv()

app = FastAPI()

# Substitua pelo seu token de acesso
ACCESS_TOKEN = os.getenv("TOKEN_META")  # Token de acesso do Meta Developers
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

# Verificação para garantir que as variáveis estão configuradas
if not all([ACCESS_TOKEN, PHONE_NUMBER_ID, VERIFY_TOKEN]):
    raise ValueError("Variáveis de ambiente não configuradas corretamente.")


def send_message(to, message):
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {"messaging_product": "whatsapp", "to": to, "text": {"body": message}}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        print(f"Erro ao enviar mensagem: {response.text}")


@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()

    # Verifica se há mensagens
    if data and "messages" in data.get("entry", [{}])[0].get("changes", [{}])[0].get(
        "value", {}
    ):
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        phone_number = message["from"]  # Número do remetente
        text = message["text"]["body"]  # Texto da mensagem recebida

        # Responde à mensagem
        send_message(phone_number, f"Você enviou: {text}")

    return {"status": "success"}


@app.post("/webhooksend-message")
async def send_message_route(to: str, message: str):
    try:
        send_message(to, message)
        return {"status": "success", "message": f"Mensagem enviada para {to}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# Rota para validar o webhook no Meta (necessário ao configurar o webhook)
@app.get("/webhook")
async def validate_webhook(request: Request):
    params = request.query_params
    hub_mode = params.get("hub.mode")
    hub_verify_token = params.get("hub.verify_token")
    hub_challenge = params.get("hub.challenge")

    print(
        f"Recebido: hub_mode={hub_mode}, hub_verify_token={hub_verify_token}, hub_challenge={hub_challenge}"
    )

    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return PlainTextResponse(hub_challenge)  # Retorna o desafio como texto puro
    return {"error": "Token de verificação inválido"}
