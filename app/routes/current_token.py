from fastapi import APIRouter, HTTPException
from app.config import ACCESS_TOKEN
import logging

router = APIRouter()

# Endpoint para verificação do token atual
@router.get("/current-token")
def get_current_token():
    return {"access_token": ACCESS_TOKEN}