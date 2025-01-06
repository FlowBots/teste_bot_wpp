"""
    Arquivo de importação de rotas
"""

# * Importando classes de seus respectivos módulos dentro do pacote atual. Fazemos, por padrão, o import relativo
# * (com ponto inicial) para que o Python saiba que estamos importando de um módulo dentro do mesmo pacote.

from .cancel_scheduled_message import router as cancel_scheduled_message_router
from .list_scheduled_messages import router as list_scheduled_messages_router
from .schedule_message import router as schedule_message_router
from .schedule_recurring import router as schedule_recurring_router
from .send_bulk_messages import router as send_bulk_messages_router
from .send_instant_message import router as send_instant_message_router
from .send_template_message import router as send_template_message_router

__all__ = [
    "cancel_scheduled_message_router",
    "list_scheduled_messages_router",
    "schedule_message_router",
    "schedule_recurring_router",
    "send_bulk_messages_router",
    "send_instant_message_router",
    "send_template_message_router",
]