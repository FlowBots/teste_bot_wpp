from pydantic import BaseModel, Field, validator
from datetime import datetime, timezone
import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from dotenv import load_dotenv

class ScheduleMessageRequest(BaseModel):
    recipient: str = Field(..., description="Número do destinatário no formato E.164", example="+5511999999999")
    message: str = Field(..., description="Mensagem a ser enviada")
    send_time: datetime = Field(..., description="Data e hora do envio no formato ISO 8601", example="2024-12-25T15:30:00")
    
    @validator("recipient")
    def validate_recipient(cls, value):
        logging.info(f"Validando destinatário: {value}")
        if not value.startswith("+") or not value[1:].isdigit():
            logging.error("Número de destinatário inválido.")
            raise ValueError("Número do destinatário deve estar no formato E.164 (ex: +5511999999999)")
        return value
    
    @validator("send_time")
    def validate_send_time(cls, value):
        now = datetime.now(timezone.utc)
        logging.info(f"Horário atual (UTC): {now}")
        logging.info(f"Horário fornecido (UTC): {value}")
        
        # Certifique-se de que o valor seja "offset-aware" (com fuso horário)
        if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
            value = value.replace(tzinfo=timezone.utc)
        
        if value <= now:
            raise ValueError("O horário de envio deve ser no futuro")
        return value
