"""
Endpoints para gestion de fallos 
"""
from fastapi import APIRouter, HttpException
from typing import List 
from pydantic import BaseModel 

router = APIRouter()

# Modelo de Datos simple (pydantic)
class FalloSimple(BaseModel):
    id: int 
    titulo: str
    materia: str
    fecha: str
    
