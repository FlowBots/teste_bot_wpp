# NÃO CONSEGUI VERIFICAR O FUNCIONAMENTO DESSE ENDPOINT

from fastapi import APIRouter, HTTPException
import requests
from app.config import WHATSAPP_API_URL, ACCESS_TOKEN
import logging

router = APIRouter()

@router.get("/templates", status_code=200)
def list_templates():
    """
    Lista os templates disponíveis na conta de WhatsApp Business.
    """
    logging.info("Solicitando lista de templates disponíveis.")
    
    url = f"{WHATSAPP_API_URL}/v14.0/{ACCESS_TOKEN}/message_templates"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        templates = response.json().get("data", [])
        
        logging.info(f"{len(templates)} templates encontrados.")
        return {"status": "success", "templates": templates}
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao listar templates: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao listar templates")

