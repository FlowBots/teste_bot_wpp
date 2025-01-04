from fastapi import APIRouter, HTTPException
from app.services.get_expiration_time import get_expiration_time
import logging

router = APIRouter()

# Endpoint para pegar tempo de expiração do token
@router.get("/expiration-time", tags=["Meta"],
    summary="Tempo de expiração de Token",
    description="Retorna o tempo de expiaração do Token de acesso",)
def expiration_time():
    expiration_time = get_expiration_time()
    return {"expiration_time": expiration_time}