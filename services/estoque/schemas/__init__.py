"""Schemas do serviço de estoque."""
from .estoque import (
    # Estoque
    EstoqueCreate,
    EstoqueUpdate,
    EstoqueResponse,
    EstoqueComAlerta,
    
    # Movimentação
    MovimentacaoCreate,
    MovimentacaoResponse,
    
    # Lote
    LoteCreate,
    LoteUpdate,
    LoteResponse,
    LoteComAlerta,
    
    # Inventário
    InventarioCreate,
    InventarioUpdate,
    InventarioResponse,
    ItemInventarioCreate,
    ItemInventarioResponse,
    
    # Operações
    EntradaEstoqueRequest,
    SaidaEstoqueRequest,
    AjusteEstoqueRequest,
    ReservaEstoqueRequest,
    LiberarReservaRequest,
    
    # Relatórios
    RelatorioEstoque,
    RelatorioMovimentacoes,
)

__all__ = [
    "EstoqueCreate",
    "EstoqueUpdate",
    "EstoqueResponse",
    "EstoqueComAlerta",
    "MovimentacaoCreate",
    "MovimentacaoResponse",
    "LoteCreate",
    "LoteUpdate",
    "LoteResponse",
    "LoteComAlerta",
    "InventarioCreate",
    "InventarioUpdate",
    "InventarioResponse",
    "ItemInventarioCreate",
    "ItemInventarioResponse",
    "EntradaEstoqueRequest",
    "SaidaEstoqueRequest",
    "AjusteEstoqueRequest",
    "ReservaEstoqueRequest",
    "LiberarReservaRequest",
    "RelatorioEstoque",
    "RelatorioMovimentacoes",
]
