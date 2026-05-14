"""
Schema de paginação padrão para todos os microsserviços.
"""
from typing import Generic, TypeVar
from pydantic import BaseModel, Field
from math import ceil


T = TypeVar('T')


class PaginatedResponse(BaseModel, Generic[T]):
    """Resposta paginada padrão."""
    
    items: list[T] = Field(description="Lista de itens da página atual")
    total: int = Field(description="Total de itens disponíveis")
    page: int = Field(description="Página atual (1-indexed)")
    size: int = Field(description="Tamanho da página")
    pages: int = Field(description="Total de páginas")
    
    @classmethod
    def create(
        cls,
        items: list[T],
        total: int,
        page: int,
        size: int
    ) -> "PaginatedResponse[T]":
        """Factory method para criar resposta paginada."""
        pages = ceil(total / size) if size > 0 else 0
        return cls(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=pages
        )


class PaginationParams(BaseModel):
    """Parâmetros de paginação padrão."""
    
    page: int = Field(default=1, ge=1, description="Número da página (1-indexed)")
    size: int = Field(default=20, ge=1, le=100, description="Tamanho da página")
    
    @property
    def skip(self) -> int:
        """Calcula o offset para o banco de dados."""
        return (self.page - 1) * self.size
    
    @property
    def limit(self) -> int:
        """Retorna o limite para o banco de dados."""
        return self.size
