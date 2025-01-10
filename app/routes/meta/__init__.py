"""
    Arquivo de importação de rotas
"""

# * Importando classes de seus respectivos módulos dentro do pacote atual. Fazemos, por padrão, o import relativo
# * (com ponto inicial) para que o Python saiba que estamos importando de um módulo dentro do mesmo pacote.

from .current_token import router as current_token_router
from .expiration_time import router as expiration_time_router
from .update_token import router as update_token_router
from .webhook import router as webhook_router
from .WABA import router as WABA_router

__all__ = [
    "current_token_router",
    "expiration_time_router",
    "update_token_router",
    "webhook_router",
    "WABA_router",
]