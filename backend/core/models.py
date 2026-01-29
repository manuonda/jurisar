"""
Modelos SQLAlchemy para la base de datos
"""
from sqlalchemy import Column, Integer, String, Text, Date, Float, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base


class Fallo(Base):
    """Modelo para fallos judiciales"""
    __tablename__ = "fallos"
    
    id = Column(Integer, primary_key=True, index=True)
    caratula = Column(Text, nullable=False)
    fecha_fallo = Column(Date)
    tribunal = Column(String(255))
    expediente = Column(String(100))
    materia = Column(String(100))
    tipo_proceso = Column(String(100))
    juez = Column(String(255))
    texto_completo = Column(Text)
    resumen_ia = Column(Text)
    resultado = Column(String(50))
    url_original = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relaciones
    etiquetas = relationship("FalloEtiqueta", back_populates="fallo", cascade="all, delete-orphan")
    embedding = relationship("Embedding", back_populates="fallo", uselist=False, cascade="all, delete-orphan")


class Etiqueta(Base):
    """Modelo para etiquetas del tesauro jurídico"""
    __tablename__ = "etiquetas"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)
    categoria = Column(String(50))
    descripcion = Column(Text)
    es_generada = Column(String(1), default='N')  # 'S' o 'N'
    
    # Relaciones
    fallos = relationship("FalloEtiqueta", back_populates="etiqueta")


class FalloEtiqueta(Base):
    """Tabla intermedia para relación muchos a muchos entre fallos y etiquetas"""
    __tablename__ = "fallo_etiquetas"
    
    fallo_id = Column(Integer, ForeignKey("fallos.id"), primary_key=True)
    etiqueta_id = Column(Integer, ForeignKey("etiquetas.id"), primary_key=True)
    confianza = Column(Float)
    
    # Relaciones
    fallo = relationship("Fallo", back_populates="etiquetas")
    etiqueta = relationship("Etiqueta", back_populates="fallos")


class Embedding(Base):
    """Modelo para almacenar embeddings vectoriales"""
    __tablename__ = "embeddings"
    
    fallo_id = Column(Integer, ForeignKey("fallos.id"), primary_key=True)
    embedding = Column(String)  # Se almacenará como texto, pgvector lo maneja como vector
    modelo = Column(String(50))
    
    # Relación
    fallo = relationship("Fallo", back_populates="embedding")
