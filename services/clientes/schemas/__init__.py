"""Schemas Pydantic."""
from .cliente import (
    ClienteCreate,
    ClienteUpdate,
    ClienteResponse,
    ClienteComEnderecos,
    CreditoUpdate,
    CreditoDelta,
    EnderecoCreate,
    EnderecoUpdate,
    EnderecoResponse
)

__all__ = [
    "ClienteCreate",
    "ClienteUpdate",
    "ClienteResponse",
    "ClienteComEnderecos",
    "CreditoUpdate",
    "CreditoDelta",
    "EnderecoCreate",
    "EnderecoUpdate",
    "EnderecoResponse"
]