from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse
from app.config import VERIFY_TOKEN

router = APIRouter()

@router.get("/webhook")
async def validate_webhook(request: Request):
    params = request.query_params
    logging.info(f"Webhook recebido - Parâmetros: {params}")

    hub_mode = params.get("hub.mode")
    hub_verify_token = params.get("hub.verify_token")
    hub_challenge = params.get("hub.challenge")

    # Log para depuração
    logging.info(
        f"Recebido: hub_mode={hub_mode}, hub_verify_token={hub_verify_token}, hub_challenge={hub_challenge}"
    )

    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        logging.info("Webhook validado com sucesso.")
        return PlainTextResponse(hub_challenge)  # Retorna o desafio como texto puro
    else:
        logging.warning("Falha ao validar o webhook. Token de verificação inválido.")
        return {"error": "Token de verificação inválido"}