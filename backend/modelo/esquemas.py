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

class ConfiguracionAudio(BaseModel):
    """Esquema para configuración de audio"""
    frecuencia_muestreo: int = Field(default=40000, description="Frecuencia de muestreo en Hz")
    bits: int = Field(default=16, description="Profundidad de bits")

class DatosFormaOnda(BaseModel):
    """Esquema para datos de forma de onda"""
    muestras: List[float] = Field(description="Lista de valores de amplitud")
    cantidad_muestras: int = Field(description="Cantidad total de muestras")
    frecuencia_muestreo: int = Field(description="Frecuencia de muestreo en Hz")

class DatosEspectro(BaseModel):
    """Esquema para datos de espectro de frecuencia"""
    frecuencias: List[float] = Field(description="Lista de frecuencias en Hz")
    magnitudes: List[float] = Field(description="Lista de magnitudes del espectro")
    frecuencia_muestreo: int = Field(description="Frecuencia de muestreo en Hz")

class RespuestaAudio(BaseModel):
    """Esquema para respuesta de audio"""
    mensaje: str = Field(description="Mensaje de respuesta")
    archivo_id: str = Field(description="ID del archivo procesado")
    formato: Optional[str] = Field(default=None, description="Formato del archivo")
    frecuencia_muestreo: Optional[int] = Field(default=None, description="Frecuencia de muestreo")
    bits: Optional[int] = Field(default=None, description="Profundidad de bits")

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