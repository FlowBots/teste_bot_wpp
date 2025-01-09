from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse
from app.config import VERIFY_TOKEN
import logging
import requests

router = APIRouter()

# Endpoint para validação inicial do webhook (GET)
@router.get("/webhook", tags=["Meta"],
    summary="Validação inicial do webhook",
    description="Endpoint para validação inicial do webhook (GET)",)
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

# Endpoint para receber notificações (POST)
@router.post("/webhook", tags=["Meta"],
    summary="Receber notificações - webhook",
    description="Endpoint para receber notificações (POST)",)
async def receive_webhook(request: Request):
    try:
        payload = await request.json()
        logging.info(f"Payload recebido no webhook: {payload}")

        # Aqui você pode processar os eventos recebidos
        # Exemplo: Verificar se a mensagem é de um novo cliente, se foi entregue, etc.

        return {"status": "Webhook processado com sucesso"}
    except Exception as e:
        logging.error(f"Erro ao processar o webhook: {str(e)}")
        return {"error": "Erro ao processar o webhook"}