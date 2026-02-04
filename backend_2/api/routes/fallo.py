"""
Endpoints para la gestion de fallos
Esta API maneja las operaciones de CRUD para los fallos judiciales
"""

from fastapi import APIRouter
from typing import List 
from pydantic import BaseModel 

router = APIRouter()

# Modelo de Datos simple 
class FalloSimple(BaseModel):
    id: int 
    titulo: str
    materia: str 
    fecha: str
    
    class Config:
        
