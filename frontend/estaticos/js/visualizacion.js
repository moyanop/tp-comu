// visualizacion.js
// Lógica para interactuar con el backend y visualizar audio

document.addEventListener('DOMContentLoaded', function () {
    // Elementos
    const formAudio = document.getElementById('form-audio');
    const inputAudio = document.getElementById('input-audio');
    const mensajeAudio = document.getElementById('mensaje-audio');
    const formConversion = document.getElementById('form-conversion');
    const mensajeConversion = document.getElementById('mensaje-conversion');
    const canvasOnda = document.getElementById('canvas-onda');
    const canvasEspectro = document.getElementById('canvas-espectro');
    const btnDescargar = document.getElementById('btn-descargar');
    // Grabación
    const btnGrabar = document.getElementById('btn-grabar');
    const btnDetener = document.getElementById('btn-detener');
    const grabandoLabel = document.getElementById('grabando-label');
    const audioPreview = document.getElementById('audio-preview');

    let mediaRecorder = null;
    let audioChunks = [];
    let blobGrabado = null;
    let archivoIdActual = null; // Guardar ID del archivo subido

    // Grabación de audio
    btnGrabar.addEventListener('click', async function () {
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            alert('Tu navegador no soporta grabación de audio');
            return;
        }
        btnGrabar.classList.add('d-none');
        btnDetener.classList.remove('d-none');
        grabandoLabel.classList.remove('d-none');
        audioPreview.classList.add('d-none');
        mensajeAudio.textContent = '';
        audioChunks = [];
        blobGrabado = null;
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.ondataavailable = e => {
            if (e.data.size > 0) audioChunks.push(e.data);
        };
        mediaRecorder.onstop = () => {
            const blob = new Blob(audioChunks, { type: 'audio/webm' });
            blobGrabado = blob;
            audioPreview.src = URL.createObjectURL(blob);
            audioPreview.classList.remove('d-none');
            // Limpiar input file para evitar confusión
            inputAudio.value = '';
        };
        mediaRecorder.start();
    });

    btnDetener.addEventListener('click', function () {
        if (mediaRecorder && mediaRecorder.state === 'recording') {
            mediaRecorder.stop();
        }
        btnGrabar.classList.remove('d-none');
        btnDetener.classList.add('d-none');
        grabandoLabel.classList.add('d-none');
    });

    // Subir audio (grabado o cargado)
    formAudio.addEventListener('submit', async function (e) {
        e.preventDefault();
        
        // Ocultar reproductor convertido al subir nuevo audio
        document.getElementById('app-reproductor-convertido').classList.add('d-none');
        
        let archivo = inputAudio.files[0];
        if (!archivo && blobGrabado) {
            archivo = new File([blobGrabado], 'grabacion.webm', { type: 'audio/webm' });
        }
        if (!archivo) {
            mensajeAudio.textContent = 'Selecciona o graba un archivo de audio.';
            return;
        }
        const formData = new FormData();
        formData.append('audio', archivo);
        mensajeAudio.textContent = 'Subiendo...';
        const resp = await fetch('/api/audio/subir', {
            method: 'POST',
            body: formData
        });
        const data = await resp.json();
        if (resp.ok) {
            mensajeAudio.textContent = data.mensaje;
            archivoIdActual = data.archivo_id; // Guardar el ID
            await actualizarVisualizacion();
            
            // Actualizar y mostrar el reproductor de audio convertido
            const appReproductor = document.getElementById('app-reproductor-convertido');
            const audioPlayer = document.getElementById('audio-convertido-preview');
            
            // Se agrega un timestamp para evitar que el navegador use una versión en caché del audio
            const audioUrl = `/api/audio/descargar/${archivoIdActual}?t=${new Date().getTime()}`;
            
            audioPlayer.src = audioUrl;
            audioPlayer.load();
            appReproductor.classList.remove('d-none');

        } else {
            mensajeAudio.textContent = data.error || 'Error al subir audio.';
        }
    });

    // Convertir audio
    formConversion.addEventListener('submit', async function (e) {
        e.preventDefault();
        if (!archivoIdActual) {
            mensajeConversion.textContent = 'Primero debes subir un archivo.';
            return;
        }

        try {
            const frecuencia = document.getElementById('frecuencia').value;
            const bits = document.getElementById('bits').value;
            
            const formData = new FormData();
            formData.append('frecuencia_muestreo', frecuencia);
            formData.append('bits', bits);

            mensajeConversion.textContent = 'Convirtiendo...';
            const resp = await fetch(`/api/audio/convertir/${archivoIdActual}`, {
                method: 'POST',
                body: formData
            });

            const data = await resp.json();

            if (resp.ok) {
                mensajeConversion.textContent = data.mensaje;
                archivoIdActual = data.archivo_id; 
                await actualizarVisualizacion();

                // Actualizar y mostrar el reproductor de audio convertido
                const appReproductor = document.getElementById('app-reproductor-convertido');
                const audioPlayer = document.getElementById('audio-convertido-preview');
                
                // Se agrega un timestamp para evitar que el navegador use una versión en caché del audio
                const audioUrl = `/api/audio/descargar/${archivoIdActual}?t=${new Date().getTime()}`;
                
                audioPlayer.src = audioUrl;
                audioPlayer.load();
                appReproductor.classList.remove('d-none');

            } else {
                // Muestra un error más detallado del servidor
                mensajeConversion.textContent = `Error del servidor: ${data.detail || data.error || 'Error desconocido.'}`;
            }
        } catch (error) {
            // Muestra errores de red o del script
            console.error('Error en la función de conversión:', error);
            mensajeConversion.textContent = `Error de conexión o en el script: ${error.message}`;
        }
    });

    // Descargar audio procesado
    btnDescargar.addEventListener('click', function (e) {
        if (!archivoIdActual) {
            e.preventDefault();
            alert('No hay un archivo procesado para descargar. Sube y convierte un audio primero.');
            return;
        }
        btnDescargar.href = `/api/audio/descargar/${archivoIdActual}`;
    });

    // Visualización de forma de onda y espectro
    async function actualizarVisualizacion() {
        if (!archivoIdActual) return;

        // Forma de onda
        const respOnda = await fetch(`/api/audio/forma-onda/${archivoIdActual}`);
        const dataOnda = await respOnda.json();
        if (respOnda.ok && dataOnda.muestras) {
            graficarFormaOnda(dataOnda.muestras);
        } else {
            graficarFormaOnda([]);
        }
        // Espectro
        const respEspectro = await fetch(`/api/audio/espectro/${archivoIdActual}`);
        const dataEspectro = await respEspectro.json();
        if (respEspectro.ok && dataEspectro.magnitudes) {
            graficarEspectro(dataEspectro.magnitudes);
        } else {
            graficarEspectro([]);
        }
    }

    // Graficar forma de onda
    function graficarFormaOnda(datos) {
        const ctx = canvasOnda.getContext('2d');
        ctx.clearRect(0, 0, canvasOnda.width, canvasOnda.height);
        ctx.beginPath();
        if (datos.length > 0) {
            for (let i = 0; i < datos.length; i++) {
                const x = (i / datos.length) * canvasOnda.width;
                const y = (1 - (datos[i] - Math.min(...datos)) / (Math.max(...datos) - Math.min(...datos) || 1)) * canvasOnda.height;
                if (i === 0) ctx.moveTo(x, y);
                else ctx.lineTo(x, y);
            }
        }
        ctx.strokeStyle = '#007bff';
        ctx.lineWidth = 2;
        ctx.stroke();
    }

    // Graficar espectro
    function graficarEspectro(datos) {
        const ctx = canvasEspectro.getContext('2d');
        ctx.clearRect(0, 0, canvasEspectro.width, canvasEspectro.height);
        ctx.beginPath();
        if (datos.length > 0) {
            for (let i = 0; i < datos.length; i++) {
                const x = (i / datos.length) * canvasEspectro.width;
                const y = canvasEspectro.height - (datos[i] / Math.max(...datos)) * canvasEspectro.height;
                if (i === 0) ctx.moveTo(x, y);
                else ctx.lineTo(x, y);
            }
        }
        ctx.strokeStyle = '#28a745';
        ctx.lineWidth = 2;
        ctx.stroke();
    }

    // Inicializar visualización vacía
    graficarFormaOnda([]);
    graficarEspectro([]);
}); 