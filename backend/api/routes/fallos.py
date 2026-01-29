"""
Endpoints para gestión de fallos
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from core.database import get_db
from core.models import Fallo
from core.schemas import FalloResponse, FalloCreate

router = APIRouter()


@router.get("/", response_model=List[FalloResponse])
async def listar_fallos(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    materia: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Listar fallos con paginación"""
    query = db.query(Fallo)
    
    if materia:
        query = query.filter(Fallo.materia == materia)
    
    fallos = query.offset(skip).limit(limit).all()
    return fallos


@router.get("/{fallo_id}", response_model=FalloResponse)
async def obtener_fallo(
    fallo_id: int,
    db: Session = Depends(get_db)
):
    """Obtener un fallo por ID"""
    fallo = db.query(Fallo).filter(Fallo.id == fallo_id).first()
    if not fallo:
        raise HTTPException(status_code=404, detail="Fallo no encontrado")
    return fallo


@router.post("/", response_model=FalloResponse)
async def crear_fallo(
    fallo_data: FalloCreate,
    db: Session = Depends(get_db)
):
    """Crear un nuevo fallo (usado por el scraper)"""
    fallo = Fallo(**fallo_data.dict())
    db.add(fallo)
    db.commit()
    db.refresh(fallo)
    return fallo
