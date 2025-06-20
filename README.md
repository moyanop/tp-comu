# 🎵 Sistema de Procesamiento de Audio - FastAPI

Sistema web para procesar, convertir y analizar archivos de audio utilizando FastAPI y Python.

## 🚀 Características

- **Subida de archivos**: Soporte para WAV, MP3, FLAC, OGG, M4A
- **Conversión de audio**: Cambio de frecuencia de muestreo y profundidad de bits
- **Análisis de audio**: Visualización de forma de onda y espectro de frecuencia
- **Descarga de archivos**: Descarga de archivos procesados
- **API REST**: Documentación automática con Swagger/OpenAPI
- **Arquitectura MVC**: Separación clara de responsabilidades

## 🏗️ Arquitectura

```
tp-comu/
├── app.py                     # Punto de entrada principal
├── backend/                   # Backend FastAPI
│   ├── aplicacion.py         # Aplicación principal
│   ├── configuracion/        # Configuración del sistema
│   │   ├── __init__.py
│   │   └── config.py
│   ├── controlador/          # Controladores (Routers)
│   │   ├── __init__.py
│   │   ├── rutas_audio.py    # Endpoints de audio
│   │   └── rutas_web.py      # Endpoints web
│   ├── modelo/               # Modelos y esquemas
│   │   ├── __init__.py
│   │   ├── audio.py         # Procesador de audio (legacy)
│   │   └── esquemas.py      # Esquemas Pydantic
│   └── servicios/            # Lógica de negocio
│       ├── __init__.py
│       └── servicio_audio.py # Servicio de procesamiento
├── frontend/                 # Frontend (HTML/CSS/JS)
│   ├── estaticos/
│   │   ├── css/
│   │   └── js/
│   │       └── visualizacion.js
│   └── plantillas/
│       └── principal.html
├── uploads/                  # Archivos subidos (se crea automáticamente)
├── temp/                     # Archivos temporales (se crea automáticamente)
├── requirements.txt          # Dependencias Python
└── README.md
```

## 📋 Requisitos

- Python 3.8+
- pip (gestor de paquetes Python)

## 🛠️ Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd tp-comu
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Iniciar el servidor**
   ```bash
   python app.py
   ```

4. **Acceder a la aplicación**
   - Frontend: http://localhost:8000
   - Documentación API: http://localhost:8000/documentacion
   - Swagger UI: http://localhost:8000/docs

## 🔧 Configuración

Edita el archivo `backend/configuracion/config.py` para personalizar:

```python
# Cambiar puerto del servidor
PUERTO = 8000

# Agregar/quitar formatos de audio soportados
FORMATOS_AUDIO_PERMITIDOS = [".wav", ".mp3", ".flac", ".ogg", ".m4a"]

# Cambiar tamaño máximo de archivo (en bytes)
MAX_TAMANO_ARCHIVO = 50 * 1024 * 1024  # 50MB
```

## 📚 API Endpoints

### Audio

- `POST /api/audio/subir` - Subir archivo de audio
- `POST /api/audio/convertir` - Convertir archivo de audio
- `GET /api/audio/forma-onda/{archivo_id}` - Obtener forma de onda
- `GET /api/audio/espectro/{archivo_id}` - Obtener espectro de frecuencia
- `GET /api/audio/descargar/{archivo_id}` - Descargar archivo procesado
- `DELETE /api/audio/limpiar/{archivo_id}` - Limpiar archivos temporales

### Web

- `GET /` - Página principal
- `GET /documentacion` - Documentación de la API
- `GET /salud` - Verificar estado del servidor

## 🎯 Funcionalidades

### Subida de Archivos
- Soporte para múltiples formatos de audio
- Validación de tamaño y formato
- Almacenamiento temporal seguro

### Procesamiento de Audio
- Conversión de frecuencia de muestreo (8kHz - 192kHz)
- Cambio de profundidad de bits (8, 16, 24, 32 bits)
- Procesamiento en tiempo real

### Análisis de Audio
- Visualización de forma de onda
- Análisis de espectro de frecuencia
- Datos en formato JSON para integración

### Descarga
- Archivos procesados en formato WAV
- Nombres de archivo únicos
- Headers HTTP apropiados

## 🔒 Seguridad

- Validación de tipos de archivo
- Límite de tamaño de archivo
- Limpieza automática de archivos temporales
- Manejo seguro de rutas de archivo

## 🚀 Despliegue

### Desarrollo
```bash
python app.py
```

### Producción
```bash
python app.py
# O cambiar DEBUG = False en config.py
```

## 📝 Tecnologías Utilizadas

- **Backend**: FastAPI, Python 3.8+
- **Procesamiento de Audio**: soundfile, numpy, scipy
- **Validación**: Pydantic
- **Servidor**: Uvicorn
- **Frontend**: HTML5, CSS3, JavaScript
- **Visualización**: Chart.js (frontend)

## 🤝 Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte

Si encuentras algún problema o tienes preguntas:

1. Revisa la documentación de la API en `/documentacion`
2. Verifica los logs del servidor
3. Abre un issue en el repositorio

## 🔄 Changelog

### v1.0.0
- Migración completa a FastAPI
- Arquitectura MVC implementada
- Soporte para múltiples formatos de audio
- API REST documentada
- Sistema de configuración simplificado
- Ejecución simple con `python app.py` 