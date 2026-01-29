"""
JurisAR - Backend API
Motor de Inteligencia Jurídica y Búsqueda Semántica
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.routes import search, fallos, etiquetas, embeddings
from core.config import settings

app = FastAPI(
    title="JurisAR API",
    description="Motor de Inteligencia Jurídica y Búsqueda Semántica para la Jurisprudencia Argentina",
    version="1.0.0"
)

# Configurar CORS para Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(search.router, prefix="/api/v1/search", tags=["Búsqueda"])
app.include_router(fallos.router, prefix="/api/v1/fallos", tags=["Fallos"])
app.include_router(etiquetas.router, prefix="/api/v1/etiquetas", tags=["Etiquetas"])
app.include_router(embeddings.router, prefix="/api/v1/embeddings", tags=["Embeddings"])


@app.get("/")
async def root():
    """Endpoint raíz"""
    return JSONResponse({
        "message": "JurisAR API",
        "version": "1.0.0",
        "status": "running"
    })


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse({"status": "healthy"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
