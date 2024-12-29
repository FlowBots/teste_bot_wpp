from pydantic import BaseModel, Field, validator
from datetime import datetime
from app.config import BRASILIA_TZ
import logging

# Modelo de Dados para a Requisição
class ScheduleMessageRequest(BaseModel):
    recipient: str = Field(
        ...,
        description="Número do destinatário no formato E.164",
        example="+5555997013555",
    )
    message: str = Field(..., description="Mensagem a ser enviada")
    send_time: datetime = Field(
        ...,
        description="Data e hora do envio no formato ISO 8601",
        example="2024-12-27T15:30:00",
    )

    @validator("recipient")
    def validate_recipient(cls, value):
        logging.info(f"Validando destinatário: {value}")
        if not value.startswith("+") or not value[1:].isdigit():
            logging.error("Número de destinatário inválido.")
            raise ValueError(
                "Número do destinatário deve estar no formato E.164 (ex: +5511999999999)"
            )
        return value

    @validator("send_time")
    def validate_send_time(cls, value):
        # Obter o horário atual no fuso horário de Brasília
        now_brasilia = datetime.now(BRASILIA_TZ)
        logging.info(f"Horário atual (Brasília): {now_brasilia}")

        # Certificar que o horário fornecido é "offset-aware" (com fuso horário)
        if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
            value = BRASILIA_TZ.localize(value)

        logging.info(f"Horário fornecido 'offset-aware': {value}")

        # Comparar o horário ajustado com o horário atual de Brasília
        if value <= now_brasilia:
            logging.error("O horário de envio está no passado.")
            raise ValueError("O horário de envio deve ser no futuro")

        return value  # Retorna o horário original


# Modelo de Dados para a Requisição de Mensagem Instantânea
class InstantMessageRequest(BaseModel):
    recipient: str = Field(
        ...,
        description="Número do destinatário no formato E.164",
        example="+5555997013555",
    )
    message: str = Field(..., description="Mensagem a ser enviada")

    @validator("recipient")
    def validate_recipient(cls, value):
        logging.info(f"Validando destinatário: {value}")
        if not value.startswith("+") or not value[1:].isdigit():
            logging.error("Número de destinatário inválido.")
            raise ValueError(
                "Número do destinatário deve estar no formato E.164 (ex: +5511999999999)"
            )
        return value