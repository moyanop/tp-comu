"""
Servicio de procesamiento de audio
Maneja la lógica de negocio para procesar archivos de audio
"""

import os
import uuid
import tempfile
from typing import Optional, Tuple, List
import soundfile as sf
import numpy as np
from scipy.fft import fft
from scipy import signal
import matplotlib.pyplot as plt
import io
import base64

from backend.configuracion import config
from backend.modelo.esquemas import ConfiguracionAudio, DatosFormaOnda, DatosEspectro

class ServicioAudio:
    """Servicio para procesamiento de archivos de audio"""
    
    def __init__(self):
        self.archivos_temporales = {}  # Almacena archivos en memoria por sesión
    
    def validar_archivo_audio(self, nombre_archivo: str) -> bool:
        """Validar que el archivo sea un formato de audio permitido"""
        extension = os.path.splitext(nombre_archivo.lower())[1]
        return extension in config.FORMATOS_AUDIO_PERMITIDOS
    
    def guardar_archivo_temporal(self, contenido: bytes, nombre_original: str) -> str:
        """Guardar archivo de audio temporalmente y retornar ID"""
        archivo_id = str(uuid.uuid4())
        
        # Crear archivo temporal
        extension = os.path.splitext(nombre_original.lower())[1]
        archivo_temp = tempfile.NamedTemporaryFile(
            delete=False, 
            suffix=extension,
            dir=config.DIRECTORIO_TEMPORALES
        )
        
        archivo_temp.write(contenido)
        archivo_temp.close()
        
        # Guardar información del archivo
        self.archivos_temporales[archivo_id] = {
            'ruta': archivo_temp.name,
            'nombre_original': nombre_original,
            'procesado': None
        }
        
        return archivo_id
    
    def cargar_audio(self, archivo_id: str) -> Tuple[np.ndarray, int]:
        """Cargar archivo de audio y retornar muestras y frecuencia de muestreo"""
        if archivo_id not in self.archivos_temporales:
            raise ValueError("Archivo no encontrado")
        
        ruta_archivo = self.archivos_temporales[archivo_id]['ruta']
        muestras, frecuencia = sf.read(ruta_archivo, always_2d=False)
        
        return muestras, frecuencia
    
    def convertir_audio(
        self, 
        archivo_id: str, 
        config_audio: ConfiguracionAudio
    ) -> str:
        """Convertir archivo de audio con nueva configuración"""
        if archivo_id not in self.archivos_temporales:
            raise ValueError("Archivo no encontrado")
        
        # Cargar audio original
        muestras, frecuencia_original = self.cargar_audio(archivo_id)
        
        # Convertir a mono si es estéreo
        if muestras.ndim == 2:
            muestras = muestras.mean(axis=1)
        
        # Cambiar frecuencia de muestreo si es necesario
        if frecuencia_original != config_audio.frecuencia_muestreo:
            numero_muestras = int(len(muestras) * config_audio.frecuencia_muestreo / frecuencia_original)
            muestras = signal.resample(muestras, numero_muestras)
        
        # Guardar archivo procesado
        archivo_procesado = tempfile.NamedTemporaryFile(
            delete=False,
            suffix='.wav',
            dir=config.DIRECTORIO_TEMPORALES
        )
        
        # Determinar subtype basado en bits
        if config_audio.bits == 16:
            subtype = 'PCM_16'
        elif config_audio.bits == 24:
            subtype = 'PCM_24'
        elif config_audio.bits == 32:
            subtype = 'PCM_32'
        else:
            subtype = 'PCM_16'
        
        sf.write(
            archivo_procesado.name,
            muestras,
            config_audio.frecuencia_muestreo,
            subtype=subtype
        )
        
        # Actualizar información del archivo
        self.archivos_temporales[archivo_id]['procesado'] = archivo_procesado.name
        
        return archivo_procesado.name
    
    def obtener_forma_onda(self, archivo_id: str, cantidad_muestras: int = 1000) -> DatosFormaOnda:
        """Obtener datos de forma de onda del archivo de audio"""
        if archivo_id not in self.archivos_temporales:
            raise ValueError("Archivo no encontrado")
        
        # Usar archivo procesado si existe, sino el original
        ruta_archivo = (
            self.archivos_temporales[archivo_id].get('procesado') or 
            self.archivos_temporales[archivo_id]['ruta']
        )
        
        muestras, frecuencia = sf.read(ruta_archivo, always_2d=False)
        
        # Convertir a mono si es estéreo
        if muestras.ndim == 2:
            muestras = muestras.mean(axis=1)
        
        # Reducir cantidad de muestras para visualización
        factor = max(1, len(muestras) // cantidad_muestras)
        muestras_reducidas = muestras[::factor]
        
        return DatosFormaOnda(
            muestras=muestras_reducidas.tolist(),
            cantidad_muestras=len(muestras_reducidas),
            frecuencia_muestreo=frecuencia
        )
    
    def obtener_espectro(self, archivo_id: str, cantidad_bins: int = 512) -> DatosEspectro:
        """Obtener espectro de frecuencia del archivo de audio"""
        if archivo_id not in self.archivos_temporales:
            raise ValueError("Archivo no encontrado")
        
        # Usar archivo procesado si existe, sino el original
        ruta_archivo = (
            self.archivos_temporales[archivo_id].get('procesado') or 
            self.archivos_temporales[archivo_id]['ruta']
        )
        
        muestras, frecuencia = sf.read(ruta_archivo, always_2d=False)
        
        # Convertir a mono si es estéreo
        if muestras.ndim == 2:
            muestras = muestras.mean(axis=1)
        
        # Calcular FFT
        espectro = np.abs(fft(muestras))[:cantidad_bins]
        
        # Calcular frecuencias correspondientes
        frecuencias = np.linspace(0, frecuencia/2, cantidad_bins)
        
        return DatosEspectro(
            frecuencias=frecuencias.tolist(),
            magnitudes=espectro.tolist(),
            frecuencia_muestreo=frecuencia
        )
    
    def obtener_archivo_procesado(self, archivo_id: str) -> Optional[str]:
        """Obtener ruta del archivo procesado para descarga"""
        if archivo_id not in self.archivos_temporales:
            return None
        
        return (
            self.archivos_temporales[archivo_id].get('procesado') or 
            self.archivos_temporales[archivo_id]['ruta']
        )
    
    def limpiar_archivo(self, archivo_id: str):
        """Limpiar archivos temporales de un archivo específico"""
        if archivo_id in self.archivos_temporales:
            archivo_info = self.archivos_temporales[archivo_id]
            
            # Eliminar archivo original
            if os.path.exists(archivo_info['ruta']):
                os.unlink(archivo_info['ruta'])
            
            # Eliminar archivo procesado si existe
            if archivo_info.get('procesado') and os.path.exists(archivo_info['procesado']):
                os.unlink(archivo_info['procesado'])
            
            # Remover de la memoria
            del self.archivos_temporales[archivo_id]

# Instancia global del servicio
servicio_audio = ServicioAudio() 