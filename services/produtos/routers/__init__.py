"""Routers FastAPI."""
from routers.produtos import (
    router_categorias,
    router_produtos,
    router_variantes,
    router_catalogo,
    router_fornecedores,
    router_fornecedor_produtos,
)

__all__ = [
    "router_categorias",
    "router_produtos",
    "router_variantes",
    "router_catalogo",
    "router_fornecedores",
    "router_fornecedor_produtos",
]