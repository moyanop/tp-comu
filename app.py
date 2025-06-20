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
    print("Sistema de Procesamiento de Audio")
    print("=" * 40)
    print(f"Servidor iniciando en http://{HOST}:{PUERTO}")
    print(f"Documentación: http://{HOST}:{PUERTO}/documentacion")
    print(f"Swagger UI: http://{HOST}:{PUERTO}/docs")
    print("Presiona Ctrl+C para detener el servidor")
    print("-" * 40)
    
    uvicorn.run(
        "backend.aplicacion:aplicacion",
        host=HOST,
        port=PUERTO,
        reload=DEBUG
    ) 