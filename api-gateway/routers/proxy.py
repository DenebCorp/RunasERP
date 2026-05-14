"""
Router de proxy para microsserviços.
"""
from typing import Annotated
from fastapi import APIRouter, Request, Depends
from auth.oauth2 import get_current_active_user, require_admin
from models.usuario import Usuario
from proxy.service_proxy import ServiceProxy


router = APIRouter()


# Rotas públicas (sem autenticação)
@router.api_route(
    "/catalogo/{path:path}",
    methods=["GET"],
    tags=["Catálogo Público"]
)
async def proxy_catalogo_publico(request: Request, path: str):
    """Proxy para catálogo público (sem autenticação)."""
    full_path = f"/catalogo/{path}" if path else "/catalogo"
    return await ServiceProxy.proxy_request(request, full_path)


@router.api_route(
    "/carrinho/{path:path}",
    methods=["GET", "POST", "PATCH", "DELETE"],
    tags=["Carrinho Público"]
)
async def proxy_carrinho_publico(request: Request, path: str):
    """Proxy para carrinho (sem autenticação)."""
    full_path = f"/carrinho/{path}" if path else "/carrinho"
    return await ServiceProxy.proxy_request(request, full_path)


# Rotas protegidas (requerem autenticação)
@router.api_route(
    "/clientes/{path:path}",
    methods=["GET", "POST", "PATCH", "DELETE"],
    tags=["Clientes"]
)
async def proxy_clientes(
    request: Request,
    path: str,
    current_user: Annotated[Usuario, Depends(get_current_active_user)]
):
    """Proxy para serviço de clientes (autenticado)."""
    full_path = f"/clientes/{path}" if path else "/clientes"
    return await ServiceProxy.proxy_request(request, full_path)


@router.api_route(
    "/produtos/{path:path}",
    methods=["GET", "POST", "PATCH", "DELETE"],
    tags=["Produtos"]
)
async def proxy_produtos(
    request: Request,
    path: str,
    current_user: Annotated[Usuario, Depends(get_current_active_user)]
):
    """Proxy para serviço de produtos (autenticado)."""
    full_path = f"/produtos/{path}" if path else "/produtos"
    return await ServiceProxy.proxy_request(request, full_path)


@router.api_route(
    "/estoque/{path:path}",
    methods=["GET", "POST", "PATCH", "DELETE"],
    tags=["Estoque"]
)
async def proxy_estoque(
    request: Request,
    path: str,
    current_user: Annotated[Usuario, Depends(require_admin)]
):
    """Proxy para serviço de estoque (apenas admin)."""
    full_path = f"/estoque/{path}" if path else "/estoque"
    return await ServiceProxy.proxy_request(request, full_path)


@router.api_route(
    "/pedidos/{path:path}",
    methods=["GET", "POST", "PATCH", "DELETE"],
    tags=["Pedidos"]
)
async def proxy_pedidos(
    request: Request,
    path: str,
    current_user: Annotated[Usuario, Depends(get_current_active_user)]
):
    """Proxy para serviço de vendas - pedidos (autenticado)."""
    full_path = f"/pedidos/{path}" if path else "/pedidos"
    return await ServiceProxy.proxy_request(request, full_path)


@router.api_route(
    "/pagamentos/{path:path}",
    methods=["GET", "POST", "PATCH"],
    tags=["Pagamentos"]
)
async def proxy_pagamentos(
    request: Request,
    path: str,
    current_user: Annotated[Usuario, Depends(get_current_active_user)]
):
    """Proxy para serviço de vendas - pagamentos (autenticado)."""
    full_path = f"/pagamentos/{path}" if path else "/pagamentos"
    return await ServiceProxy.proxy_request(request, full_path)


@router.api_route(
    "/contas/{path:path}",
    methods=["GET", "POST", "PATCH"],
    tags=["Financeiro"]
)
async def proxy_contas(
    request: Request,
    path: str,
    current_user: Annotated[Usuario, Depends(require_admin)]
):
    """Proxy para serviço financeiro (apenas admin)."""
    full_path = f"/contas/{path}" if path else "/contas"
    return await ServiceProxy.proxy_request(request, full_path)


@router.api_route(
    "/notificacoes/{path:path}",
    methods=["GET", "POST"],
    tags=["Notificações"]
)
async def proxy_notificacoes(
    request: Request,
    path: str,
    current_user: Annotated[Usuario, Depends(require_admin)]
):
    """Proxy para serviço de notificações (apenas admin)."""
    full_path = f"/notificacoes/{path}" if path else "/notificacoes"
    return await ServiceProxy.proxy_request(request, full_path)


# Webhook público (sem autenticação)
@router.post(
    "/pagamentos/webhook/mercadopago",
    tags=["Webhooks"]
)
async def proxy_webhook_mercadopago(request: Request):
    """Proxy para webhook do Mercado Pago (público)."""
    return await ServiceProxy.proxy_request(request, "/pagamentos/webhook/mercadopago")
