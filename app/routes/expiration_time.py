from fastapi import APIRouter, HTTPException
from app.services.get_expiration_time import get_expiration_time
import logging

router = APIRouter()

# Endpoint para pegar tempo de expiração do token
@router.get("/expiration-time")
def expiration_time():
    expiration_time = get_expiration_time()
    return {"expiration_time": expiration_time}