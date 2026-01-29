"""
Endpoints para gestión de etiquetas
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from core.database import get_db
from core.models import Etiqueta
from core.schemas import EtiquetaResponse

router = APIRouter()


@router.get("/", response_model=List[EtiquetaResponse])
async def listar_etiquetas(
    categoria: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Listar todas las etiquetas disponibles"""
    query = db.query(Etiqueta)
    
    if categoria:
        query = query.filter(Etiqueta.categoria == categoria)
    
    etiquetas = query.all()
    return etiquetas


@router.get("/categorias")
async def listar_categorias(db: Session = Depends(get_db)):
    """Listar todas las categorías de etiquetas"""
    categorias = db.query(Etiqueta.categoria).distinct().all()
    return {"categorias": [cat[0] for cat in categorias if cat[0]]
