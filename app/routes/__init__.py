"""
    Arquivo de importação de rotas
"""

# * Importando classes de seus respectivos módulos dentro do pacote atual. Fazemos, por padrão, o import relativo
# * (com ponto inicial) para que o Python saiba que estamos importando de um módulo dentro do mesmo pacote.

from .check_user_status import router as check_user_status_router
from .list_templates import router as list_templates_router
from .manage_templates import router as manage_templates_router

__all__ = [
    "check_user_status_router",
    "list_templates_router",
    "manage_templates_router",
]