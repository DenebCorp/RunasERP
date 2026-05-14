"""
Routers de Estoque.
"""
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from schemas.estoque import (
    EstoqueCreate,
    EstoqueUpdate,
    EstoqueResponse,
    EstoqueComAlerta,
    MovimentacaoResponse,
    LoteResponse,
    LoteComAlerta,
    EntradaEstoqueRequest,
    SaidaEstoqueRequest,
    AjusteEstoqueRequest,
    ReservaEstoqueRequest,
    LiberarReservaRequest,
    RelatorioEstoque,
    RelatorioMovimentacoes,
)
from services.estoque_service import EstoqueService
from repositories.estoque_repository import (
    EstoqueRepository,
    MovimentacaoRepository,
    LoteRepository
)
from models.estoque import TipoMovimentacao

router = APIRouter(prefix="/estoque", tags=["Estoque"])


# ==================== ESTOQUE ====================

@router.post("", response_model=EstoqueResponse, status_code=status.HTTP_201_CREATED)
async def criar_estoque(
    data: EstoqueCreate,
    db: AsyncSession = Depends(get_db)
):
    """Cria um novo registro de estoque."""
    try:
        return await EstoqueService.criar_estoque(db, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", response_model=List[EstoqueComAlerta])
async def listar_estoques(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    apenas_baixo: bool = Query(False, description="Apenas estoques abaixo do mínimo"),
    apenas_zerado: bool = Query(False, description="Apenas estoques zerados"),
    db: AsyncSession = Depends(get_db)
):
    """Lista estoques com alertas."""
    return await EstoqueService.listar_estoques(
        db, skip=skip, limit=limit,
        apenas_baixo=apenas_baixo,
        apenas_zerado=apenas_zerado
    )


@router.get("/baixo", response_model=List[EstoqueComAlerta])
async def listar_estoque_baixo(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
):
    """Lista produtos com estoque abaixo do mínimo."""
    return await EstoqueService.listar_estoques(db, skip=skip, limit=limit, apenas_baixo=True)


@router.get("/zerado", response_model=List[EstoqueComAlerta])
async def listar_estoque_zerado(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
):
    """Lista produtos sem estoque."""
    return await EstoqueService.listar_estoques(db, skip=skip, limit=limit, apenas_zerado=True)


@router.get("/{estoque_id}", response_model=EstoqueComAlerta)
async def buscar_estoque(
    estoque_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Busca estoque por ID."""
    estoque = await EstoqueService.buscar_estoque(db, estoque_id)
    if not estoque:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estoque não encontrado")
    return estoque


@router.put("/{estoque_id}", response_model=EstoqueResponse)
async def atualizar_estoque(
    estoque_id: int,
    data: EstoqueUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Atualiza configurações de estoque."""
    estoque = await EstoqueService.atualizar_estoque(db, estoque_id, data)
    if not estoque:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estoque não encontrado")
    return estoque


# ==================== MOVIMENTAÇÕES ====================

@router.post("/entrada", response_model=EstoqueResponse, status_code=status.HTTP_201_CREATED)
async def entrada_estoque(
    data: EntradaEstoqueRequest,
    db: AsyncSession = Depends(get_db)
):
    """Registra entrada de estoque."""
    try:
        estoque, lote_id = await EstoqueService.entrada_estoque(db, data)
        return estoque
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/saida", response_model=EstoqueResponse)
async def saida_estoque(
    data: SaidaEstoqueRequest,
    db: AsyncSession = Depends(get_db)
):
    """Registra saída de estoque."""
    try:
        return await EstoqueService.saida_estoque(db, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/ajuste", response_model=EstoqueResponse)
async def ajustar_estoque(
    data: AjusteEstoqueRequest,
    db: AsyncSession = Depends(get_db)
):
    """Ajusta estoque (inventário)."""
    try:
        return await EstoqueService.ajustar_estoque(db, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/reservar", response_model=EstoqueResponse)
async def reservar_estoque(
    data: ReservaEstoqueRequest,
    db: AsyncSession = Depends(get_db)
):
    """Reserva estoque para venda."""
    try:
        return await EstoqueService.reservar_estoque(db, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/liberar-reserva", response_model=EstoqueResponse)
async def liberar_reserva(
    data: LiberarReservaRequest,
    db: AsyncSession = Depends(get_db)
):
    """Libera reserva de estoque."""
    try:
        return await EstoqueService.liberar_reserva(db, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{estoque_id}/movimentacoes", response_model=List[MovimentacaoResponse])
async def listar_movimentacoes(
    estoque_id: int,
    tipo: Optional[TipoMovimentacao] = Query(None, description="Filtrar por tipo"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
):
    """Lista movimentações de um estoque."""
    movimentacoes = await MovimentacaoRepository.listar(
        db, estoque_id=estoque_id, tipo=tipo, skip=skip, limit=limit
    )
    return [MovimentacaoResponse.model_validate(m) for m in movimentacoes]


# ==================== LOTES ====================

@router.get("/{estoque_id}/lotes", response_model=List[LoteComAlerta])
async def listar_lotes(
    estoque_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
):
    """Lista lotes de um estoque."""
    lotes = await LoteRepository.listar(db, estoque_id=estoque_id, skip=skip, limit=limit)
    
    result = []
    for lote in lotes:
        response = LoteComAlerta.model_validate(lote)
        
        # Calcular alertas
        if lote.data_validade:
            hoje = datetime.now().date()
            dias_para_vencer = (lote.data_validade - hoje).days
            response.dias_para_vencer = dias_para_vencer
            response.alerta_vencimento = 0 < dias_para_vencer <= 30
            response.vencido = dias_para_vencer < 0
        else:
            response.dias_para_vencer = None
            response.alerta_vencimento = False
            response.vencido = False
        
        result.append(response)
    
    return result


@router.get("/lotes/vencendo", response_model=List[LoteComAlerta])
async def listar_lotes_vencendo(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
):
    """Lista lotes próximos do vencimento (30 dias)."""
    lotes = await LoteRepository.listar(db, vencendo=True, skip=skip, limit=limit)
    
    result = []
    for lote in lotes:
        response = LoteComAlerta.model_validate(lote)
        
        if lote.data_validade:
            hoje = datetime.now().date()
            dias_para_vencer = (lote.data_validade - hoje).days
            response.dias_para_vencer = dias_para_vencer
            response.alerta_vencimento = True
            response.vencido = False
        
        result.append(response)
    
    return result


# ==================== RELATÓRIOS ====================

@router.get("/relatorios/geral", response_model=RelatorioEstoque)
async def relatorio_geral(db: AsyncSession = Depends(get_db)):
    """Gera relatório geral de estoque."""
    return await EstoqueService.gerar_relatorio(db)


@router.get("/relatorios/movimentacoes", response_model=RelatorioMovimentacoes)
async def relatorio_movimentacoes(
    data_inicio: datetime = Query(..., description="Data inicial"),
    data_fim: datetime = Query(..., description="Data final"),
    db: AsyncSession = Depends(get_db)
):
    """Gera relatório de movimentações por período."""
    return await EstoqueService.gerar_relatorio_movimentacoes(db, data_inicio, data_fim)
