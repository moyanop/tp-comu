from pydub import AudioSegment
import numpy as np
from scipy.fft import fft
import io

class ProcesadorAudio:
    def __init__(self, archivo=None):
        self.audio = None
        if archivo:
            self.cargar_audio(archivo)

    def cargar_audio(self, archivo):
        self.audio = AudioSegment.from_file(archivo)

    def convertir_frecuencia(self, nueva_frecuencia):
        if self.audio:
            self.audio = self.audio.set_frame_rate(nueva_frecuencia)

    def convertir_bits(self, nuevos_bits):
        if self.audio:
            self.audio = self.audio.set_sample_width(nuevos_bits // 8)

    def exportar(self, formato='wav'):
        if self.audio:
            buffer = io.BytesIO()
            self.audio.export(buffer, format=formato)
            buffer.seek(0)
            return buffer
        return None

    def obtener_muestras(self):
        if self.audio:
            muestras = np.array(self.audio.get_array_of_samples())
            if self.audio.channels == 2:
                muestras = muestras.reshape((-1, 2))
                muestras = muestras.mean(axis=1)  # Convertir a mono para visualización
            return muestras
        return np.array([])

    def obtener_forma_onda(self, cantidad=1000):
        muestras = self.obtener_muestras()
        if len(muestras) == 0:
            return []
        factor = max(1, len(muestras) // cantidad)
        return muestras[::factor].tolist()

    def obtener_espectro(self, cantidad=512):
        muestras = self.obtener_muestras()
        if len(muestras) == 0:
            return []
        espectro = np.abs(fft(muestras))[:cantidad]
        return espectro.tolist() 