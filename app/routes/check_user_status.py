from fastapi import APIRouter, HTTPException
import requests
from app.config import WHATSAPP_API_URL, ACCESS_TOKEN
import logging

router = APIRouter()
# NÃO CONSEGUI VERIFICAR O FUNCIONAMENTO DESSE ENDPOINT
@router.get("/users/{phone_number}/status", status_code=200)
def check_user_status(phone_number: str):
    """
    Verifica o status de um número no WhatsApp.
    """
    logging.info(f"Verificando status do número: {phone_number}")
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    url = f"{WHATSAPP_API_URL}/{phone_number}/exists"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        logging.info(f"Status do número {phone_number}: {data}")
        return {
            "status": "success",
            "number": phone_number,
            "whatsapp_registered": data.get("whatsapp_registered"),
        }
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao verificar status do número {phone_number}: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Erro ao verificar status do número"
        )
