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
from pydub import AudioSegment

from backend.configuracion import config
from backend.modelo.esquemas import ConfiguracionAudio, DatosFormaOnda, DatosEspectro

class ServicioAudio:
    """Servicio para procesamiento de archivos de audio"""
    
    def __init__(self):
        self.archivos_temporales = {}  # Archivos en memoria por sesión
    
    def validar_archivo_audio(self, filename):
        extension = os.path.splitext(filename)[1].lower()
        return extension in [".wav", ".mp3", ".flac", ".ogg", ".m4a", ".webm"]
    
    def guardar_archivo_temporal(self, contenido, extension):
        # Guarda el archivo en el directorio temporal
        pass

    def respuesta_procesamiento(self, archivo_id):
        # Devuelve la respuesta con los datos del archivo procesado
        pass
    
    def guardar_archivo_temporal(self, contenido: bytes, nombre_original: str) -> str:
        """
        Guardar archivo de audio, convertirlo a WAV y retornar ID.
        Esto estandariza el formato para el resto del procesamiento.
        """
        archivo_id = str(uuid.uuid4())
        extension_original = os.path.splitext(nombre_original.lower())[1]
        
        # Asegurarse de que el directorio de temporales existe
        if not os.path.exists(config.DIRECTORIO_TEMPORALES):
            os.makedirs(config.DIRECTORIO_TEMPORALES)

        try:
            # Cargar el audio desde los bytes en memoria
            segmento = AudioSegment.from_file(io.BytesIO(contenido), format=extension_original.replace('.', ''))
            
            # Crear un archivo temporal para el WAV estandarizado
            archivo_wav_temp = tempfile.NamedTemporaryFile(
                delete=False, 
                suffix='.wav',
                dir=config.DIRECTORIO_TEMPORALES
            )
            
            # Exportar el audio a formato WAV (PCM de 16 bits es un buen estándar intermedio)
            segmento.export(archivo_wav_temp.name, format='wav')
            archivo_wav_temp.close()

            # Guardar información del archivo (apuntando al nuevo WAV)
            self.archivos_temporales[archivo_id] = {
                'ruta': archivo_wav_temp.name,
                'nombre_original': nombre_original,
                'procesado': None
            }
            
            return archivo_id

        except FileNotFoundError:
            # Este error usualmente indica que ffmpeg no está instalado o no está en el PATH
            raise IOError(
                "ffmpeg no encontrado. "
                "Por favor, instala ffmpeg y asegúrate de que esté en el PATH de tu sistema para procesar este formato de audio."
            )
        except Exception as e:
            # Si pydub/ffmpeg falla por otra razón, lanzar una excepción para que el controlador la capture
            raise IOError(f"No se pudo procesar el archivo de audio con pydub: {e}")
    
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
        """Convertir archivo de audio con nueva configuración usando pydub."""
        if archivo_id not in self.archivos_temporales:
            raise ValueError("Archivo no encontrado")
        
        ruta_archivo_original = self.archivos_temporales[archivo_id]['ruta']

        try:
            # Cargar audio original con pydub
            segmento = AudioSegment.from_file(ruta_archivo_original)

            # Cambiar frecuencia de muestreo
            segmento = segmento.set_frame_rate(config_audio.frecuencia_muestreo)

            # Cambiar profundidad de bits (sample_width está en bytes: 1=8-bit, 2=16-bit, etc.)
            segmento = segmento.set_sample_width(config_audio.bits // 8)

            # Guardar archivo procesado en un nuevo archivo temporal
            archivo_procesado = tempfile.NamedTemporaryFile(
                delete=False,
                suffix='.wav',
                dir=config.DIRECTORIO_TEMPORALES
            )
            
            segmento.export(archivo_procesado.name, format='wav')
            archivo_procesado.close()
            
            # Limpiar archivo procesado anterior si existía
            if self.archivos_temporales[archivo_id].get('procesado'):
                ruta_antigua = self.archivos_temporales[archivo_id]['procesado']
                if os.path.exists(ruta_antigua):
                    os.unlink(ruta_antigua)

            # Actualizar información del archivo con la nueva ruta
            self.archivos_temporales[archivo_id]['procesado'] = archivo_procesado.name
            
            return archivo_procesado.name
            
        except Exception as e:
            raise IOError(f"Error al convertir audio con pydub: {e}")
    
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