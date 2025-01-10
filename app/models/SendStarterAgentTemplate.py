from pydantic import BaseModel, Field, validator
from datetime import datetime
from app.config import BRASILIA_TZ
import logging


# Modelo de requisição
class TemplateRequest(BaseModel):
    """
    Modelo de mensagem usado no template de mensagem starter_agent da meta
    """

    recipient: str  # Número do destinatário no formato E.164
