"""
Esquemas Pydantic para validación de datos
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ConfiguracionConversion(BaseModel):
    """Esquema para configuración de conversión de audio"""
    frecuencia_muestreo: int
    bits: int

class RespuestaProcesamientoAudio(BaseModel):
    """Esquema para respuesta de procesamiento de audio"""
    archivo_id: str
    mensaje: str
    formato: str

class FormaOnda(BaseModel):
    """Esquema para datos de forma de onda"""
    muestras: List[float]
    frecuencia_muestreo: int

class EspectroFrecuencia(BaseModel):
    """Esquema para datos de espectro de frecuencia"""
    frecuencias: List[float]
    magnitudes: List[float]

class InfoArchivoAudio(BaseModel):
    """Esquema para información de archivo de audio"""
    archivo_id: str
    nombre: str
    formato: str
    tamano: int

class RespuestaError(BaseModel):
    """Esquema para respuestas de error"""
    error: str

class RespuestaExito(BaseModel):
    """Esquema para respuestas exitosas"""
    mensaje: str 