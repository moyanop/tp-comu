"""
Aplicación principal FastAPI para procesamiento de audio
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

from backend.controlador.rutas_audio import router as router_audio
from backend.controlador.rutas_web import router as router_web

# Crear instancia de FastAPI
aplicacion = FastAPI(
    title="Sistema de Procesamiento de Audio",
    description="API para procesar, convertir y analizar archivos de audio",
    version="1.0.0",
    docs_url="/documentacion",
    redoc_url="/documentacion-redoc"
)

# CORS abierto para desarrollo
aplicacion.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar archivos estáticos
ruta_estaticos = os.path.join(os.path.dirname(__file__), "..", "frontend", "estaticos")
if os.path.exists(ruta_estaticos):
    aplicacion.mount("/estaticos", StaticFiles(directory=ruta_estaticos), name="estaticos")

# Configurar templates
ruta_templates = os.path.join(os.path.dirname(__file__), "..", "frontend", "plantillas")
templates = Jinja2Templates(directory=ruta_templates)

# Incluir routers
aplicacion.include_router(router_web, prefix="", tags=["Web"])
aplicacion.include_router(router_audio, prefix="/api/audio", tags=["Audio"])

@aplicacion.get("/")
async def raiz():
    """Endpoint raíz de la aplicación"""
    return {
        "mensaje": "Sistema de Procesamiento de Audio",
        "version": "1.0.0",
        "documentacion": "/documentacion"
    }

@aplicacion.get("/salud")
async def verificar_salud():
    """Endpoint para verificar el estado de la aplicación"""
    return {"estado": "funcionando", "servicio": "procesamiento_audio"} 