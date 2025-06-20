# Conversor de Audio Analógico a Digital (Python + Flask)

## Estructura del Proyecto

```
tp-comu-py/
│
├── backend/
│   ├── app.py                # Punto de entrada Flask
│   ├── modelo/               # Lógica de negocio y datos
│   ├── controlador/          # Rutas y lógica de interacción
│   └── base_datos/           # (Opcional) Modelos y gestión de BD
│
├── frontend/
│   ├── plantillas/           # HTML (Jinja2)
│   └── estaticos/            # JS y CSS
│
├── requirements.txt          # Dependencias del proyecto
└── README.md                 # Documentación
```

## ¿Cómo correr el proyecto?

1. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Ejecuta la aplicación:
   ```bash
   python backend/app.py
   ```
3. Abre tu navegador en [http://localhost:5000](http://localhost:5000)

## ¿Qué hace este proyecto?
- Permite grabar o cargar archivos de audio
- Convierte el audio a diferentes frecuencias de muestreo y profundidades de bits
- Visualiza la forma de onda y el espectro de frecuencia de manera interactiva (JS)
- Permite exportar el audio procesado

## Tecnologías utilizadas
- **Flask** (Python) para backend y servidor
- **Bootstrap** para la interfaz
- **JavaScript** puro para la visualización interactiva
- **pydub, numpy, scipy, matplotlib** para procesamiento de audio

## Notas
- Todo el código está en español y estructurado siguiendo el patrón MVC
- Puedes modificar y mejorar la visualización en `frontend/estaticos/js/visualizacion.js`
- Si necesitas persistencia, puedes usar la carpeta `backend/base_datos/` 