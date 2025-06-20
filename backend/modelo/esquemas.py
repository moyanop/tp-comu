"""
Esquemas Pydantic para validación de datos
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ConfiguracionAudio(BaseModel):
    """Esquema para configuración de conversión de audio"""
    frecuencia_muestreo: int = Field(
        default=44100, 
        ge=8000, 
        le=192000, 
        description="Frecuencia de muestreo en Hz"
    )
    bits: int = Field(
        default=16, 
        ge=8, 
        le=32, 
        description="Profundidad de bits"
    )

class RespuestaAudio(BaseModel):
    """Esquema para respuesta de procesamiento de audio"""
    mensaje: str
    archivo_id: Optional[str] = None
    formato: Optional[str] = None
    duracion: Optional[float] = None
    frecuencia_muestreo: Optional[int] = None
    bits: Optional[int] = None

class DatosFormaOnda(BaseModel):
    """Esquema para datos de forma de onda"""
    muestras: List[float]
    cantidad_muestras: int
    frecuencia_muestreo: int

class DatosEspectro(BaseModel):
    """Esquema para datos de espectro de frecuencia"""
    frecuencias: List[float]
    magnitudes: List[float]
    frecuencia_muestreo: int

class InformacionArchivo(BaseModel):
    """Esquema para información de archivo de audio"""
    nombre: str
    formato: str
    tamano_bytes: int
    duracion_segundos: float
    frecuencia_muestreo: int
    canales: int
    bits: int
    fecha_subida: datetime

class RespuestaError(BaseModel):
    """Esquema para respuestas de error"""
    error: str
    detalles: Optional[str] = None
    codigo: Optional[int] = None

class RespuestaExito(BaseModel):
    """Esquema para respuestas exitosas"""
    mensaje: str
    datos: Optional[dict] = None 