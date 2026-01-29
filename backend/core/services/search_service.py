"""
Servicio de búsqueda semántica e híbrida
"""
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, List
from core.config import settings
from core.services.embedding_service import EmbeddingService


class SearchService:
    """Servicio para búsqueda de fallos"""
    
    def __init__(self, db: Session):
        self.db = db
        self.embedding_service = EmbeddingService(db)
    
    async def buscar_semantica(
        self,
        query: str,
        limit: int = 10,
        materia: Optional[str] = None,
        tipo_proceso: Optional[str] = None
    ):
        """
        Búsqueda semántica usando embeddings
        """
        # Generar embedding de la consulta
        query_embedding_vector = await self.embedding_service.generar_embedding(query)
        # Convertir a formato pgvector
        query_embedding_str = "[" + ",".join(map(str, query_embedding_vector)) + "]"
        
        # Construir query SQL con pgvector
        sql = """
        SELECT 
            f.id,
            f.caratula,
            f.resumen_ia,
            f.fecha_fallo,
            f.tribunal,
            f.materia,
            1 - (e.embedding <=> :query_embedding::vector) as similitud
        FROM fallos f
        JOIN embeddings e ON f.id = e.fallo_id
        WHERE 1=1
        """
        params = {"query_embedding": query_embedding_str}
        
        if materia:
            sql += " AND f.materia = :materia"
            params["materia"] = materia
        
        if tipo_proceso:
            sql += " AND f.tipo_proceso = :tipo_proceso"
            params["tipo_proceso"] = tipo_proceso
        
        sql += " ORDER BY e.embedding <=> :query_embedding::vector LIMIT :limit"
        params["limit"] = limit
        
        result = self.db.execute(text(sql), params)
        return [dict(row) for row in result]
    
    async def buscar_hibrida(
        self,
        query: str,
        limit: int = 10,
        etiquetas: Optional[List[str]] = None,
        materia: Optional[str] = None,
        fecha_desde: Optional[str] = None,
        fecha_hasta: Optional[str] = None
    ):
        """
        Búsqueda híbrida: combina filtros SQL con similitud vectorial
        """
        # Generar embedding de la consulta
        query_embedding_vector = await self.embedding_service.generar_embedding(query)
        # Convertir a formato pgvector
        query_embedding_str = "[" + ",".join(map(str, query_embedding_vector)) + "]"
        
        # Construir query SQL con filtros y ordenamiento por similitud
        sql = """
        SELECT DISTINCT
            f.id,
            f.caratula,
            f.resumen_ia,
            f.fecha_fallo,
            f.tribunal,
            f.materia,
            1 - (e.embedding <=> :query_embedding::vector) as similitud
        FROM fallos f
        JOIN embeddings e ON f.id = e.fallo_id
        WHERE 1=1
        """
        params = {"query_embedding": query_embedding_str}
        
        if materia:
            sql += " AND f.materia = :materia"
            params["materia"] = materia
        
        if fecha_desde:
            sql += " AND f.fecha_fallo >= :fecha_desde"
            params["fecha_desde"] = fecha_desde
        
        if fecha_hasta:
            sql += " AND f.fecha_fallo <= :fecha_hasta"
            params["fecha_hasta"] = fecha_hasta
        
        if etiquetas:
            sql += """
            AND f.id IN (
                SELECT fe.fallo_id 
                FROM fallo_etiquetas fe
                JOIN etiquetas et ON fe.etiqueta_id = et.id
                WHERE et.nombre = ANY(:etiquetas)
            )
            """
            params["etiquetas"] = etiquetas
        
        sql += " ORDER BY e.embedding <=> :query_embedding::vector LIMIT :limit"
        params["limit"] = limit
        
        result = self.db.execute(text(sql), params)
        return [dict(row) for row in result]
