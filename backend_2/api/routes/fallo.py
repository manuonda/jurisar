"""
Endpoint para analizar fallos judiciales
"""

from fastapi import APIRouter
from core.services.ia_service import IAService
from typing import Optional, List

router = APIRouter()
ia_service = IAService()

# Modelo de Datos simple 
class FalloSimple(BaseModel):
    id: int 
    titulo: str
    materia: str 
    fecha: str
    
    class Config:
        
