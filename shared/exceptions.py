"""
Exceções customizadas compartilhadas entre os microsserviços.
"""
from typing import Any, Optional


class RunasBaseException(Exception):
    """Exceção base para todas as exceções customizadas do Runas."""
    
    def __init__(self, message: str, details: Optional[dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(RunasBaseException):
    """Erro de validação de dados de negócio."""
    pass


class NotFoundError(RunasBaseException):
    """Recurso não encontrado."""
    pass


class ConflictError(RunasBaseException):
    """Conflito de dados (duplicação, estado inválido, etc)."""
    pass


class UnauthorizedError(RunasBaseException):
    """Usuário não autenticado."""
    pass


class ForbiddenError(RunasBaseException):
    """Usuário sem permissão para a operação."""
    pass


class InsufficientStockError(ConflictError):
    """Estoque insuficiente para a operação."""
    pass


class ClientBlockedError(ConflictError):
    """Cliente bloqueado."""
    pass


class InsufficientCreditError(ConflictError):
    """Crédito insuficiente."""
    pass


class InvalidCPFError(ValidationError):
    """CPF inválido."""
    pass


class InvalidCNPJError(ValidationError):
    """CNPJ inválido."""
    pass


class InvalidPhoneError(ValidationError):
    """Telefone inválido."""
    pass


class ExpiredCartError(ValidationError):
    """Carrinho expirado."""
    pass


class InvalidOrderStatusError(ValidationError):
    """Status de pedido inválido para a operação."""
    pass
