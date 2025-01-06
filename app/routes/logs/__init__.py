"""
    Arquivo de importação de rotas
"""

# * Importando classes de seus respectivos módulos dentro do pacote atual. Fazemos, por padrão, o import relativo
# * (com ponto inicial) para que o Python saiba que estamos importando de um módulo dentro do mesmo pacote.

from .logs import router as logs_router

__all__ = [
    "logs_router",
]