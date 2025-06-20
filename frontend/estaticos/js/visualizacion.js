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
            await actualizarVisualizacion();
        } else {
            mensajeAudio.textContent = data.error || 'Error al subir audio.';
        }
    });

    // Convertir audio
    formConversion.addEventListener('submit', async function (e) {
        e.preventDefault();
        const frecuencia = document.getElementById('frecuencia').value;
        const bits = document.getElementById('bits').value;
        mensajeConversion.textContent = 'Convirtiendo...';
        const resp = await fetch('/api/audio/convertir', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ frecuencia, bits })
        });
        const data = await resp.json();
        if (resp.ok) {
            mensajeConversion.textContent = data.mensaje;
            await actualizarVisualizacion();
        } else {
            mensajeConversion.textContent = data.error || 'Error al convertir.';
        }
    });

    // Descargar audio procesado
    btnDescargar.addEventListener('click', function (e) {
        e.preventDefault();
        btnDescargar.href = '/api/audio/descargar';
        // El atributo download ya está puesto
    });

    // Visualización de forma de onda y espectro
    async function actualizarVisualizacion() {
        // Forma de onda
        const respOnda = await fetch('/api/audio/forma_onda');
        const dataOnda = await respOnda.json();
        if (respOnda.ok && dataOnda.forma_onda) {
            graficarFormaOnda(dataOnda.forma_onda);
        } else {
            graficarFormaOnda([]);
        }
        // Espectro
        const respEspectro = await fetch('/api/audio/espectro');
        const dataEspectro = await respEspectro.json();
        if (respEspectro.ok && dataEspectro.espectro) {
            graficarEspectro(dataEspectro.espectro);
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