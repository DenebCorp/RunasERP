"""
Routers do serviço de Clientes.
"""
from .clientes import router as clientes_router
from .enderecos import router as enderecos_router

__all__ = ["clientes_router", "enderecos_router"]
