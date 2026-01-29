"""
Servicio para generación de embeddings usando OpenAI
"""
import openai
from sqlalchemy.orm import Session
from core.config import settings
from core.models import Fallo, Embedding


class EmbeddingService:
    """Servicio para generar y gestionar embeddings"""
    
    def __init__(self, db: Session):
        self.db = db
        openai.api_key = settings.OPENAI_API_KEY
    
    async def generar_embedding(self, texto: str) -> list:
        """
        Genera un embedding vectorial para un texto
        """
        from openai import OpenAI
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
        response = client.embeddings.create(
            model=settings.OPENAI_EMBEDDING_MODEL,
            input=texto
        )
        
        return response.data[0].embedding
    
    async def generar_embedding_fallo(self, fallo_id: int) -> bool:
        """
        Genera y almacena el embedding para un fallo
        El documento de búsqueda se compone de:
        Carátula + Resumen IA + Etiquetas + Normativa Clave
        """
        fallo = self.db.query(Fallo).filter(Fallo.id == fallo_id).first()
        if not fallo:
            raise ValueError(f"Fallo {fallo_id} no encontrado")
        
        # Construir documento de búsqueda
        documento_busqueda = f"{fallo.caratula}\n\n"
        
        if fallo.resumen_ia:
            documento_busqueda += f"{fallo.resumen_ia}\n\n"
        
        # Agregar etiquetas si existen
        if fallo.etiquetas:
            etiquetas_texto = ", ".join([fe.etiqueta.nombre for fe in fallo.etiquetas])
            documento_busqueda += f"Etiquetas: {etiquetas_texto}\n\n"
        
        # Generar embedding
        embedding_vector = await self.generar_embedding(documento_busqueda)
        
        # Convertir a formato pgvector (usando text() para convertir a string de vector)
        # pgvector espera el formato: '[0.1,0.2,0.3,...]'
        embedding_str = "[" + ",".join(map(str, embedding_vector)) + "]"
        
        # Guardar o actualizar embedding usando SQL directo para pgvector
        from sqlalchemy import text
        
        # Verificar si ya existe
        existing = self.db.execute(
            text("SELECT fallo_id FROM embeddings WHERE fallo_id = :fallo_id"),
            {"fallo_id": fallo_id}
        ).first()
        
        if existing:
            # Actualizar
            self.db.execute(
                text("UPDATE embeddings SET embedding = :embedding::vector, modelo = :modelo WHERE fallo_id = :fallo_id"),
                {
                    "embedding": embedding_str,
                    "modelo": settings.OPENAI_EMBEDDING_MODEL,
                    "fallo_id": fallo_id
                }
            )
        else:
            # Insertar nuevo
            self.db.execute(
                text("INSERT INTO embeddings (fallo_id, embedding, modelo) VALUES (:fallo_id, :embedding::vector, :modelo)"),
                {
                    "fallo_id": fallo_id,
                    "embedding": embedding_str,
                    "modelo": settings.OPENAI_EMBEDDING_MODEL
                }
            )
        
        self.db.commit()
        return True
