"""
Endpoints para gestión de embeddings
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db

router = APIRouter()


@router.post("/generar/{fallo_id}")
async def generar_embedding(
    fallo_id: int,
    db: Session = Depends(get_db)
):
    """
    Generar embedding para un fallo específico
    (Normalmente se hace automáticamente durante el procesamiento)
    """
    from core.services.embedding_service import EmbeddingService
    
    embedding_service = EmbeddingService(db)
    resultado = await embedding_service.generar_embedding_fallo(fallo_id)
    
    return {"mensaje": "Embedding generado exitosamente", "fallo_id": fallo_id}
