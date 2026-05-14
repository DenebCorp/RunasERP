"""
Publisher de eventos para RabbitMQ.
"""
import json
from typing import Any
import aio_pika
from aio_pika import ExchangeType
import structlog
from config import settings


log = structlog.get_logger()


class EventPublisher:
    """Publisher de eventos de domínio."""
    
    def __init__(self):
        self.connection = None
        self.channel = None
        self.exchange = None
    
    async def connect(self):
        """Conecta ao RabbitMQ."""
        if self.connection is None or self.connection.is_closed:
            self.connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
            self.channel = await self.connection.channel()
            self.exchange = await self.channel.declare_exchange(
                "erp.events",
                ExchangeType.TOPIC,
                durable=True
            )
    
    async def publish(self, routing_key: str, payload: dict[str, Any]):
        """
        Publica um evento.
        
        Args:
            routing_key: Chave de roteamento (ex: "pedido.confirmado")
            payload: Dados do evento
        """
        await self.connect()
        
        message = aio_pika.Message(
            body=json.dumps(payload).encode(),
            content_type="application/json",
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )
        
        await self.exchange.publish(message, routing_key=routing_key)
        
        log.info("event.published", routing_key=routing_key, payload=payload)
    
    async def close(self):
        """Fecha a conexão."""
        if self.connection and not self.connection.is_closed:
            await self.connection.close()


# Singleton
_publisher = EventPublisher()


async def get_publisher() -> EventPublisher:
    """Obtém instância do publisher."""
    return _publisher
