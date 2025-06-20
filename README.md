# Sistema de Procesamiento de Audio - FastAPI

Sistema web para procesar, convertir y analizar archivos de audio usando FastAPI y Python.

## Características

- Subida de archivos: Soporte para WAV, MP3, FLAC, OGG, M4A, WEBM
- Conversión de audio: Cambio de frecuencia de muestreo y profundidad de bits
- Análisis de audio: Visualización de forma de onda y espectro de frecuencia
- Descarga de archivos procesados
- API REST con documentación automática

## Estructura del proyecto

```
tp-comu/
├── app.py                  # Punto de entrada principal
├── backend/                # Backend FastAPI
│   ├── aplicacion.py       # Aplicación principal
│   ├── configuracion/      # Configuración
│   │   ├── __init__.py
│   │   └── config.py
│   ├── controlador/        # Routers
│   │   ├── __init__.py
│   │   ├── rutas_audio.py  # Endpoints de audio
│   │   └── rutas_web.py    # Endpoints web
│   ├── modelo/             # Modelos y esquemas
│   │   ├── __init__.py
│   │   └── esquemas.py     # Esquemas Pydantic
│   └── servicios/          # Lógica de negocio
│       ├── __init__.py
│       └── servicio_audio.py
├── frontend/               # Frontend (HTML/JS)
│   ├── estaticos/
│   │   └── js/
│   │       └── visualizacion.js
│   └── plantillas/
│       └── principal.html
├── uploads/                # Archivos subidos (se crea automáticamente)
├── temp/                   # Archivos temporales (se crea automáticamente)
├── requirements.txt        # Dependencias Python
└── README.md
```

## Requisitos

- Python 3.8 a 3.12 (no compatible con 3.13)
- pip

## Instalación

1. Clona el repositorio
   ```bash
   git clone <url-del-repositorio>
   cd tp-comu
   ```
2. Instala las dependencias
   ```bash
   pip install -r requirements.txt
   ```
3. Inicia el servidor
   ```bash
   python app.py
   ```
4. Accede a la aplicación
   - Frontend: http://localhost:8000
   - Documentación API: http://localhost:8000/documentacion
   - Swagger UI: http://localhost:8000/docs

## Configuración

Edita `backend/configuracion/config.py` para personalizar:
- Puerto del servidor
- Formatos de audio soportados
- Tamaño máximo de archivo

## Endpoints principales

- `POST /api/audio/subir` - Subir archivo de audio
- `POST /api/audio/convertir` - Convertir archivo de audio
- `GET /api/audio/forma-onda/{archivo_id}` - Obtener forma de onda
- `GET /api/audio/espectro/{archivo_id}` - Obtener espectro de frecuencia
- `GET /api/audio/descargar/{archivo_id}` - Descargar archivo procesado
- `DELETE /api/audio/limpiar/{archivo_id}` - Limpiar archivos temporales
- `GET /` - Página principal
- `GET /documentacion` - Documentación de la API
- `GET /salud` - Verificar estado del servidor

## Tecnologías utilizadas

- FastAPI
- Uvicorn
- soundfile, numpy, scipy, pydub
- HTML5, JavaScript

## Notas

- El proyecto no es compatible con Python 3.13 por dependencias de audio.
- Los directorios `uploads` y `temp` se crean automáticamente.

## Licencia

MIT
