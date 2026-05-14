"""
Middleware de logging estruturado.
"""
import time
import structlog
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


log = structlog.get_logger()


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware para log estruturado de todas as requisições."""
    
    async def dispatch(self, request: Request, call_next):
        """Processa a requisição e loga."""
        start_time = time.time()
        
        # Log da requisição
        log.info(
            "request.started",
            method=request.method,
            path=request.url.path,
            client_ip=request.client.host if request.client else None
        )
        
        # Processar requisição
        response = await call_next(request)
        
        # Log da resposta
        duration = time.time() - start_time
        log.info(
            "request.completed",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=round(duration * 1000, 2)
        )
        
        return response
