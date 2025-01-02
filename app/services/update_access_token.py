import requests
import logging
from app.config import APP_ID, APP_SECRET, ACCESS_TOKEN

# Função para atualizar o token de acesso
def update_access_token():
    global ACCESS_TOKEN
    logging.info("Iniciando renovação do token de acesso.")
    try:
        url = "https://graph.facebook.com/v14.0/oauth/access_token"
        params = {
            "grant_type": "fb_exchange_token",
            "client_id": APP_ID,
            "client_secret": APP_SECRET,
            "fb_exchange_token": ACCESS_TOKEN,
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        ACCESS_TOKEN = data.get("access_token")
        logging.info("Token de acesso atualizado com sucesso.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao renovar o token de acesso: {str(e)}")