from pydantic import BaseModel, Field, validator
from typing import List
import logging

# Modelo de dados para validação do payload
class BulkMessageRequest(BaseModel):
    recipients: List[str] = Field(
        ...,
        description="Lista de números de telefone no formato E.164",
        example=["+5555997013555", "+5555997013555", "+5555996884436", "+5555997013555"]
    )
    message: str = Field(
        ...,
        description="Mensagem a ser enviada para os destinatários",
        example="Olá, estamos entrando em contato para informar sobre nossas promoções!"
    )

    @validator("recipients", each_item=True)
    def validate_recipients(cls, value):
        logging.info(f"Validando destinatários: {value}")
        if not value.startswith("+") or not value[1:].isdigit():
            logging.error("Número de destinatário(s) inválido(s).")
            raise ValueError(
                "Cada número deve estar no formato E.164 (exemplo: +5511999999999)"
            )
        return value