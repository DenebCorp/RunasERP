"""
Cliente Redis para gerenciamento de tokens.
"""
from redis.asyncio import Redis, from_url
from config import settings


_redis_client: Redis | None = None


async def get_redis() -> Redis:
    """
    Obtém cliente Redis (singleton).
    
    Returns:
        Cliente Redis
    """
    global _redis_client
    
    if _redis_client is None:
        _redis_client = from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True
        )
    
    return _redis_client


async def close_redis():
    """Fecha conexão com Redis."""
    global _redis_client
    
    if _redis_client is not None:
        await _redis_client.close()
        _redis_client = None
