""" Juris - Backend API
Motor de Inteligencia Jurídica y Búsqueda Semántica para la Jurisprudencia Argentina
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Juris - Backend API",
    description="Motor de Inteligencia Jurídica y Búsqueda Semántica para la Jurisprudencia Argentina",
    version="1.0.0"
) 

# Configurar CORS para Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Incluide routers 



@app.get("/")
async def root():
    """Endpoint raiz"""
    return JSONResponse({
        "message": "JurisAR API",
        "version": "1.0.0",
        "status": "running"
    })

@app.get("/health")
async def health_check():
    """ Health check endpoint """
    return JSONResponse({"status": "healthy"})
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

    
