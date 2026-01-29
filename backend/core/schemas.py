"""
Schemas Pydantic para validación de datos
"""
from pydantic import BaseModel
from datetime import date
from typing import Optional, List


class FalloBase(BaseModel):
    """Schema base para fallos"""
    caratula: str
    fecha_fallo: Optional[date] = None
    tribunal: Optional[str] = None
    expediente: Optional[str] = None
    materia: Optional[str] = None
    tipo_proceso: Optional[str] = None
    juez: Optional[str] = None
    texto_completo: Optional[str] = None
    resumen_ia: Optional[str] = None
    resultado: Optional[str] = None
    url_original: Optional[str] = None


class FalloCreate(FalloBase):
    """Schema para crear un fallo"""
    pass


class EtiquetaResponse(BaseModel):
    """Schema de respuesta para etiquetas"""
    id: int
    nombre: str
    categoria: Optional[str] = None
    descripcion: Optional[str] = None
    es_generada: str = 'N'
    
    class Config:
        from_attributes = True


class FalloResponse(FalloBase):
    """Schema de respuesta para fallos"""
    id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    class Config:
        from_attributes = True


class FalloDetalleResponse(FalloResponse):
    """Schema de respuesta detallada con etiquetas"""
    etiquetas: List[EtiquetaResponse] = []
