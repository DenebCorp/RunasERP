"""
Schemas Pydantic para usuário.
"""
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, field_validator
from models.usuario import RoleEnum


class UsuarioBase(BaseModel):
    """Schema base de usuário."""
    nome: str = Field(..., min_length=3, max_length=255)
    email: EmailStr


class UsuarioCreate(UsuarioBase):
    """Schema para criação de usuário."""
    senha: str = Field(..., min_length=8, max_length=100)
    role: RoleEnum = RoleEnum.OPERADOR
    
    @field_validator('senha')
    @classmethod
    def validate_senha(cls, v: str) -> str:
        """Valida força da senha."""
        if not any(c.isupper() for c in v):
            raise ValueError('Senha deve conter ao menos uma letra maiúscula')
        if not any(c.islower() for c in v):
            raise ValueError('Senha deve conter ao menos uma letra minúscula')
        if not any(c.isdigit() for c in v):
            raise ValueError('Senha deve conter ao menos um número')
        return v


class UsuarioUpdate(BaseModel):
    """Schema para atualização de usuário."""
    nome: str | None = Field(None, min_length=3, max_length=255)
    email: EmailStr | None = None
    role: RoleEnum | None = None
    ativo: bool | None = None


class UsuarioResponse(UsuarioBase):
    """Schema de resposta de usuário."""
    id: UUID
    role: RoleEnum
    ativo: bool
    criado_em: datetime
    
    model_config = {"from_attributes": True}


class Token(BaseModel):
    """Schema de token JWT."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Payload do token JWT."""
    sub: str  # user_id
    role: RoleEnum
    exp: int
    iat: int


class RefreshTokenRequest(BaseModel):
    """Request para refresh token."""
    refresh_token: str
