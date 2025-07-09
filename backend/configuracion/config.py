"""
Configuración del sistema (editable directamente)
"""

# Configuración principal
NOMBRE_APLICACION = "Sistema de Procesamiento de Audio"
VERSION = "1.0.0"
DEBUG = True

# Servidor
HOST = "localhost"
PUERTO = 8000

# Archivos
DIRECTORIO_UPLOADS = "uploads"
DIRECTORIO_TEMPORALES = "temp"
MAX_TAMANO_ARCHIVO = 50 * 1024 * 1024  # 50MB

# Audio
FORMATOS_AUDIO_PERMITIDOS = [".wav", ".mp3", ".flac", ".ogg", ".m4a", ".webm"]
FRECUENCIA_MUESTREO_DEFAULT = 40000
BITS_DEFAULT = 16

import os

def crear_directorios():
    """Crear directorios necesarios para la aplicación"""
    for directorio in [DIRECTORIO_UPLOADS, DIRECTORIO_TEMPORALES]:
        if not os.path.exists(directorio):
            os.makedirs(directorio)
            print(f"Directorio creado: {directorio}")

crear_directorios() 