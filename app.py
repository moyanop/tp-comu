"""
Aplicación principal - Sistema de Procesamiento de Audio
Ejecutar con: python app.py
"""

import uvicorn
import sys
import os

# Agrega el directorio actual al path para los imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.configuracion.config import HOST, PUERTO, DEBUG

if __name__ == "__main__":
    # Usar puerto de Railway si está disponible
    port = int(os.environ.get("PORT", PUERTO))
    host = "0.0.0.0" if os.environ.get("PORT") else HOST
    
    print("Sistema de Procesamiento de Audio")
    print("=" * 40)
    print(f"Servidor iniciando en http://{host}:{port}")
    print(f"Documentación: http://{host}:{port}/documentacion")
    print(f"Swagger UI: http://{host}:{port}/docs")
    print("Presiona Ctrl+C para detener el servidor")
    print("-" * 40)
    
    uvicorn.run(
        "backend.aplicacion:aplicacion",
        host=host,
        port=port,
        reload=DEBUG
    ) 