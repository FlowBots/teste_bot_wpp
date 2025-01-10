from fastapi import APIRouter, HTTPException
import requests
from app.config import ACCESS_TOKEN, WHATSAPP_API_URL_GLOBAL
import logging

router = APIRouter()

@router.get("/WABA", status_code=200, tags=["Meta"],
    summary="Sobre um número de telefone registrado na API",
    description="Obter informações detalhadas sobre um número de telefone registrado na API do WhatsApp Business (WABA). Essa rota retorna metadados e configurações associadas ao número de telefone específico (GET)",)
def list_templates():
    """
    Obter informações detalhadas sobre um número de telefone registrado na API do WhatsApp Business (WABA). Essa rota retorna metadados e configurações associadas ao número de telefone específico.
    """
    logging.info("Iniciando a rota para obter informações detalhadas sobre um número de telefone registrado na API.")
    
    url = f"{WHATSAPP_API_URL_GLOBAL}"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    
    payload = {}

    try:
        response = requests.get(url, headers=headers, data=payload)
        
        logging.info(f"Response: {response.json()}")
        return {"status": "success", "templates": response.json()}
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao listar templates: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao listar templates")