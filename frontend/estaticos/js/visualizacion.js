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
    const fileUploadArea = document.querySelector('.file-upload-area');
    const notificationContainer = document.getElementById('notification-container');
    
    // Grabación
    const btnGrabar = document.getElementById('btn-grabar');
    const btnDetener = document.getElementById('btn-detener');
    const grabandoLabel = document.getElementById('grabando-label');
    const audioPreview = document.getElementById('audio-preview');
    const audioPreviewContainer = document.getElementById('audio-preview-container');

    let mediaRecorder = null;
    let audioChunks = [];
    let blobGrabado = null;
    let archivoIdActual = null; // Guardar ID del archivo subido

    // Configurar drag & drop
    setupDragAndDrop();

    // Función para configurar drag & drop
    function setupDragAndDrop() {
        fileUploadArea.addEventListener('dragover', function(e) {
            e.preventDefault();
            fileUploadArea.classList.add('dragover');
        });

        fileUploadArea.addEventListener('dragleave', function(e) {
            e.preventDefault();
            fileUploadArea.classList.remove('dragover');
        });

        fileUploadArea.addEventListener('drop', function(e) {
            e.preventDefault();
            fileUploadArea.classList.remove('dragover');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                inputAudio.files = files;
                mostrarNotificacion('Archivo Seleccionado', '📁 Archivo listo: ' + files[0].name, 'success');
            }
        });

        // Mostrar archivo seleccionado
        inputAudio.addEventListener('change', function() {
            if (this.files.length > 0) {
                mostrarNotificacion('Archivo Seleccionado', '📁 Archivo listo: ' + this.files[0].name, 'success');
            }
        });
    }

    // Función para mostrar notificaciones en la parte superior
    function mostrarNotificacion(titulo, mensaje, tipo = 'success') {
        const notification = document.createElement('div');
        notification.className = `notification ${tipo}`;
        
        const icono = tipo === 'success' ? '✓' : '❌';
        const tituloTexto = tipo === 'success' ? titulo : 'Error';
        
        notification.innerHTML = `
            <div class="notification-icon">${icono}</div>
            <div class="notification-content">
                <div class="notification-title">${tituloTexto}</div>
                <div class="notification-message">${mensaje}</div>
            </div>
            <button class="notification-close" onclick="this.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        notificationContainer.appendChild(notification);
        
        // Animar entrada
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);
        
        // Auto-remover después de 5 segundos
        setTimeout(() => {
            if (notification.parentElement) {
                notification.classList.remove('show');
                setTimeout(() => {
                    if (notification.parentElement) {
                        notification.remove();
                    }
                }, 500);
            }
        }, 5000);
        
        console.log('Notificación mostrada:', titulo, mensaje);
    }
    
    // Función para mostrar mensajes con estilos (mantener para compatibilidad)
    function mostrarMensaje(mensaje, tipo) {
        const titulo = tipo === 'success' ? 'Éxito' : 'Error';
        mostrarNotificacion(titulo, mensaje, tipo);
    }

    // Función para mostrar loading
    function mostrarLoading(elemento) {
        elemento.innerHTML = '<span class="loading-spinner"></span> Procesando...';
        elemento.classList.remove('d-none');
    }

    // Grabación de audio
    btnGrabar.addEventListener('click', async function () {
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            mostrarMensaje('Tu navegador no soporta grabación de audio', 'error');
            return;
        }
        
        try {
            btnGrabar.classList.add('d-none');
            btnDetener.classList.remove('d-none');
            grabandoLabel.classList.remove('d-none');
            audioPreviewContainer.classList.add('d-none');
            mensajeAudio.classList.add('d-none');
            
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
                audioPreviewContainer.classList.remove('d-none');
                inputAudio.value = '';
                mostrarNotificacion('Éxito', 'Audio grabado exitosamente', 'success');
            };
            
            mediaRecorder.start();
            
        } catch (error) {
            mostrarMensaje('Error al acceder al micrófono: ' + error.message, 'error');
            btnGrabar.classList.remove('d-none');
            btnDetener.classList.add('d-none');
            grabandoLabel.classList.add('d-none');
        }
    });

    btnDetener.addEventListener('click', function () {
        if (mediaRecorder && mediaRecorder.state === 'recording') {
            mediaRecorder.stop();
            mediaRecorder.stream.getTracks().forEach(track => track.stop());
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
            mostrarMensaje('Selecciona o graba un archivo de audio.', 'error');
            return;
        }
        
        const formData = new FormData();
        formData.append('audio', archivo);
        
        mostrarLoading(mensajeAudio);
        
        try {
            const resp = await fetch('/api/audio/subir', {
                method: 'POST',
                body: formData
            });
            
            const data = await resp.json();
            
            if (resp.ok) {
                console.log('Archivo subido exitosamente, mostrando mensaje...'); // Debug
                mostrarNotificacion('Archivo Subido', '✅ ¡Audio subido exitosamente! El archivo está listo para procesar.', 'success');
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
                
                // Animación de entrada
                appReproductor.style.opacity = '0';
                appReproductor.style.transform = 'translateY(20px)';
                setTimeout(() => {
                    appReproductor.style.transition = 'all 0.5s ease';
                    appReproductor.style.opacity = '1';
                    appReproductor.style.transform = 'translateY(0)';
                }, 100);

            } else {
                mostrarMensaje(data.detail || data.error || 'Error al subir audio.', 'error');
            }
        } catch (error) {
            mostrarMensaje('Error de conexión: ' + error.message, 'error');
        }
    });

    // Convertir audio
    formConversion.addEventListener('submit', async function (e) {
        e.preventDefault();
        if (!archivoIdActual) {
            mostrarMensaje('Primero debes subir un archivo.', 'error');
            return;
        }

        try {
            const frecuencia = document.getElementById('frecuencia').value;
            const bits = document.getElementById('bits').value;
            
            const formData = new FormData();
            formData.append('frecuencia_muestreo', frecuencia);
            formData.append('bits', bits);

            mostrarLoading(mensajeConversion);
            
            const resp = await fetch(`/api/audio/convertir/${archivoIdActual}`, {
                method: 'POST',
                body: formData
            });

            const data = await resp.json();

            if (resp.ok) {
                mostrarNotificacion('Conversión Completada', '🎵 ¡Audio convertido exitosamente! El archivo procesado está listo.', 'success');
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

                // Animación de actualización
                appReproductor.style.transform = 'scale(1.02)';
                setTimeout(() => {
                    appReproductor.style.transition = 'transform 0.3s ease';
                    appReproductor.style.transform = 'scale(1)';
                }, 100);

            } else {
                mostrarMensaje(`Error del servidor: ${data.detail || data.error || 'Error desconocido.'}`, 'error');
            }
        } catch (error) {
            console.error('Error en la función de conversión:', error);
            mostrarMensaje(`Error de conexión: ${error.message}`, 'error');
        }
    });

    // Descargar audio procesado
    btnDescargar.addEventListener('click', function (e) {
        if (!archivoIdActual) {
            e.preventDefault();
            mostrarMensaje('No hay un archivo procesado para descargar. Sube y convierte un audio primero.', 'error');
            return;
        }
        btnDescargar.href = `/api/audio/descargar/${archivoIdActual}`;
        
        // Animación de descarga
        btnDescargar.style.transform = 'scale(0.95)';
        setTimeout(() => {
            btnDescargar.style.transition = 'transform 0.2s ease';
            btnDescargar.style.transform = 'scale(1)';
        }, 200);
    });

    // Visualización de forma de onda y espectro
    async function actualizarVisualizacion() {
        if (!archivoIdActual) return;

        try {
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
        } catch (error) {
            console.error('Error al actualizar visualización:', error);
        }
    }

    // Graficar forma de onda con mejor diseño
    function graficarFormaOnda(datos) {
        const ctx = canvasOnda.getContext('2d');
        ctx.clearRect(0, 0, canvasOnda.width, canvasOnda.height);
        
        if (datos.length === 0) {
            // Mostrar mensaje cuando no hay datos
            ctx.fillStyle = '#a8a8a8';
            ctx.font = '14px Arial';
            ctx.textAlign = 'center';
            ctx.fillText('Sube un archivo para ver la forma de onda', canvasOnda.width / 2, canvasOnda.height / 2);
            return;
        }
        
        // Crear gradiente para la forma de onda
        const gradient = ctx.createLinearGradient(0, 0, canvasOnda.width, 0);
        gradient.addColorStop(0, '#667eea');
        gradient.addColorStop(0.5, '#764ba2');
        gradient.addColorStop(1, '#667eea');
        
        ctx.beginPath();
        ctx.strokeStyle = gradient;
        ctx.lineWidth = 3;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';
        
        for (let i = 0; i < datos.length; i++) {
            const x = (i / datos.length) * canvasOnda.width;
            const y = (1 - (datos[i] - Math.min(...datos)) / (Math.max(...datos) - Math.min(...datos) || 1)) * canvasOnda.height;
            if (i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        }
        
        ctx.stroke();
        
        // Agregar sombra
        ctx.shadowColor = 'rgba(102, 126, 234, 0.5)';
        ctx.shadowBlur = 10;
        ctx.stroke();
        ctx.shadowBlur = 0;
    }

    // Graficar espectro con mejor diseño
    function graficarEspectro(datos) {
        const ctx = canvasEspectro.getContext('2d');
        ctx.clearRect(0, 0, canvasEspectro.width, canvasEspectro.height);
        
        if (datos.length === 0) {
            // Mostrar mensaje cuando no hay datos
            ctx.fillStyle = '#a8a8a8';
            ctx.font = '14px Arial';
            ctx.textAlign = 'center';
            ctx.fillText('Sube un archivo para ver el espectro', canvasEspectro.width / 2, canvasEspectro.height / 2);
            return;
        }
        
        // Crear gradiente para el espectro
        const gradient = ctx.createLinearGradient(0, 0, 0, canvasEspectro.height);
        gradient.addColorStop(0, '#4facfe');
        gradient.addColorStop(1, '#00f2fe');
        
        ctx.fillStyle = gradient;
        
        const barWidth = canvasEspectro.width / datos.length;
        const maxMagnitude = Math.max(...datos);
        
        for (let i = 0; i < datos.length; i++) {
            const barHeight = (datos[i] / maxMagnitude) * canvasEspectro.height;
            const x = i * barWidth;
            const y = canvasEspectro.height - barHeight;
            
            // Agregar sombra
            ctx.shadowColor = 'rgba(79, 172, 254, 0.5)';
            ctx.shadowBlur = 5;
            
            ctx.fillRect(x, y, barWidth - 1, barHeight);
        }
        
        ctx.shadowBlur = 0;
    }

    // Inicializar visualización vacía
    graficarFormaOnda([]);
    graficarEspectro([]);
    
    // Agregar animación de entrada a las tarjetas
    const cards = document.querySelectorAll('.card-custom');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        setTimeout(() => {
            card.style.transition = 'all 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 200);
    });
    
    // Verificar que los elementos de mensaje existen
    console.log('Elemento mensajeAudio:', mensajeAudio);
    console.log('Elemento mensajeConversion:', mensajeConversion);
    
    // Mostrar mensaje de prueba al cargar (opcional, para debug)
    // setTimeout(() => {
    //     mostrarMensaje('🚀 Sistema listo para procesar audio', 'success');
    // }, 1000);
}); 