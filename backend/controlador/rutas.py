from flask import Blueprint, render_template, request, jsonify, send_file, session
from backend.modelo.audio import ProcesadorAudio
import os, tempfile

rutas = Blueprint('rutas', __name__)

# Almacenar el audio en memoria temporal (por usuario/session)
audio_actual = {}

@rutas.route('/')
def principal():
    return render_template('principal.html')

@rutas.route('/api/audio/subir', methods=['POST'])
def subir_audio():
    archivo = request.files.get('audio')
    if not archivo:
        return jsonify({'error': 'No se recibió archivo'}), 400
    # Guardar archivo temporalmente
    temp = tempfile.NamedTemporaryFile(delete=False)
    archivo.save(temp.name)
    audio_actual['ruta'] = temp.name
    audio_actual['procesado'] = None
    return jsonify({'mensaje': 'Archivo subido correctamente'})

@rutas.route('/api/audio/convertir', methods=['POST'])
def convertir_audio():
    datos = request.json
    frecuencia = int(datos.get('frecuencia', 44100))
    bits = int(datos.get('bits', 16))
    if 'ruta' not in audio_actual:
        return jsonify({'error': 'No hay audio cargado'}), 400
    procesador = ProcesadorAudio(audio_actual['ruta'])
    procesador.convertir_frecuencia(frecuencia)
    procesador.convertir_bits(bits)
    # Guardar audio procesado temporalmente
    temp = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    procesador.audio.export(temp.name, format='wav')
    audio_actual['procesado'] = temp.name
    return jsonify({'mensaje': 'Audio convertido correctamente'})

@rutas.route('/api/audio/forma_onda', methods=['GET'])
def forma_onda():
    ruta = audio_actual.get('procesado') or audio_actual.get('ruta')
    if not ruta:
        return jsonify({'error': 'No hay audio cargado'}), 400
    procesador = ProcesadorAudio(ruta)
    datos = procesador.obtener_forma_onda()
    return jsonify({'forma_onda': datos})

@rutas.route('/api/audio/espectro', methods=['GET'])
def espectro():
    ruta = audio_actual.get('procesado') or audio_actual.get('ruta')
    if not ruta:
        return jsonify({'error': 'No hay audio cargado'}), 400
    procesador = ProcesadorAudio(ruta)
    datos = procesador.obtener_espectro()
    return jsonify({'espectro': datos})

@rutas.route('/api/audio/descargar', methods=['GET'])
def descargar_audio():
    ruta = audio_actual.get('procesado') or audio_actual.get('ruta')
    if not ruta:
        return jsonify({'error': 'No hay audio para descargar'}), 400
    return send_file(ruta, as_attachment=True, download_name='audio_convertido.wav')

@rutas.route('/api/ejemplo', methods=['GET'])
def api_ejemplo():
    return jsonify({'mensaje': 'API funcionando correctamente'}) 