# Sistema de Procesamiento de Audio - Documentación Técnica

## 📋 Descripción General

Este sistema permite **subir, procesar y visualizar archivos de audio** con control total sobre parámetros como frecuencia de muestreo y profundidad de bits. La aplicación está construida con **FastAPI** en el backend y **HTML/JavaScript** en el frontend.

---

## 🏗️ Arquitectura del Sistema

### Backend (Python/FastAPI)
```
backend/
├── aplicacion.py          # Configuración principal de FastAPI
├── controlador/
│   └── rutas_audio.py    # Endpoints para procesamiento de audio
├── servicios/
│   └── servicio_audio.py # Lógica de negocio - CORAZÓN DEL SISTEMA
├── modelo/
│   └── esquemas.py       # Esquemas Pydantic para validación
└── configuracion/
    └── config.py         # Configuración del sistema
```

---

## 🛠️ Librerías Críticas y su Uso

### 1. **pydub** - Procesamiento de Audio
```python
from pydub import AudioSegment
```
**¿Qué hace?** Convierte archivos de audio entre formatos (MP3, WAV, WEBM, etc.)

**Uso crítico en el código:**
```python
# Cargar archivo desde bytes en memoria
segmento = AudioSegment.from_file(io.BytesIO(contenido), format='webm')

# Cambiar frecuencia de muestreo
segmento = segmento.set_frame_rate(44100)

# Cambiar profundidad de bits (8, 16, 24, 32 bits)
segmento = segmento.set_sample_width(2)  # 2 bytes = 16 bits

# Exportar a WAV
segmento.export("archivo.wav", format='wav')
```

### 2. **soundfile** - Lectura/Escritura de Audio
```python
import soundfile as sf
```
**¿Qué hace?** Lee archivos de audio y los convierte a arrays de NumPy para análisis

**Uso crítico:**
```python
# Leer archivo WAV
muestras, frecuencia = sf.read("archivo.wav")

# muestras = array de amplitudes [-1.0 a 1.0]
# frecuencia = frecuencia de muestreo (ej: 44100 Hz)
```

### 3. **scipy** - Análisis de Frecuencias
```python
from scipy.fft import fft
```
**¿Qué hace?** Calcula la Transformada Rápida de Fourier para obtener el espectro de frecuencias

**Uso crítico:**
```python
# Calcular espectro de frecuencias
espectro = np.abs(fft(muestras))[:512]
frecuencias = np.linspace(0, frecuencia/2, 512)
```

---

## 🔄 Flujo Crítico: Subida y Procesamiento de Audio

### Paso 1: Subida de Archivo
**Archivo:** `backend/controlador/rutas_audio.py`
```python
@router.post("/subir", response_model=RespuestaAudio)
async def subir_archivo_audio(audio: UploadFile = File(...)):
    # 1. Validar formato
    extension = os.path.splitext(audio.filename)[1].lower()
    
    # 2. Leer contenido
    contenido = await audio.read()
    
    # 3. Guardar y procesar
    archivo_id = servicio_audio.guardar_archivo_temporal(contenido, audio.filename)
```

### Paso 2: Procesamiento con pydub
**Archivo:** `backend/servicios/servicio_audio.py`
```python
def guardar_archivo_temporal(self, contenido: bytes, nombre_original: str) -> str:
    # 1. Detectar formato
    extension_original = os.path.splitext(nombre_original.lower())[1]
    
    # 2. Cargar con pydub
    segmento = AudioSegment.from_file(io.BytesIO(contenido), format='webm')
    
    # 3. Convertir a WAV estándar
    segmento.export(archivo_wav_temp.name, format='wav')
```

### Paso 3: Conversión con Parámetros Personalizados
**Archivo:** `backend/servicios/servicio_audio.py`
```python
def convertir_audio(self, archivo_id: str, config_audio: ConfiguracionAudio) -> str:
    # 1. Cargar audio original
    segmento = AudioSegment.from_file(ruta_archivo_original)
    
    # 2. Cambiar frecuencia de muestreo
    segmento = segmento.set_frame_rate(config_audio.frecuencia_muestreo)
    
    # 3. Cambiar profundidad de bits
    segmento = segmento.set_sample_width(config_audio.bits // 8)
    
    # 4. Exportar con nueva configuración
    segmento.export(archivo_procesado.name, format='wav')
```

