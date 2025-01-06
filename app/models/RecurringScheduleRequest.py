from pydantic import BaseModel, Field, validator
from datetime import datetime
from app.config import BRASILIA_TZ
import logging

class RecurringScheduleRequest(BaseModel):
    recipient: str = Field(
        ...,
        description="Número do destinatário no formato E.164",
        example="+5555997013555"
    )
    message: str = Field(
        ...,
        description="Mensagem a ser enviada",
        example="Essa é uma mensagem recorrente!"
    )
    frequency: str = Field(
        ...,
        description="Frequência de envio: daily, weekly, monthly",
        example="daily"
    )
    start_time: datetime = Field(
        ...,
        description="Data e hora de início no formato ISO 8601",
        example="2025-01-02T15:30:00"
    )
    end_time: datetime = Field(
        None,
        description="Data e hora de término no formato ISO 8601 (opcional)",
        example="2025-01-10T15:30:00"
    )

    @validator("recipient")
    def validate_recipient(cls, value):
        if not value.startswith("+") or not value[1:].isdigit():
            raise ValueError("O número deve estar no formato E.164 (ex: +5511999999999)")
        return value

    @validator("frequency")
    def validate_frequency(cls, value):
        if value not in ["daily", "weekly", "monthly"]:
            raise ValueError("A frequência deve ser daily, weekly ou monthly")
        return value