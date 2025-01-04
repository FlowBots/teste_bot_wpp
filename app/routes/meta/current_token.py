from fastapi import APIRouter, HTTPException
from app.config import ACCESS_TOKEN
import logging

router = APIRouter()

# Endpoint para verificação do token atual
@router.get("/current-token", tags=["Meta"],
    summary="Ver Token de acesso atual",
    description="Retorna Token de acesso atual no projeto",)
def get_current_token():
    return {"access_token": ACCESS_TOKEN}