"""
Endpoints de búsqueda semántica e híbrida
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from core.database import get_db
from core.services.search_service import SearchService

router = APIRouter()


@router.get("/semantica")
async def buscar_semantica(
    query: str = Query(..., description="Consulta en lenguaje natural"),
    limit: int = Query(10, ge=1, le=100),
    materia: Optional[str] = None,
    tipo_proceso: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Búsqueda semántica de fallos usando embeddings
    """
    search_service = SearchService(db)
    resultados = await search_service.buscar_semantica(
        query=query,
        limit=limit,
        materia=materia,
        tipo_proceso=tipo_proceso
    )
    return {"resultados": resultados, "total": len(resultados)}


@router.get("/hibrida")
async def buscar_hibrida(
    query: str = Query(..., description="Consulta en lenguaje natural"),
    limit: int = Query(10, ge=1, le=100),
    etiquetas: Optional[List[str]] = Query(None),
    materia: Optional[str] = None,
    fecha_desde: Optional[str] = None,
    fecha_hasta: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Búsqueda híbrida: combina filtros SQL con búsqueda semántica
    """
    search_service = SearchService(db)
    resultados = await search_service.buscar_hibrida(
        query=query,
        limit=limit,
        etiquetas=etiquetas,
        materia=materia,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta
    )
    return {"resultados": resultados, "total": len(resultados)}