---

## 📊 Análisis y Visualización

### Forma de Onda
**Archivo:** `backend/servicios/servicio_audio.py`
```python
def obtener_forma_onda(self, archivo_id: str, cantidad_muestras: int = 1000):
    # 1. Leer archivo con soundfile
    muestras, frecuencia = sf.read(ruta_archivo)
    
    # 2. Convertir a mono si es estéreo
    if muestras.ndim == 2:
        muestras = muestras.mean(axis=1)
    
    # 3. Reducir muestras para visualización
    factor = max(1, len(muestras) // cantidad_muestras)
    muestras_reducidas = muestras[::factor]
```

### Espectro de Frecuencias
```python
def obtener_espectro(self, archivo_id: str, cantidad_bins: int = 512):
    # 1. Leer archivo
    muestras, frecuencia = sf.read(ruta_archivo)
    
    # 2. Calcular FFT
    espectro = np.abs(fft(muestras))[:cantidad_bins]
    
    # 3. Calcular frecuencias correspondientes
    frecuencias = np.linspace(0, frecuencia/2, cantidad_bins)
```

---

## 🔧 Configuración Crítica

### Configuración de ffmpeg
**Archivo:** `backend/servicios/servicio_audio.py`
```python
def _configurar_ffmpeg(self):
    # pydub necesita ffmpeg para procesar formatos como MP3, WEBM
    rutas_posibles = [
        "ffmpeg",  # Si está en PATH
        r"C:\Users\pedro\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
    ]
    
    for ruta in rutas_posibles:
        if os.path.exists(ruta):
            AudioSegment.converter = ruta  # Configurar pydub
```

### Parámetros de Audio
**Archivo:** `backend/configuracion/config.py`
```python
# Formatos soportados
FORMATOS_AUDIO_PERMITIDOS = [".wav", ".mp3", ".flac", ".ogg", ".m4a", ".webm"]

# Configuración por defecto
FRECUENCIA_MUESTREO_DEFAULT = 40000  # Hz
BITS_DEFAULT = 16  # bits
```

---

## 🎯 Puntos Clave para la Exposición

### 1. **Procesamiento Multi-formato**
- El sistema acepta **6 formatos diferentes** de audio
- **pydub** convierte todo a WAV internamente
- **ffmpeg** es crítico para formatos como MP3, WEBM

### 2. **Control de Calidad de Audio**
- **Frecuencia de muestreo**: 8000 Hz - 192000 Hz
- **Profundidad de bits**: 8, 16, 24, 32 bits
- Conversión en tiempo real sin pérdida de calidad

### 3. **Análisis Técnico**
- **Forma de onda**: Visualización de amplitud vs tiempo
- **Espectro**: Análisis de frecuencias usando FFT
- **Reducción de datos**: Optimización para visualización web

### 4. **Arquitectura Robusta**
- **Separación de responsabilidades**: Controlador → Servicio → Modelo
- **Manejo de errores**: Validación de formatos y parámetros
- **Archivos temporales**: Gestión automática de memoria

---

## 🚀 Comandos para Ejecutar

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
python app.py

# Acceder a la aplicación
http://localhost:8000
```

---

## 🔄 Flujo de Usuario

1. **Subir/Grabar** → Archivo de audio (WEBM, MP3, etc.)
2. **Procesar** → Conversión a WAV con parámetros estándar
3. **Convertir** → Aplicar nueva frecuencia y profundidad de bits
4. **Visualizar** → Forma de onda y espectro de frecuencias
5. **Descargar** → Archivo procesado en formato WAV

**¡El sistema demuestra control total sobre la calidad y características del audio!**

---

## 📝 Notas Técnicas Adicionales

### Manejo de Errores
- Validación de formatos de archivo
- Verificación de tamaño máximo (50MB)
- Manejo de errores de ffmpeg
- Limpieza automática de archivos temporales

### Optimizaciones
- Reducción de muestras para visualización
- Conversión a mono para análisis
- Uso de archivos temporales para evitar pérdida de memoria
- Configuración automática de ffmpeg

### Seguridad
- Validación de tipos de archivo
- Sanitización de nombres de archivo
- Límites de tamaño de archivo
- Gestión segura de archivos temporales 