from pydantic import BaseModel, Field, validator
import logging

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