# NÃO CONSEGUI VERIFICAR O FUNCIONAMENTO DESSE ENDPOINT

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import requests
from app.config import WHATSAPP_API_URL, ACCESS_TOKEN
import logging

router = APIRouter()

class TemplateRequest(BaseModel):
    name: str = Field(..., description="Nome do template", example="order_update")
    language: str = Field(..., description="Código do idioma", example="pt_BR")
    category: str = Field(..., description="Categoria do template", example="TRANSACTIONAL")
    components: list = Field(
        ...,
        description="Componentes do template (e.g., corpo, cabeçalho)",
        example=[
            {
                "type": "BODY",
                "text": "Olá, seu pedido {{1}} foi atualizado para o status {{2}}."
            }
        ],
    )

@router.post("/templates", status_code=201)
def create_or_update_template(request: TemplateRequest):
    """
    Cria ou atualiza templates na conta de WhatsApp Business.
    """
    logging.info(f"Iniciando criação/atualização do template: {request.name}")
    
    url = f"{WHATSAPP_API_URL}/v14.0/{ACCESS_TOKEN}/message_templates"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "name": request.name,
        "language": request.language,
        "category": request.category,
        "components": request.components,
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        logging.info(f"Template {request.name} criado/atualizado com sucesso.")
        return {"status": "success", "data": data}
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao criar/atualizar template {request.name}: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao criar/atualizar template")
