"""
Controlador para rutas de procesamiento de audio
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Form, Query
from fastapi.responses import FileResponse, JSONResponse
from typing import Optional
import os

from backend.servicios.servicio_audio import servicio_audio
from backend.modelo.esquemas import (
    ConfiguracionAudio, 
    RespuestaAudio, 
    DatosFormaOnda, 
    DatosEspectro,
    RespuestaError
)
from backend.configuracion import config

router = APIRouter()

@router.post("/subir", response_model=RespuestaAudio)
async def subir_archivo_audio(audio: UploadFile = File(...)):
    """
    Subir archivo de audio para procesamiento
    
    - **audio**: Archivo de audio (WAV, MP3, FLAC, OGG, M4A)
    """
    try:
        # Validar formato de archivo
        extension = os.path.splitext(audio.filename)[1].lower()
        if extension not in config.FORMATOS_AUDIO_PERMITIDOS:
            raise HTTPException(
                status_code=400,
                detail=f"Formato de archivo no permitido. Formatos válidos: {', '.join(config.FORMATOS_AUDIO_PERMITIDOS)}"
            )
        
        # Leer contenido del archivo
        contenido = await audio.read()
        
        # Validar tamaño del archivo
        if len(contenido) > 50 * 1024 * 1024:  # 50MB
            raise HTTPException(
                status_code=400,
                detail="El archivo es demasiado grande. Máximo 50MB"
            )
        
        # Guardar archivo temporalmente
        archivo_id = servicio_audio.guardar_archivo_temporal(contenido, audio.filename)
        
        return RespuestaAudio(
            mensaje="Archivo subido correctamente",
            archivo_id=archivo_id,
            formato=extension
        )
        
    except Exception as e:
        print(f"Error detallado al subir archivo: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error al subir archivo: {str(e)}")

@router.post("/convertir/{archivo_id}", response_model=RespuestaAudio)
async def convertir_archivo_audio(
    archivo_id: str,
    frecuencia_muestreo: int = Form(config.FRECUENCIA_MUESTREO_DEFAULT),
    bits: int = Form(config.BITS_DEFAULT)
):
    """
    Convertir archivo de audio con nueva configuración
    
    - **archivo_id**: ID del archivo subido
    - **frecuencia_muestreo**: Nueva frecuencia de muestreo (Hz)
    - **bits**: Nueva profundidad de bits
    """
    try:
        # Validar parámetros
        if frecuencia_muestreo < 8000 or frecuencia_muestreo > 192000:
            raise HTTPException(
                status_code=400,
                detail="Frecuencia de muestreo debe estar entre 8000 y 192000 Hz"
            )
        
        if bits not in [8, 16, 24, 32]:
            raise HTTPException(
                status_code=400,
                detail="Bits debe ser 8, 16, 24 o 32"
            )
        
        # Crear configuración
        config = ConfiguracionAudio(
            frecuencia_muestreo=frecuencia_muestreo,
            bits=bits
        )
        
        # Convertir audio
        ruta_procesado = servicio_audio.convertir_audio(archivo_id, config)
        
        return RespuestaAudio(
            mensaje="Audio convertido correctamente",
            archivo_id=archivo_id,
            frecuencia_muestreo=frecuencia_muestreo,
            bits=bits
        )
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al convertir audio: {str(e)}")

@router.get("/forma-onda/{archivo_id}", response_model=DatosFormaOnda)
async def obtener_forma_onda(
    archivo_id: str,
    cantidad_muestras: int = 1000
):
    """
    Obtener datos de forma de onda del archivo de audio
    
    - **archivo_id**: ID del archivo
    - **cantidad_muestras**: Cantidad de muestras para la visualización
    """
    try:
        return servicio_audio.obtener_forma_onda(archivo_id, cantidad_muestras)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener forma de onda: {str(e)}")

@router.get("/espectro/{archivo_id}", response_model=DatosEspectro)
async def obtener_espectro(
    archivo_id: str,
    cantidad_bins: int = 512
):
    """
    Obtener espectro de frecuencia del archivo de audio
    
    - **archivo_id**: ID del archivo
    - **cantidad_bins**: Cantidad de bins para el espectro
    """
    try:
        return servicio_audio.obtener_espectro(archivo_id, cantidad_bins)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener espectro: {str(e)}")

@router.get("/descargar/{archivo_id}")
async def descargar_archivo_audio(archivo_id: str):
    """
    Descargar archivo de audio procesado
    
    - **archivo_id**: ID del archivo
    """
    try:
        ruta_archivo = servicio_audio.obtener_archivo_procesado(archivo_id)
        if not ruta_archivo or not os.path.exists(ruta_archivo):
            raise HTTPException(status_code=404, detail="Archivo no encontrado")
        
        nombre_archivo = f"audio_procesado_{archivo_id}.wav"
        
        return FileResponse(
            path=ruta_archivo,
            filename=nombre_archivo,
            media_type="audio/wav"
        )
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al descargar archivo: {str(e)}")

@router.delete("/limpiar/{archivo_id}")
async def limpiar_archivo_audio(archivo_id: str):
    """
    Limpiar archivos temporales de un archivo específico
    
    - **archivo_id**: ID del archivo a limpiar
    """
    try:
        servicio_audio.limpiar_archivo(archivo_id)
        return {"mensaje": "Archivo limpiado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al limpiar archivo: {str(e)}") 