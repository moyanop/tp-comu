"""
Controlador para rutas web (frontend)
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()

# Configuración de templates
ruta_templates = os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "plantillas")
templates = Jinja2Templates(directory=ruta_templates)

@router.get("/", response_class=HTMLResponse)
def pagina_principal(request: Request):
    """
    Página principal de la aplicación
    """
    return templates.TemplateResponse(
        "principal.html",
        {
            "request": request,
            "titulo": "Sistema de Procesamiento de Audio",
            "version": "1.0.0"
        }
    )

@router.get("/documentacion", response_class=HTMLResponse)
async def pagina_documentacion(request: Request):
    """
    Página de documentación de la API
    """
    return templates.TemplateResponse(
        "documentacion.html",
        {
            "request": request,
            "titulo": "Documentación API",
            "endpoints": [
                {
                    "ruta": "/api/audio/subir",
                    "metodo": "POST",
                    "descripcion": "Subir archivo de audio"
                },
                {
                    "ruta": "/api/audio/convertir",
                    "metodo": "POST",
                    "descripcion": "Convertir archivo de audio"
                },
                {
                    "ruta": "/api/audio/forma-onda/{archivo_id}",
                    "metodo": "GET",
                    "descripcion": "Obtener forma de onda"
                },
                {
                    "ruta": "/api/audio/espectro/{archivo_id}",
                    "metodo": "GET",
                    "descripcion": "Obtener espectro de frecuencia"
                },
                {
                    "ruta": "/api/audio/descargar/{archivo_id}",
                    "metodo": "GET",
                    "descripcion": "Descargar archivo procesado"
                }
            ]
        }
    ) 