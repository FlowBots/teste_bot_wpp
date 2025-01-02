from fastapi import APIRouter, HTTPException
from app.services.update_access_token import update_access_token
from app.config import ACCESS_TOKEN
import logging

router = APIRouter()

# Endpoint para renovar o token de acesso
@router.get("/update-token")
def update_token():
    global ACCESS_TOKEN
    update_access_token()
    return {"access_token": ACCESS_TOKEN}