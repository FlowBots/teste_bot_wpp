"""
    Arquivo de importação de rotas
"""

# * Importando classes de seus respectivos módulos dentro do pacote atual. Fazemos, por padrão, o import relativo
# * (com ponto inicial) para que o Python saiba que estamos importando de um módulo dentro do mesmo pacote.

from .send_hello_word import router as send_hello_word_router
from .send_instant_message import router as send_instant_message_router
from .send_message_template import router as send_message_template_router
from .webhook import router as webhook_router
from .logs import router as logs_router
from .schedule_message import router as schedule_message_router
from .update_token import router as update_token_router
from .current_token import router as current_token_router
from .expiration_time import router as expiration_time_router

__all__ = [
    "send_hello_word_router",
    "send_instant_message_router",
    "send_message_template_router",
    "webhook_router",
    "logs_router",
    "schedule_message_router",
    "update_token_router",
    "current_token_router",
    "expiration_time_router",
]
