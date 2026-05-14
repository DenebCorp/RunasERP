"""
Classes base para eventos de domínio compartilhados entre microsserviços.
"""
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class DomainEvent(BaseModel):
    """Evento de domínio base."""
    
    event_id: UUID = Field(default_factory=uuid4)
    event_type: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    payload: dict[str, Any]
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }


class PedidoConfirmadoEvent(DomainEvent):
    """Evento: pedido confirmado."""
    event_type: str = "pedido.confirmado"


class PedidoCanceladoEvent(DomainEvent):
    """Evento: pedido cancelado."""
    event_type: str = "pedido.cancelado"


class EstoqueMinimoEvent(DomainEvent):
    """Evento: estoque atingiu quantidade mínima."""
    event_type: str = "estoque.minimo"


class CobrancaLembreteEvent(DomainEvent):
    """Evento: lembrete de cobrança (3 dias antes)."""
    event_type: str = "cobranca.lembrete"


class CobrancaVencidaEvent(DomainEvent):
    """Evento: cobrança vencida."""
    event_type: str = "cobranca.vencida"


class ContaQuitadaEvent(DomainEvent):
    """Evento: conta quitada."""
    event_type: str = "conta.quitada"
